import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------------------
# Page Configuration
# ----------------------------------------

st.set_page_config(
    page_title="Data Cleaning Automation",
    page_icon="📊",
    layout="wide"
)

# ----------------------------------------
# Title
# ----------------------------------------

st.title("📊 Smart Data Cleaning & Reporting Automation System")

st.markdown("""
This application automates:

✅ Data Cleaning  
✅ Missing Value Handling  
✅ Duplicate Removal  
✅ Data Visualization  
✅ Automated Reporting  
""")

# ----------------------------------------
# Upload CSV File
# ----------------------------------------

uploaded_file = st.file_uploader(
    "Upload Your CSV File",
    type=["csv"]
)

# ----------------------------------------
# Process Dataset
# ----------------------------------------

if uploaded_file is not None:

    # Read dataset
    df = pd.read_csv(uploaded_file)

    # ----------------------------------------
    # Original Dataset
    # ----------------------------------------

    st.subheader("📁 Original Dataset")

    st.dataframe(df)

    # Store original shape
    original_rows = df.shape[0]

    # ----------------------------------------
    # Missing Value Handling
    # ----------------------------------------

    numeric_columns = df.select_dtypes(include=['number']).columns

    for col in numeric_columns:
        df[col] = df[col].fillna(df[col].mean())

    object_columns = df.select_dtypes(include=['object']).columns

    for col in object_columns:
        df[col] = df[col].fillna(df[col].mode()[0])

    # ----------------------------------------
    # Remove Duplicates
    # ----------------------------------------

    duplicate_count = df.duplicated().sum()

    df = df.drop_duplicates()

    # ----------------------------------------
    # Remove Invalid Ages
    # ----------------------------------------

    if 'Age' in df.columns:
        df = df[df['Age'] > 0]

    # ----------------------------------------
    # Standardize Text
    # ----------------------------------------

    for col in object_columns:
        df[col] = df[col].astype(str).str.strip().str.title()

    # ----------------------------------------
    # Convert Date Format
    # ----------------------------------------

    if 'Purchase_Date' in df.columns:
        df['Purchase_Date'] = pd.to_datetime(
            df['Purchase_Date'],
            errors='coerce'
        )

    # ----------------------------------------
    # Cleaned Dataset
    # ----------------------------------------

    st.subheader("✅ Cleaned Dataset")

    st.dataframe(df)

    # ----------------------------------------
    # Cleaning Summary
    # ----------------------------------------

    st.subheader("📌 Cleaning Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Original Rows", original_rows)

    col2.metric("Duplicates Removed", duplicate_count)

    col3.metric("Final Rows", df.shape[0])

    # ----------------------------------------
    # Statistical Summary
    # ----------------------------------------

    st.subheader("📈 Statistical Summary")

    st.write(df.describe(include='all'))

    # ----------------------------------------
    # Visualization Section
    # ----------------------------------------

    st.subheader("📊 Data Visualization")

    # ----------------------------------------
    # Sales by City Chart
    # ----------------------------------------

    if 'City' in df.columns and 'Purchase_Amount' in df.columns:

        st.markdown("### Sales by City")

        city_sales = df.groupby('City')[
            'Purchase_Amount'
        ].sum()

        fig1, ax1 = plt.subplots(figsize=(8, 5))

        city_sales.plot(
            kind='bar',
            ax=ax1
        )

        ax1.set_xlabel("City")
        ax1.set_ylabel("Sales Amount")
        ax1.set_title("Sales by City")

        st.pyplot(fig1)

    # ----------------------------------------
    # Product Category Distribution
    # ----------------------------------------

    if 'Product_Category' in df.columns:

        st.markdown("### Product Category Distribution")

        fig2, ax2 = plt.subplots(figsize=(8, 5))

        sns.countplot(
            x='Product_Category',
            data=df,
            ax=ax2
        )

        plt.xticks(rotation=45)

        ax2.set_title("Category Distribution")

        st.pyplot(fig2)

    # ----------------------------------------
    # Purchase Amount Histogram
    # ----------------------------------------

    if 'Purchase_Amount' in df.columns:

        st.markdown("### Purchase Amount Distribution")

        fig3, ax3 = plt.subplots(figsize=(8, 5))

        ax3.hist(
            df['Purchase_Amount'],
            bins=10
        )

        ax3.set_xlabel("Purchase Amount")
        ax3.set_ylabel("Frequency")
        ax3.set_title("Purchase Amount Histogram")

        st.pyplot(fig3)

    # ----------------------------------------
    # Download Cleaned Data
    # ----------------------------------------

    cleaned_csv = df.to_csv(index=False)

    st.download_button(
        label="⬇ Download Cleaned Dataset",
        data=cleaned_csv,
        file_name='cleaned_dataset.csv',
        mime='text/csv'
    )

    # ----------------------------------------
    # Success Message
    # ----------------------------------------

    st.success(
        "🎉 Data Cleaning & Reporting Completed Successfully!"
    )

# ----------------------------------------
# Default Message
# ----------------------------------------

else:

    st.info(
        "Please upload a CSV file to begin."
    )
