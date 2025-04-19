# streamlit


import streamlit as st
import pandas as pd
import boto3
import io
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Load AWS credentials from .env
load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
RAW_BUCKET = "restaurant-reviews-raw-data"

st.set_page_config(page_title="🍽️ Restaurant Upload", layout="wide")
st.title("🍽️ Upload Your Restaurant Reviews!")
st.write("Upload one or more restaurant CSVs to compare analytics or explore individually.")

# File uploader to accept multiple files
uploaded_files = st.file_uploader("Upload your CSV files", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    dfs = []
    restaurant_names = []

    for uploaded_file in uploaded_files:
        try:
            df = pd.read_csv(uploaded_file)
            restaurant_name = os.path.splitext(uploaded_file.name)[0]
            df['__source__'] = restaurant_name  # add source column
            dfs.append(df)
            restaurant_names.append(restaurant_name)

            # Push to S3
            s3 = boto3.client("s3",
                              region_name=AWS_REGION,
                              aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
            s3.put_object(Bucket=RAW_BUCKET, Key=uploaded_file.name, Body=uploaded_file.getvalue())

        except Exception as e:
            st.error(f"❌ Error reading {uploaded_file.name}: {e}")

    if dfs:
        all_data = pd.concat(dfs, ignore_index=True)
        all_data['Rating'] = pd.to_numeric(all_data['Rating'], errors='coerce')
        if 'Time' in all_data.columns:
            all_data['Time'] = pd.to_datetime(all_data['Time'], errors='coerce')

        view_option = st.radio("How would you like to view analytics?", ["View Single Restaurant", "Compare Multiple Restaurants"])

        if view_option == "View Single Restaurant":
            selected_restaurant = st.selectbox("Select a restaurant:", restaurant_names)
            df = all_data[all_data['__source__'] == selected_restaurant]
        else:
            df = all_data

        st.subheader("Preview (first 3 rows)")
        st.dataframe(df.head(3))

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("⭐ Star Rating Distribution")
            fig1, ax1 = plt.subplots(figsize=(6.5, 4.5))
            df['Rating'].dropna().astype(int).value_counts().sort_index().plot(kind='bar', ax=ax1, color='skyblue')
            ax1.set_xlabel("Star Rating")
            ax1.set_ylabel("Frequency")
            ax1.set_title("Star Ratings")
            ax1.tick_params(axis='x', labelrotation=0)
            st.pyplot(fig1)

        with col2:
            if 'Restaurant' in df.columns:
                st.subheader("🌟 Avg Rating per Restaurant")
                avg_rating = df.groupby("Restaurant")["Rating"].mean().sort_values()
                fig2, ax2 = plt.subplots(figsize=(6.5, 4.5))
                sns.barplot(x=avg_rating.values, y=avg_rating.index, palette="viridis", ax=ax2)
                ax2.set_xlabel("Avg Rating")
                ax2.set_ylabel("Restaurant")
                ax2.set_title("Average Rating")
                st.pyplot(fig2)

        # Third row: Reviews over time
        if 'Time' in df.columns and not df['Time'].isna().all():
            st.subheader("📈 Review Volume Over Time")
            time_series = df.groupby(df['Time'].dt.date).size()
            fig3, ax3 = plt.subplots(figsize=(13, 4.5))
            time_series.plot(kind='line', marker='o', ax=ax3)
            ax3.set_xlabel("Date")
            ax3.set_ylabel("Review Count")
            ax3.set_title("Review Volume by Date")
            ax3.grid(True)
            st.pyplot(fig3)

       # Most Popular Reviewer
        if 'Metadata' in df.columns:
            df['Followers'] = df['Metadata'].str.extract(r'(\\d+)\\s*Followers').astype(float)
            if not df['Followers'].isna().all():
                most_popular = df.loc[df['Followers'].idxmax()]
                st.subheader("📱 Most Popular Reviewer")
                st.write(f"**Reviewer:** {most_popular['Reviewer']}")
                st.write(f"**Followers:** {int(most_popular['Followers'])}")
                st.write("**Their Review:**")
                st.write(most_popular['Review'])

        st.subheader("🏅 Highest vs. 💔 Lowest Rated Restaurants")
        ratings = df.groupby("Restaurant")["Rating"].mean()
        col5, col6 = st.columns(2)
        with col5:
            st.metric("🏆 Highest Rated", ratings.idxmax(), round(ratings.max(), 2))
        with col6:
            st.metric("💔 Lowest Rated", ratings.idxmin(), round(ratings.min(), 2))

else:
    st.info("Please upload one or more CSV files to begin.")
