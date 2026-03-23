import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

def load_loan_data():
    df = pd.read_csv("RetailLendingRiskIntelligence.csv")
    print("Dataset Loaded | Shape:", df.shape)
    return df

def clean_data(df):
    print("\n=== Data Cleaning & Preprocessing ===")

    df['monthly_income'] = df['monthly_income'].fillna(df['monthly_income'].median())
    df['credit_score'] = df['credit_score'].fillna(df['credit_score'].median())

    df = df.drop_duplicates()

    Q1 = df['loan_amount'].quantile(0.25)
    Q3 = df['loan_amount'].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df = df[(df['loan_amount'] >= lower) & (df['loan_amount'] <= upper)]

    df['loan_amount'] = df['loan_amount'].astype(float)
    df['interest_rate'] = df['interest_rate'].astype(float)
    df['tenure_months'] = df['tenure_months'].astype(int)
    df['customer_age'] = df['customer_age'].astype(int)
    df['monthly_income'] = df['monthly_income'].astype(float)
    df['credit_score'] = df['credit_score'].astype(int)
    df['emi_amount'] = df['emi_amount'].astype(float)
    df['emi_delay_days'] = df['emi_delay_days'].astype(int)

    print("Cleaned Records:", len(df))
    return df

def feature_engineering(df):
    print("\n=== Feature Engineering ===")

    df['emi_to_income_ratio'] = df['emi_amount'] / df['monthly_income']

    def credit_score_bucket(score):
        if score < 500:
            return 'Low'
        elif score < 700:
            return 'Medium'
        else:
            return 'High'

    df['credit_score_bucket'] = df['credit_score'].apply(credit_score_bucket)

    df['risk_flag'] = (
        (df['emi_delay_days'] > 30) &
        (df['loan_status'] == 'Default')
    ).astype(int)

    print("Feature Engineering Completed")
    return df

def eda(df):
    print("\n=== Exploratory Data Analysis ===")

    default_by_loan_type = (
        df.groupby('loan_type')['loan_status']
        .value_counts(normalize=True)
        .unstack()
    )
    print("\nDefault Rate by Loan Type (%):")
    print(default_by_loan_type['Default'] * 100)

    default_by_credit_score = (
        df.groupby('credit_score_bucket')['loan_status']
        .value_counts(normalize=True)
        .unstack()
    )
    print("\nDefault Rate by Credit Score Bucket (%):")
    print(default_by_credit_score['Default'] * 100)

    high_stress = df[df['emi_to_income_ratio'] > 0.5]
    stress_default_rate = (
        high_stress['loan_status']
        .value_counts(normalize=True)
        .get('Default', 0) * 100
    )
    print(f"\nDefault Rate for High EMI Stress (>0.5): {stress_default_rate:.2f}%")

    npa_by_region = (
        df.groupby('region')['loan_status']
        .value_counts(normalize=True)
        .unstack()
    )
    print("\nRegion-wise NPA (%):")
    print(npa_by_region['Default'] * 100)

    return default_by_loan_type, default_by_credit_score, npa_by_region

def create_visualizations(df, default_by_loan_type, default_by_credit_score, npa_by_region):
    print("\n=== Data Visualization ===")

    plt.figure(figsize=(10, 6))

    plt.subplot(2, 2, 1)
    default_by_loan_type['Default'].plot(kind='bar', color='skyblue')
    plt.title("Default Rate by Loan Type")
    plt.ylabel("Default Rate")

    plt.subplot(2, 2, 2)
    default_by_credit_score['Default'].plot(kind='bar', color='lightgreen')
    plt.title("Credit Score vs Default Rate")
    plt.ylabel("Default Rate")

    plt.subplot(2, 2, 3)
    plt.hist(df['emi_to_income_ratio'], bins=20, color='orange', alpha=0.7)
    plt.axvline(0.5, linestyle='--')
    plt.title("EMI-to-Income Ratio Distribution")

    plt.subplot(2, 2, 4)
    npa_by_region['Default'].plot(kind='bar', color='red')
    plt.title("Region-wise NPA Rate")

    plt.tight_layout()
    plt.savefig("loan_risk_analysis_dashboard.png", dpi=300)
    plt.show()

    print("Dashboard saved as loan_risk_analysis_dashboard.png")

def database_integration(df):
    print("\n=== SQL Database Integration ===")

    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST", "localhost")
    db_name = os.getenv("DB_NAME", "dataanalysisproject")

    engine = create_engine(
        f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}"
    )

    df.to_sql(name="loan_risk_transactions", con=engine, if_exists="replace", index=False)
    print("Dataset loaded into MySQL successfully.")

    queries = {
        "Region-wise Default Rate": """
            SELECT region,
                   COUNT(*) AS total_loans,
                   SUM(CASE WHEN loan_status='Default' THEN 1 ELSE 0 END) AS defaults,
                   (SUM(CASE WHEN loan_status='Default' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS default_rate
            FROM loan_risk_transactions
            GROUP BY region
            ORDER BY default_rate DESC;
        """,
        "Loan-Type Risk Analysis": """
            SELECT loan_type,
                   COUNT(*) AS total_loans,
                   SUM(CASE WHEN loan_status='Default' THEN 1 ELSE 0 END) AS defaults
            FROM loan_risk_transactions
            GROUP BY loan_type;
        """,
        "High-Risk Customers": """
            SELECT customer_id, loan_type, credit_score, emi_to_income_ratio, emi_delay_days
            FROM loan_risk_transactions
            WHERE risk_flag = 1;
        """
    }

    for title, query in queries.items():
        print(f"\n{title}:")
        result = pd.read_sql(query, engine)
        print(result)

def generate_insights(df):
    print("\n=== Key Insights & Findings ===")

    unsecured_default_rate = (
        df[df['loan_type'].isin(['Personal Loan', 'Credit Card'])]['loan_status']
        .value_counts(normalize=True)
        .get('Default', 0) * 100
    )
    print("\n Unsecured loans have higher default risk.")
    print(f" -> Default rate: {unsecured_default_rate:.2f}%")

    low_score_default = (
        df[df['credit_score_bucket'] == 'Low']['loan_status']
        .value_counts(normalize=True)
        .get('Default', 0) * 100
    )
    print("\n Low credit score customers contribute most NPAs.")
    print(f" -> Default rate: {low_score_default:.2f}%")

    high_stress_default = (
        df[df['emi_to_income_ratio'] > 0.5]['loan_status']
        .value_counts(normalize=True)
        .get('Default', 0) * 100
    )
    print("\n High EMI-to-income ratio is a strong default indicator.")
    print(f" -> Default rate: {high_stress_default:.2f}%")

    high_risk_regions = (
        df.groupby('region')['loan_status']
        .value_counts(normalize=True)
        .unstack()
        .sort_values(by='Default', ascending=False)
        .head(3)
        .index.tolist()
    )
    print("\n Certain regions consistently show higher risk levels.")
    print(f" -> High-risk regions: {high_risk_regions}")

def main():
    print("Retail Lending Risk Intelligence System")
    print("=" * 50)

    df = load_loan_data()
    df = clean_data(df)
    df = feature_engineering(df)

    default_by_loan_type, default_by_credit_score, npa_by_region = eda(df)

    database_integration(df)
    generate_insights(df)
    create_visualizations(df, default_by_loan_type, default_by_credit_score, npa_by_region)

    print("\n Completed Successfully")

if __name__ == "__main__":
    main()
