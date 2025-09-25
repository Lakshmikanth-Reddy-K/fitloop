# FitLoop - Technical Specifications & API Documentation

## System Requirements

### **Minimum Hardware Requirements**
- **CPU**: 2 cores, 2.4GHz
- **RAM**: 4GB available memory
- **Storage**: 10GB free disk space
- **Network**: Broadband internet connection (10Mbps+)

### **Recommended Hardware Requirements**
- **CPU**: 4+ cores, 3.0GHz+
- **RAM**: 8GB+ available memory
- **Storage**: 50GB+ free disk space (SSD recommended)
- **Network**: High-speed internet (50Mbps+)

### **Software Dependencies**
- **Python**: 3.11 or higher
- **Node.js**: 18.0 or higher (for React frontend)
- **Modern Web Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

## API Documentation

### **Base Configuration**
```
Base URL: https://fitloop-demo.onrender.com
API Version: v1
Authentication: Bearer Token
Content-Type: application/json
Token: fitloop2024
```

### **Authentication**
All API requests require authentication using a Bearer token in the Authorization header.

```http
Authorization: Bearer fitloop2024
```

### **Core Endpoints**

#### **1. File Upload**
```http
POST /upload
Content-Type: multipart/form-data
```

**Request Parameters:**
- `file` (required): CSV file containing reviews or returns data
- `data_type` (required): "reviews" or "returns"

**Response:**
```json
{
  "message": "File uploaded successfully",
  "file_id": "uuid-string",
  "records_processed": 1250,
  "processing_time": 2.3,
  "status": "success"
}
```

**Error Responses:**
```json
{
  "error": "Invalid file format",
  "details": "File must be in CSV format",
  "status": "error"
}
```

#### **2. Process Data**
```http
POST /process
Content-Type: application/json
```

**Request Body:**
```json
{
  "file_id": "uuid-string",
  "analysis_type": "full",
  "include_ai": true
}
```

**Response:**
```json
{
  "processing_id": "uuid-string",
  "status": "processing",
  "estimated_completion": "2024-01-15T10:30:00Z",
  "progress": 0
}
```

#### **3. Get Processing Status**
```http
GET /process/{processing_id}/status
```

**Response:**
```json
{
  "processing_id": "uuid-string",
  "status": "completed",
  "progress": 100,
  "results_available": true,
  "processing_time": 45.2
}
```

#### **4. Dashboard Data**
```http
GET /dashboard
```

**Query Parameters:**
- `product_id` (optional): Filter by specific product
- `date_from` (optional): Start date (YYYY-MM-DD)
- `date_to` (optional): End date (YYYY-MM-DD)
- `risk_level` (optional): "low", "medium", "high"

**Response:**
```json
{
  "summary": {
    "total_reviews": 5280,
    "total_returns": 1340,
    "high_risk_products": 23,
    "average_rating": 4.2
  },
  "products": [
    {
      "product_id": "PROD-001",
      "risk_score": 0.75,
      "review_count": 150,
      "return_count": 45,
      "issues": ["sizing", "quality", "shipping"]
    }
  ],
  "trends": {
    "return_rate_trend": [0.12, 0.15, 0.18, 0.22],
    "satisfaction_trend": [4.1, 4.0, 3.9, 3.8]
  }
}
```

#### **5. Product Details**
```http
GET /product/{product_id}
```

**Response:**
```json
{
  "product_id": "PROD-001",
  "risk_score": 0.75,
  "risk_level": "high",
  "total_reviews": 150,
  "total_returns": 45,
  "average_rating": 3.2,
  "return_rate": 0.30,
  "issues": [
    {
      "type": "sizing",
      "frequency": 65,
      "severity": "high",
      "sample_feedback": ["Too small", "Runs small", "Size chart inaccurate"]
    }
  ],
  "recommendations": [
    "Update size chart with customer measurements",
    "Consider adding size guide video",
    "Implement virtual fitting tool"
  ],
  "ai_summary": "High return rate due to sizing issues...",
  "reviews": [
    {
      "review_id": "REV-001",
      "rating": 2,
      "text": "Product runs very small, had to return",
      "sentiment": "negative",
      "issues_identified": ["sizing"]
    }
  ]
}
```

#### **6. Export Report**
```http
GET /export
```

**Query Parameters:**
- `format` (required): "pdf", "csv", "json"
- `product_ids` (optional): Comma-separated list of product IDs
- `date_from` (optional): Start date
- `date_to` (optional): End date

**Response Headers:**
```http
Content-Type: application/pdf
Content-Disposition: attachment; filename="fitloop-report-2024-01-15.pdf"
```

#### **7. Health Check**
```http
GET /health
HEAD /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00Z",
  "uptime": 3600,
  "dependencies": {
    "database": "healthy",
    "ai_service": "healthy",
    "file_storage": "healthy"
  }
}
```

### **WebSocket Endpoints**

#### **Real-time Processing Updates**
```javascript
const ws = new WebSocket('wss://fitloop-demo.onrender.com/ws/processing');

ws.onmessage = function(event) {
  const data = JSON.parse(event.data);
  console.log('Processing progress:', data.progress);
};
```

**Message Format:**
```json
{
  "type": "progress_update",
  "processing_id": "uuid-string",
  "progress": 65,
  "stage": "ai_analysis",
  "eta_seconds": 120
}
```

## Data Schemas

### **Reviews CSV Schema**
```csv
product_id,review_text,rating,date,reviewer_id,verified_purchase
PROD-001,"Great quality product!",5,2024-01-15,USER123,true
PROD-002,"Too small, returning",2,2024-01-14,USER456,true
```

**Field Specifications:**
- `product_id`: String, max 50 characters, required
- `review_text`: String, max 5000 characters, required
- `rating`: Integer, 1-5 scale, required
- `date`: ISO 8601 date format (YYYY-MM-DD), required
- `reviewer_id`: String, max 100 characters, optional
- `verified_purchase`: Boolean, optional (default: false)

### **Returns CSV Schema**
```csv
product_id,return_reason,condition_flag,date,order_id,refund_amount
PROD-001,"Too small",damaged,2024-01-15,ORD789,29.99
PROD-002,"Wrong color",new,2024-01-14,ORD790,45.00
```

**Field Specifications:**
- `product_id`: String, max 50 characters, required
- `return_reason`: String, max 1000 characters, required
- `condition_flag`: Enum ["new", "used", "damaged"], required
- `date`: ISO 8601 date format, required
- `order_id`: String, max 100 characters, optional
- `refund_amount`: Decimal (2 places), optional

### **Database Schema**

#### **Reviews Table**
```sql
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id VARCHAR(50) NOT NULL,
    review_text TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    date DATE NOT NULL,
    reviewer_id VARCHAR(100),
    verified_purchase BOOLEAN DEFAULT FALSE,
    sentiment VARCHAR(20),
    processed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_product_id (product_id),
    INDEX idx_date (date),
    INDEX idx_rating (rating)
);
```

#### **Returns Table**
```sql
CREATE TABLE returns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id VARCHAR(50) NOT NULL,
    return_reason TEXT NOT NULL,
    condition_flag VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    order_id VARCHAR(100),
    refund_amount DECIMAL(10,2),
    processed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_product_id (product_id),
    INDEX idx_date (date),
    INDEX idx_condition (condition_flag)
);
```

#### **Issues Table**
```sql
CREATE TABLE issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id VARCHAR(50) NOT NULL,
    issue_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    frequency INTEGER DEFAULT 1,
    sample_text TEXT,
    confidence_score DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_product_id (product_id),
    INDEX idx_issue_type (issue_type),
    INDEX idx_severity (severity)
);
```

## Error Handling

### **HTTP Status Codes**
- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Invalid data format
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Temporary service disruption

### **Error Response Format**
```json
{
  "error": "validation_error",
  "message": "Invalid file format provided",
  "details": {
    "field": "file",
    "expected": "CSV format",
    "received": "Excel format"
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "request_id": "req-uuid-string"
}
```

## Rate Limiting

### **API Limits**
- **Free Tier**: 100 requests/hour, 1,000 records/day
- **Starter**: 1,000 requests/hour, 10,000 records/day
- **Professional**: 10,000 requests/hour, 100,000 records/day
- **Enterprise**: Unlimited requests, custom limits

### **Rate Limit Headers**
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642248600
X-RateLimit-Window: 3600
```

## Security Specifications

### **Data Encryption**
- **In Transit**: TLS 1.3 encryption for all API communication
- **At Rest**: AES-256 encryption for stored data
- **API Keys**: SHA-256 hashed with salt

### **Access Control**
- **Authentication**: JWT tokens with 24-hour expiration
- **Authorization**: Role-based access control (RBAC)
- **Audit Logging**: All API calls logged with timestamps

### **Compliance**
- **GDPR**: Right to data deletion and export
- **CCPA**: California consumer privacy compliance
- **SOC 2 Type II**: Security and availability controls

## Performance Specifications

### **Response Time SLAs**
- **API Endpoints**: < 200ms (95th percentile)
- **File Upload**: < 2 seconds per MB
- **Data Processing**: < 30 seconds per 1,000 records
- **Report Generation**: < 5 seconds for standard reports

### **Throughput Limits**
- **Concurrent Connections**: 1,000 simultaneous users
- **File Processing**: 100MB maximum file size
- **Batch Processing**: 100,000 records per batch
- **Real-time Updates**: 100 WebSocket connections

## SDKs and Integration Libraries

### **Python SDK**
```bash
pip install fitloop-sdk
```

```python
from fitloop import FitLoopClient

client = FitLoopClient(api_key='fitloop2024')
result = client.upload_file('reviews.csv', 'reviews')
dashboard = client.get_dashboard()
```

### **JavaScript SDK**
```bash
npm install fitloop-js-sdk
```

```javascript
import { FitLoopClient } from 'fitloop-js-sdk';

const client = new FitLoopClient('fitloop2024');
const dashboard = await client.getDashboard();
```

### **cURL Examples**

#### **Upload File**
```bash
curl -X POST https://fitloop-demo.onrender.com/upload \
  -H "Authorization: Bearer fitloop2024" \
  -F "file=@reviews.csv" \
  -F "data_type=reviews"
```

#### **Get Dashboard**
```bash
curl -X GET https://fitloop-demo.onrender.com/dashboard \
  -H "Authorization: Bearer fitloop2024"
```

#### **Export Report**
```bash
curl -X GET "https://fitloop-demo.onrender.com/export?format=pdf" \
  -H "Authorization: Bearer fitloop2024" \
  -o "report.pdf"
```

This comprehensive API documentation enables developers to integrate FitLoop into existing systems and build custom applications on top of the platform.