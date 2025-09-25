# FitLoop Testing Guide

## Quick Test Script

### 1. Setup & Installation
```bash
# Setup environment
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.sample .env

# Frontend setup
cd frontend
npm install
cd ..
```

### 2. Start Services
```bash
# Terminal 1 - Backend
uvicorn main:app --reload

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

### 3. Basic Flow Test

**Step 1: Upload Sample Data**
- Navigate to http://localhost:5173
- Go to Upload page
- Upload `sample_data/reviews_sample.csv` and `sample_data/returns_sample.csv`
- Verify success message

**Step 2: Process Data**
- Click "Process Data" button
- Wait for completion message
- Should navigate to Dashboard automatically

**Step 3: Verify Dashboard**
- Should show 5 products (P1001, P1002, P1003, P1004, P1005)
- P1001 should show "runs_small" as top issue
- P1002 should show color-related issues
- Risk scores should be calculated

**Step 4: Product Detail**
- Click "View Details" for P1001
- Should show size guidance about sizing up
- Issues table should show fit issues
- Export button should download Markdown file

### 4. Extended Test (Optional)
Repeat with `reviews_extended.csv` and `returns_extended.csv` for 10 products.

## Expected Results

### Products from Sample Data:
- **P1001**: High risk, runs_small issue, size guidance "Consider one size up"
- **P1002**: Medium risk, color_fade issue, care tip about cold wash
- **P1003**: Medium risk, runs_large issue, size guidance about sizing down
- **P1004**: Low risk, no major issues
- **P1005**: Medium risk, shrink issue, care tip about air drying

### API Test Endpoints:
```bash
# Health check
curl -H "X-Auth-Token: changeme123" http://localhost:8000/

# Get products
curl -H "X-Auth-Token: changeme123" http://localhost:8000/products

# Get specific product
curl -H "X-Auth-Token: changeme123" http://localhost:8000/product/P1001
```

## Troubleshooting

### Backend Issues:
- Check Python version (3.11+)
- Verify all dependencies installed
- Check .env file exists and has AUTH_TOKEN

### Frontend Issues:  
- Check Node.js version (18+)
- Verify npm install completed
- Clear browser cache

### Processing Issues:
- Verify CSV format matches exactly
- Check minimum 3 feedback items per product
- OpenAI key optional (uses fallback)

## Manual Validation Checklist

- [ ] Upload page validates CSV schemas
- [ ] Processing extracts issues correctly
- [ ] Dashboard shows risk-ranked products
- [ ] Product detail shows generated copy
- [ ] Export downloads Markdown file
- [ ] Filtering and search work
- [ ] Error handling shows user messages
- [ ] Authentication prevents unauthorized access

## Performance Expectations

- Upload: <5 seconds for sample files
- Processing: <30 seconds for 5 products  
- Dashboard load: <2 seconds
- Product detail: <1 second
- Export: <3 seconds

Pass criteria: All core flows complete without errors.