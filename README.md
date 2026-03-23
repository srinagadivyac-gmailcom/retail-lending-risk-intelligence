# 💳 Retail Lending Risk Intelligence

> Credit risk analysis project using feature engineering, statistical analysis, and customer segmentation to identify high-risk borrowers and improve loan default prediction using Python and MySQL.

---

## 📌 Overview

This project analyzes retail lending data to identify high-risk borrower segments and provide data-driven recommendations for risk mitigation. The analysis covers EMI stress testing, credit score bucketing, NPA analysis by region, and SQL-backed risk queries.

---

## 🛠️ Tech Stack

| Tool | Usage |
|------|-------|
| Python (Pandas) | Data cleaning, EDA, feature engineering |
| Matplotlib | Risk dashboard visualizations |
| MySQL + SQLAlchemy | Database integration & SQL risk queries |
| python-dotenv | Secure credential management |

---

## ✨ Key Features

- 🧹 **Data Cleaning** — Null handling, deduplication, IQR-based outlier removal
- ⚙️ **Feature Engineering** — EMI-to-income ratio, credit score buckets, risk flag creation
- 📊 **EDA** — Default rate by loan type, credit score, EMI stress, region-wise NPA
- 🗄️ **MySQL Integration** — Data loaded to DB, SQL queries for risk segmentation
- 📈 **Visual Dashboard** — 4-chart risk analytics dashboard
- 💡 **Key Insights** — Pareto-based risk findings, high-risk region identification

---

## 📊 Dashboard Visualizations

1. Default Rate by Loan Type (Bar Chart)
2. Credit Score vs Default Rate (Bar Chart)
3. EMI-to-Income Ratio Distribution (Histogram)
4. Region-wise NPA Rate (Bar Chart)

---

## 💡 Key Insights

- Unsecured loans (Personal Loan, Credit Card) show highest default rates
- Low credit score customers (< 500) contribute most NPAs
- EMI-to-income ratio > 0.5 is a strong default predictor
- Certain regions consistently show higher risk levels

---

## 📁 Project Structure

```
retail-lending-risk-intelligence/
│
├── loan_risk_analysis.py            # Main analysis script
├── RetailLendingRiskIntelligence.csv  # Dataset (add locally)
├── .env.example                     # Environment variable template
├── .gitignore                       # Excludes .env and sensitive files
├── requirements.txt                 # Dependencies
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/srinagadivyac-gmailcom/retail-lending-risk-intelligence
cd retail-lending-risk-intelligence
```

### 2. Install Dependencies
```bash
pip install pandas matplotlib sqlalchemy mysql-connector-python python-dotenv
```

### 3. Configure Environment Variables
```bash
cp .env.example .env
# Edit .env with your MySQL credentials
```

### 4. Add Dataset
Place `RetailLendingRiskIntelligence.csv` in the project root folder.

### 5. Run the Analysis
```bash
python loan_risk_analysis.py
```

---

## 🔒 Security Notes

- Database credentials stored in `.env` file (never committed to GitHub)
- `.gitignore` excludes `.env` and sensitive files
- Use `.env.example` as setup template

---

## 👩‍💻 Author

**Srinaga Divya Chunchula**  
Data Analyst | Python | SQL | Power BI  
📧 srinagadivyac@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/sri-naga-divya-chunchula-955b56288)  
🐙 [GitHub](https://github.com/srinagadivyac-gmailcom)
