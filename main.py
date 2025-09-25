from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Header
from fastapi.responses import Response, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import io
import os
import logging
from datetime import datetime, timedelta
from collections import defaultdict, Counter

from database import get_db, Review, Return, Issue, Product, GeneratedCopy
from ai_processor import AIProcessor
from csv_utils import read_csv_from_string, safe_float, safe_int

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="FitLoop API", version="1.0.0")

# If frontend build exists, mount it (served under /app)
FRONTEND_BUILD_DIR = os.path.join(os.path.dirname(__file__), 'frontend', 'dist')
if os.path.isdir(FRONTEND_BUILD_DIR):
    app.mount('/app', StaticFiles(directory=FRONTEND_BUILD_DIR, html=True), name='app')

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI processor
ai_processor = AIProcessor()

# Authentication
def verify_token(x_auth_token: Optional[str] = Header(None)):
    expected_token = os.getenv("AUTH_TOKEN", "changeme123")
    if not x_auth_token or x_auth_token != expected_token:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return True

@app.post("/upload")
async def upload_files(
    reviews_csv: UploadFile = File(...),
    returns_csv: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: bool = Depends(verify_token)
):
    """Upload and validate CSV files"""
    try:
        # Read and validate reviews CSV
        reviews_content = await reviews_csv.read()
        reviews_data = read_csv_from_string(reviews_content.decode('utf-8'))
        
        required_review_cols = ['product_id', 'review_text', 'rating', 'date']
        if not reviews_data or not all(col in reviews_data[0].keys() for col in required_review_cols):
            if not reviews_data:
                raise HTTPException(status_code=400, detail="Reviews CSV is empty")
            missing_cols = [col for col in required_review_cols if col not in reviews_data[0].keys()]
            raise HTTPException(
                status_code=400, 
                detail=f"Reviews CSV missing required columns: {missing_cols}"
            )
        
        # Read and validate returns CSV
        returns_content = await returns_csv.read()
        returns_data = read_csv_from_string(returns_content.decode('utf-8'))
        
        required_return_cols = ['product_id', 'return_reason_text', 'condition_flag', 'date']
        if not returns_data or not all(col in returns_data[0].keys() for col in required_return_cols):
            if not returns_data:
                raise HTTPException(status_code=400, detail="Returns CSV is empty")
            missing_cols = [col for col in required_return_cols if col not in returns_data[0].keys()]
            raise HTTPException(
                status_code=400, 
                detail=f"Returns CSV missing required columns: {missing_cols}"
            )
        
        # Clear existing data
        db.query(Review).delete()
        db.query(Return).delete()
        db.query(Issue).delete()
        db.query(Product).delete()
        db.query(GeneratedCopy).delete()
        
        # Insert reviews
        for row in reviews_data:
            review = Review(
                product_id=str(row['product_id']),
                review_text=str(row['review_text']),
                rating=safe_int(row.get('rating', '3'), 3),
                date=str(row['date'])
            )
            db.add(review)
        
        # Insert returns
        for row in returns_data:
            return_record = Return(
                product_id=str(row['product_id']),
                return_reason_text=str(row['return_reason_text']),
                condition_flag=str(row['condition_flag']),
                date=str(row['date'])
            )
            db.add(return_record)
        
        db.commit()
        
        logger.info(f"Uploaded {len(reviews_data)} reviews and {len(returns_data)} returns")
        
        return {
            "status": "success",
            "reviews_uploaded": len(reviews_data),
            "returns_uploaded": len(returns_data)
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=400, detail=f"Upload failed: {str(e)}")

@app.post("/process")
async def process_data(
    db: Session = Depends(get_db),
    _: bool = Depends(verify_token)
):
    """Process uploaded data and extract issues"""
    try:
        # Get all reviews and returns
        reviews = db.query(Review).all()
        returns = db.query(Return).all()
        
        if not reviews and not returns:
            raise HTTPException(status_code=400, detail="No data to process")
        
        # Group by product
        product_data = defaultdict(lambda: {"reviews": [], "returns": []})
        
        for review in reviews:
            product_data[review.product_id]["reviews"].append(review.review_text)
        
        for return_record in returns:
            product_data[return_record.product_id]["returns"].append(return_record.return_reason_text)
        
        # Process each product
        products_processed = 0
        for product_id, data in product_data.items():
            # Combine all feedback texts
            all_texts = data["reviews"] + data["returns"]
            
            # Skip products with insufficient data
            if len(all_texts) < 3:
                logger.info(f"Skipping {product_id}: insufficient data ({len(all_texts)} texts)")
                continue
            
            # Extract issues using AI
            extracted_issues = ai_processor.extract_issues_llm(product_id, all_texts)
            
            if not extracted_issues:
                logger.info(f"No issues extracted for {product_id}")
                continue
            
            # Aggregate issues by descriptor
            issue_aggregates = defaultdict(list)
            for issue in extracted_issues:
                key = (issue.get("descriptor", ""), issue.get("issue_category", ""), issue.get("body_area", ""))
                issue_aggregates[key].append(issue)
            
            # Calculate aggregated metrics
            final_issues = []
            for (descriptor, category, body_area), issue_list in issue_aggregates.items():
                if not descriptor:
                    continue
                    
                avg_severity = sum(i.get("severity", 3) for i in issue_list) / len(issue_list)
                total_frequency = sum(i.get("frequency_hint", 0) for i in issue_list) / len(issue_list)
                
                final_issues.append({
                    "product_id": product_id,
                    "issue_category": category,
                    "body_area": body_area,
                    "descriptor": descriptor,
                    "severity": avg_severity,
                    "frequency_pct": min(100, total_frequency)
                })
            
            # Store issues in database
            for issue_data in final_issues:
                issue = Issue(
                    product_id=issue_data["product_id"],
                    issue_category=issue_data["issue_category"],
                    body_area=issue_data["body_area"],
                    descriptor=issue_data["descriptor"],
                    severity=issue_data["severity"],
                    frequency_pct=issue_data["frequency_pct"]
                )
                db.add(issue)
            
            # Calculate risk score
            if final_issues:
                # Normalize within product
                severities = [i["severity"] for i in final_issues]
                frequencies = [i["frequency_pct"] for i in final_issues]
                
                if len(severities) > 1:
                    severity_range = max(severities) - min(severities)
                    freq_range = max(frequencies) - min(frequencies)
                    
                    if severity_range > 0:
                        severity_norm = [(s - min(severities)) / severity_range for s in severities]
                    else:
                        severity_norm = [0.5 for _ in severities]  # All same, use middle value
                        
                    if freq_range > 0:
                        freq_norm = [(f - min(frequencies)) / freq_range for f in frequencies]
                    else:
                        freq_norm = [0.5 for _ in frequencies]  # All same, use middle value
                else:
                    severity_norm = [severities[0] / 5.0]
                    freq_norm = [frequencies[0] / 100.0]
                
                # Weighted risk score
                risk_scores = [0.6 * s + 0.4 * f for s, f in zip(severity_norm, freq_norm)]
                avg_risk_score = sum(risk_scores) / len(risk_scores)
                
                # Get top issue
                top_issue_idx = max(range(len(final_issues)), 
                                  key=lambda i: final_issues[i]["severity"] * final_issues[i]["frequency_pct"])
                top_issue_descriptor = final_issues[top_issue_idx]["descriptor"]
                
                # Store product summary
                product = Product(
                    product_id=product_id,
                    risk_score=avg_risk_score,
                    top_issue_descriptor=top_issue_descriptor,
                    updated_at=datetime.utcnow()
                )
                db.add(product)
                
                # Generate copy
                copy_result = ai_processor.generate_copy(product_id, final_issues)
                generated_copy = GeneratedCopy(
                    product_id=product_id,
                    size_guidance=copy_result.get("size_guidance", ""),
                    care_tip=copy_result.get("care_tip", ""),
                    generated_at=datetime.utcnow()
                )
                db.add(generated_copy)
                
                products_processed += 1
        
        db.commit()
        
        logger.info(f"Processed {products_processed} products")
        
        return {
            "status": "processed",
            "products_processed": products_processed
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/products")
async def get_products(
    db: Session = Depends(get_db),
    _: bool = Depends(verify_token)
):
    """Get all products with summary data"""
    try:
        products = db.query(Product).order_by(Product.risk_score.desc()).all()
        
        result = []
        for product in products:
            result.append({
                "product_id": product.product_id,
                "risk_score": round(product.risk_score, 3),
                "top_issue_descriptor": product.top_issue_descriptor,
                "updated_at": product.updated_at.isoformat() if product.updated_at else None
            })
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to get products: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/product/{product_id}")
async def get_product_detail(
    product_id: str,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_token)
):
    """Get detailed information for a specific product"""
    try:
        # Get product summary
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Get issues
        issues = db.query(Issue).filter(Issue.product_id == product_id).all()
        
        # Get generated copy
        generated_copy = db.query(GeneratedCopy).filter(GeneratedCopy.product_id == product_id).first()
        
        issues_data = []
        for issue in issues:
            issues_data.append({
                "issue_category": issue.issue_category,
                "body_area": issue.body_area or "",
                "descriptor": issue.descriptor,
                "severity": round(issue.severity, 2),
                "frequency_pct": round(issue.frequency_pct, 1)
            })
        
        copy_data = {
            "size_guidance": generated_copy.size_guidance if generated_copy else "",
            "care_tip": generated_copy.care_tip if generated_copy else ""
        }
        
        return {
            "product_id": product.product_id,
            "risk_score": round(product.risk_score, 3),
            "top_issue_descriptor": product.top_issue_descriptor,
            "updated_at": product.updated_at.isoformat() if product.updated_at else None,
            "issues": issues_data,
            "generated_copy": copy_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get product detail: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/export/{product_id}")
async def export_product(
    product_id: str,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_token)
):
    """Export product data as Markdown"""
    try:
        # Get product data
        product_data = await get_product_detail(product_id, db, True)
        
        # Generate Markdown
        markdown_content = f"""# Product {product_id}

**Risk Score:** {product_data['risk_score']}

## Size Guidance
{product_data['generated_copy']['size_guidance'] or 'No guidance available'}

## Care Tip
{product_data['generated_copy']['care_tip'] or 'No care tips available'}

## Issues Summary

| Descriptor | Category | Body Area | Frequency % | Severity |
|------------|----------|-----------|-------------|----------|
"""
        
        for issue in product_data['issues']:
            markdown_content += f"| {issue['descriptor']} | {issue['issue_category']} | {issue['body_area']} | {issue['frequency_pct']}% | {issue['severity']} |\n"
        
        if not product_data['issues']:
            markdown_content += "| No issues found | - | - | - | - |\n"
        
        markdown_content += f"\n---\n*Generated at: {datetime.utcnow().isoformat()}*"
        
        return Response(
            content=markdown_content,
            media_type="text/markdown",
            headers={"Content-Disposition": f"attachment; filename=product_{product_id}_analysis.md"}
        )
        
    except Exception as e:
        logger.error(f"Failed to export product: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def root():
    """Health check or redirect to UI if built."""
    if os.path.isdir(FRONTEND_BUILD_DIR):
        # Provide a small landing page with link to app UI
        return (
            "<html><head><title>FitLoop</title></head><body>"
            "<h2>FitLoop API is running ✅</h2>"
            "<p>Frontend is available at <a href='/app'>/app</a></p>"
            f"<p>AI Enabled: {ai_processor.client is not None}</p>"
            "</body></html>"
        )
    return (
        "<html><head><title>FitLoop</title></head><body>"
        "<h2>FitLoop API is running ✅ (no built frontend detected)</h2>"
        "<p>Build the frontend (npm run build) to serve it under /app.</p>"
        f"<p>AI Enabled: {ai_processor.client is not None}</p>"
        "</body></html>"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)