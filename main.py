import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="Meta Ad Intelligence Bot",
    page_icon="📊",
    layout="wide"
)

# Generate demo data
def generate_demo_data():
    data = []
    for i in range(100):
        ad = {
            'ad_id': f'ad_{i:04d}',
            'ad_copy': f"Discover our amazing offer {i}! Limited time only. 🎯",
            'page_name': random.choice(['Amazon', 'Nike', 'Apple', 'Local Business']),
            'spend': random.randint(100, 10000),
            'impressions': random.randint(1000, 100000),
            'engagement_rate': round(random.uniform(0.01, 0.05), 4),
            'country': random.choice(['US', 'GB', 'CA', 'AU']),
            'category': random.choice(['ECOMMERCE', 'POLITICS', 'HEALTH']),
            'days_active': random.randint(1, 90),
            'landing_page': f"https://example.com/offer{i}"
        }
        data.append(ad)
    return pd.DataFrame(data)

# Main app
st.title("📊 Meta Ad Intelligence Bot")
st.write("Advertising analytics dashboard - Demo Mode")

# Generate data
df = generate_demo_data()

# Display metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Ads", len(df))
with col2:
    st.metric("Total Spend", f"${df['spend'].sum():,}")
with col3:
    st.metric("Avg Engagement", f"{df['engagement_rate'].mean():.2%}")

# Show data
st.subheader("Ad Data")
st.dataframe(df)

# Simple chart
st.subheader("Spending by Category")
category_spend = df.groupby('category')['spend'].sum()
st.bar_chart(category_spend)

# Export button
csv = df.to_csv(index=False)
st.download_button(
    "📥 Download CSV",
    csv,
    "ads_data.csv",
    "text/csv"
)

st.success("✅ App is working! You can now add more features.")
