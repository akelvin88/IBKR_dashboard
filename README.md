# IBKR Performance Dashboard

A comprehensive performance dashboard for analyzing Interactive Brokers (IBKR) account performance with Money-Weighted Return (MWR) calculations. Build with Streamlit for easy sharing and collaboration.

## 🎯 Features

- **Monthly & Yearly Performance**: View returns in percentage and absolute values
- **Money-Weighted Returns (MWR)**: Accurate performance measurement accounting for cash flows
- **NAV Progression**: Monitor account Net Asset Value over time
- **Interactive Charts**: Plotly-based visualizations for data exploration
- **File Upload**: Upload your IBKR CSV directly without file system access
- **Data Export**: Export performance analysis to CSV format
- **Responsive Design**: Works on desktop and mobile browsers

## 🚀 Quick Start

### Online Demo
Visit the deployed app: [https://ibkr-dashboard-akelvin88.streamlit.app](https://ibkr-dashboard-akelvin88.streamlit.app)

### Local Installation

**Prerequisites:**
- Python 3.9 or higher
- pip (Python package manager)

**Step 1: Clone the repository**
```bash
git clone https://github.com/your-username/ibkr_dashboard.git
cd ibkr_dashboard
```

**Step 2: Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Step 3: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Run the dashboard**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📊 How to Use

1. **Upload Your Data**:
   - Click "Browse files" in the sidebar
   - Select your IBKR account statement CSV (exported from your Interactive Brokers account)
   - The dashboard automatically processes your data

2. **View Performance**:
   - **Monthly Performance Tab**: See monthly returns in percentage and value
   - **Yearly Performance Tab**: Track annual performance and wealth growth
   - **NAV Progression Tab**: Monitor account value trends
   - **Data Table Tab**: Export data in CSV format

3. **Understand the Metrics**:
   - **MWR (Money-Weighted Return)**: Accounts for timing of deposits/withdrawals
   - **NAV (Net Asset Value)**: Account value at specific points in time
   - **Cumulative Return**: Total return from inception to present

## 📋 IBKR CSV Export Format

The CSV file should contain:
- "Introduction" section with account details
- "Key Statistics" section with account summary
- "Historical Performance Benchmark Comparison" section with monthly data

**To export from IBKR:**
1. Log in to Interactive Brokers
2. Go to Account Menu → Performance → Reports
3. Choose time period and export as CSV
4. Upload the file to this dashboard

## 🌐 Deploy on Streamlit Cloud (Free)

1. **Push to GitHub**:
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy on Streamlit Cloud**:
   - Go to [streamlit.io/cloud](https://streamlit.io/cloud)
   - Click "New app"
   - Connect your GitHub repository
   - Select this repo and `app.py`
   - Click "Deploy"

3. **Share the URL**: Your app will be live at a public URL

## 📁 Project Structure

```
ibkr_dashboard/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .gitignore               # Git ignore rules
├── data/                    # Optional: sample data folder
└── src/
    ├── __init__.py
    └── data_processor.py    # IBKR data processing module
```

## 🔧 Data Processing

### IBKRDataProcessor Class

The `IBKRDataProcessor` handles:
- Loading and parsing IBKR CSV statements
- Extracting monthly return data
- Calculating Money-Weighted Returns (MWR)
- Computing NAV values and changes
- Aggregating performance metrics

### Key Methods

- `load_data()`: Reads CSV file (handles both file paths and file-like objects)
- `extract_monthly_returns()`: Parses monthly return percentages
- `extract_key_statistics()`: Retrieves account summary statistics
- `calculate_mwr()`: Computes MWR by month and year
- `calculate_nav_values()`: Estimates NAV progression
- `get_performance_summary()`: Returns complete analysis

## 📦 Dependencies

- **streamlit**: Web framework for data applications
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **plotly**: Interactive charting library
- **pyxirr**: XIRR calculations for MWR analysis
- **python-dateutil**: Date manipulation utilities

## 🐛 Troubleshooting

### CSV Upload Issues
- Ensure your IBKR export includes the "Historical Performance Benchmark Comparison" section
- Check that the file is valid CSV format
- Try exporting again from IBKR if you're having parsing errors

### App Won't Start
- Verify all dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (need 3.9+)
- Try verbose mode: `streamlit run app.py --logger.level=debug`

### Data Not Appearing
- Verify your CSV has monthly performance data
- Check that the data includes at least 1 month of performance
- Ensure no special characters in field values

## 🔒 Security

- No data is stored on servers
- Uploaded files are processed in-memory only
- Files are not saved to disk permanently
- Perfect for sensitive financial data

## 🚀 Future Enhancements

- Real-time data sync with IBKR API
- Portfolio composition analysis
- Risk metrics and Sharpe ratio calculations
- Benchmark comparison tools
- Custom date range selection
- Performance attribution analysis
- Multi-account support

## 📝 License

This project is open source and available for personal and educational use.

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## ⚙️ Support

For issues or questions:
1. Check the troubleshooting section
2. Open an issue on GitHub
3. Review your CSV export format from IBKR

---

**Last Updated**: March 2026  
**Python Version**: 3.9+  
**Streamlit Version**: 1.28.1+

