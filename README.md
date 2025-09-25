# FitLoop: AI Feedback-to-Guidance Optimizer

FitLoop is a lightweight web application that converts product review and return reason text into structured fit/care issues and actionable size & care guidance. It helps retail teams reduce avoidable returns by providing data-driven sizing guidance and care instructions.

## 🚀 Features

- **CSV Upload & Validation**: Upload reviews and returns data with automatic schema validation
- **AI-Powered Issue Extraction**: Uses OpenAI GPT or fallback rule-based extraction to identify fit and care issues
- **Risk Scoring**: Calculates product-level risk scores based on issue severity and frequency
- **Automated Copy Generation**: Creates size guidance and care tip snippets for each product
- **Interactive Dashboard**: Browse products by risk score, filter by categories, and search
- **Detailed Product Views**: Analyze individual products with issue breakdowns and generated copy
- **Markdown Export**: Export detailed product analysis reports
- **Zero PII**: No personal data required - only product feedback text

## 🏗️ Architecture

```
Browser (React) → FastAPI Backend → SQLite Database
                      ↓
                AI Processing Pipeline
                (OpenAI GPT / Rule-based)
                      ↓
             Risk Scoring & Copy Generation
```

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

## ⚡ Quick Start

### Backend Setup

1. **Clone and navigate to project**:
   ```bash
   cd fitloop
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   copy .env.sample .env
   ```
   
   Edit `.env` and set:
   - `AUTH_TOKEN`: Choose a secure token for API authentication
   - `OPENAI_API_KEY`: Optional - for AI extraction (uses rule-based fallback if not provided)

5. **Start backend**:
   ```bash
   uvicorn main:app --reload
   ```
   
   Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```
   
   Frontend will be available at `http://localhost:5173`

## 📊 Data Format

### Reviews CSV
Required columns:
- `product_id`: Product identifier
- `review_text`: Customer review text
- `rating`: Numeric rating (1-5)
- `date`: Date string (any format)

### Returns CSV
Required columns:
- `product_id`: Product identifier  
- `return_reason_text`: Reason for return
- `condition_flag`: Item condition (good/used/damaged)
- `date`: Date string (any format)

## 🔄 Usage Flow

1. **Upload Data**: Go to Upload page and select your CSV files
2. **Validate**: System validates column schemas and uploads data
3. **Process**: Click "Process Data" to run AI analysis pipeline
4. **Review Results**: Navigate to Dashboard to see product risk scores
5. **Analyze Products**: Click on products to see detailed analysis
6. **Export Reports**: Download Markdown reports for specific products

## 🧮 Processing Pipeline

1. **Data Ingestion**: CSV files validated and stored in SQLite
2. **Text Cleaning**: Normalize text (lowercase, remove special characters)
3. **Issue Extraction**: 
   - AI Path: Batch texts to OpenAI GPT for structured extraction
   - Fallback: Rule-based keyword matching and categorization
4. **Aggregation**: Group issues by descriptor, calculate frequency percentages
5. **Risk Scoring**: `risk_score = 0.6 * severity_norm + 0.4 * frequency_norm`
6. **Copy Generation**: Create size guidance and care tip snippets
7. **Storage**: Persist results for dashboard and reporting

## 🎯 Sample Data

Sample CSV files are provided in `sample_data/`:
- `reviews_sample.csv`: Basic sample with 5 products
- `returns_sample.csv`: Corresponding returns data
- `reviews_extended.csv`: Extended sample with 10 products  
- `returns_extended.csv`: Extended returns data

## 🔧 Configuration

### Environment Variables

- `AUTH_TOKEN`: API authentication token (required)
- `OPENAI_API_KEY`: OpenAI API key for AI extraction (optional)
- `API_MODEL_PROVIDER`: Model provider ("openai", default)

### Frontend Configuration

The frontend automatically proxies API calls to `http://localhost:8000`. For production deployment, update the `VITE_API_BASE_URL` environment variable.

## 📡 API Endpoints

- `POST /upload` - Upload CSV files
- `POST /process` - Process uploaded data  
- `GET /products` - List all products with summaries
- `GET /product/{id}` - Get detailed product analysis
- `GET /export/{id}` - Export product report as Markdown
- `GET /` - Health check

All endpoints require `X-Auth-Token` header.

## 🛡️ Security

- Simple token-based authentication via headers
- No sensitive customer data stored (only product feedback text)
- CORS enabled for development (configure for production)
- Input validation on all uploads

## 🚦 Error Handling

- Comprehensive validation with user-friendly error messages
- Graceful fallback from AI to rule-based processing
- Database transaction rollbacks on failures
- Frontend toast notifications for user feedback

## 📈 Metrics & KPIs

The system is designed to support these business metrics:
- **Return Rate Reduction**: Size-related returns decreased by 5-8%
- **Processing Speed**: Complete analysis in under 2 minutes
- **Issue Detection Accuracy**: ≥80% precision on manual audit
- **Copy Adoption**: ≥70% of generated guidance accepted

## 🔄 Risk Score Calculation

Risk scores are normalized within each product:
- **Severity**: Issue impact (1-5 scale)
- **Frequency**: How often mentioned (0-100%)
- **Formula**: `0.6 * normalized_severity + 0.4 * normalized_frequency`
- **Thresholds**: High (≥0.7), Medium (0.4-0.69), Low (<0.4)

## 🎨 AI Extraction

### With OpenAI API
Uses GPT-4o-mini with structured prompts for:
- Issue categorization (fit/care)
- Severity scoring (1-5)
- Body area identification
- Frequency estimation

### Fallback Rules
Keyword-based extraction using predefined mappings:
- Size issues: "tight", "small", "loose", "large"
- Care issues: "fade", "shrink", "wrinkle", "pill"
- Body areas: "waist", "sleeve", "length", "color"

## 🚀 Deployment

### Development
```bash
# Backend
uvicorn main:app --reload

# Frontend  
npm run dev
```

### Production
```bash
# Backend
uvicorn main:app --host 0.0.0.0 --port 8000

# Frontend
npm run build
# Serve dist/ folder with nginx/apache
```

## 🧪 Testing

### Manual Testing Checklist
- [ ] Upload valid CSV files
- [ ] Validate error handling for invalid schemas
- [ ] Process data and verify results in dashboard
- [ ] Test product detail views and issue analysis
- [ ] Export Markdown reports
- [ ] Test with and without OpenAI API key

### Sample Test Cases
```bash
# Test with sample data
# 1. Upload sample_data/reviews_sample.csv + returns_sample.csv
# 2. Click Process Data
# 3. Verify 5 products appear in dashboard
# 4. Check product P1001 shows "runs_small" issues
# 5. Export report and verify Markdown format
```

## 🔮 Roadmap

- **Phase 1**: Core functionality (✅ Complete)
- **Phase 2**: Multilingual support
- **Phase 3**: Trend detection and alerts
- **Phase 4**: CMS integration APIs
- **Phase 5**: Advanced clustering and ML models

## 🐛 Troubleshooting

### Common Issues

**Upload fails with "missing columns"**
- Verify CSV has exact column names (case-sensitive)
- Check for hidden characters or encoding issues

**Processing returns no results**  
- Ensure products have ≥3 total feedback items
- Check OpenAI API key if using AI extraction
- Review backend logs for extraction errors

**Dashboard shows no products**
- Verify processing completed successfully
- Check authentication token in browser developer tools
- Refresh browser and try again

**Export doesn't download**
- Ensure popup blockers are disabled
- Try right-click "Save as" on export button
- Check browser download settings

## 📄 License

Internal hackathon prototype. No production guarantees or warranties.

## 🤝 Contributing

This is a hackathon project. For production use:
1. Add comprehensive test suite
2. Implement proper authentication
3. Add database migrations
4. Configure production CORS
5. Add monitoring and logging
6. Implement rate limiting

## 📞 Support

For questions or issues:
1. Check this README first
2. Review browser console for frontend errors  
3. Check backend logs for API errors
4. Verify environment configuration

---

**Built for TCS AI Hackathon 2025** - Transforming retail feedback into actionable insights 🎯