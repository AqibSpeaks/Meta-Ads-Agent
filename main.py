import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import io

# Page configuration
st.set_page_config(
    page_title="Meta Ad Intelligence Bot",
    page_icon="📊",
    layout="wide"
)

# Generate demo data function
def generate_demo_data():
    categories = ['ECOMMERCE', 'POLITICS', 'HEALTH', 'TECH', 'EDUCATION']
    countries = ['US', 'GB', 'CA', 'AU', 'DE', 'FR']
    pages = ['Amazon', 'Nike', 'Apple', 'Local Business', 'NonProfit Org']
    
    ecommerce_ads = [
        "Summer Sale! Get 50% OFF everything. Limited time offer! 🛍️",
        "Free shipping on all orders over $50. Shop now! 🚚",
        "New collection just dropped. Be the first to shop! 👕",
        "Black Friday deals live! Up to 70% OFF selected items. 🎁"
    ]
    
    politics_ads = [
        "Vote for change. Join our movement for a better future. 🗳️",
        "Election day is coming. Make your voice heard! 🇺🇸",
        "Support our campaign for education reform. 📚",
        "Stand with us for climate action now! 🌍"
    ]
    
    data = []
    for i in range(200):
        category = random.choice(categories)
        
        if category == 'ECOMMERCE':
            ad_copy = random.choice(ecommerce_ads)
        elif category == 'POLITICS':
            ad_copy = random.choice(politics_ads)
        else:
            ad_copy = f"Discover our new {category.lower()} services. Quality guaranteed! ✅"
        
        spend = random.randint(100, 50000)
        impressions = random.randint(1000, 1000000)
        
        ad = {
            'ad_id': f'ad_{i:04d}',
            'ad_copy': ad_copy,
            'ad_title': f"{category} Campaign {i}",
            'page_name': random.choice(pages),
            'spend': spend,
            'impressions': impressions,
            'estimated_likes': int(impressions * 0.02),
            'estimated_shares': int(impressions * 0.005),
            'estimated_comments': int(impressions * 0.003),
            'engagement_rate': round(random.uniform(0.01, 0.05), 4),
            'currency': 'USD',
            'countries': random.choice(countries),
            'category': category,
            'days_active': random.randint(1, 90),
            'landing_page': f"https://example.com/{category.lower()}/offer{i}",
            'start_date': (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d')
        }
        data.append(ad)
    
    return pd.DataFrame(data)

# Main app
st.title("📊 Meta Ad Intelligence Bot")
st.markdown("Advertising insights and analytics dashboard")

# Sidebar filters
st.sidebar.title("🔍 Search Filters")
st.sidebar.markdown("---")

search_query = st.sidebar.text_input("Search Terms", "")
selected_countries = st.sidebar.multiselect("Countries", ['US', 'GB', 'CA', 'AU', 'DE', 'FR'], default=['US'])
selected_categories = st.sidebar.multiselect("Categories", ['ECOMMERCE', 'POLITICS', 'HEALTH', 'TECH', 'EDUCATION'], 
                                           default=['ECOMMERCE', 'POLITICS'])

spend_min, spend_max = st.sidebar.slider("Spending Range ($)", 0, 50000, (1000, 20000))
min_engagement = st.sidebar.slider("Min Engagement Rate", 0.0, 0.1, 0.01, 0.001)

# Generate data
if 'ads_data' not in st.session_state:
    st.session_state.ads_data = generate_demo_data()

df = st.session_state.ads_data

# Apply filters
filtered_df = df[
    (df['countries'].isin(selected_countries)) &
    (df['category'].isin(selected_categories)) &
    (df['spend'] >= spend_min) &
    (df['spend'] <= spend_max) &
    (df['engagement_rate'] >= min_engagement)
]

if search_query:
    filtered_df = filtered_df[
        filtered_df['ad_copy'].str.contains(search_query, case=False) |
        filtered_df['ad_title'].str.contains(search_query, case=False)
    ]

# Display metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Ads", len(filtered_df))
with col2:
    st.metric("Total Spend", f"${filtered_df['spend'].sum():,}")
with col3:
    st.metric("Avg Engagement", f"{filtered_df['engagement_rate'].mean():.2%}")
with col4:
    st.metric("Avg Days Active", f"{filtered_df['days_active'].mean():.1f}")

# Data table
st.subheader("📋 Ads Data")
st.dataframe(
    filtered_df[['page_name', 'category', 'countries', 'spend', 
                'engagement_rate', 'days_active', 'ad_title']].head(50),
    use_container_width=True,
    height=400
)

# Export buttons
csv = filtered_df.to_csv(index=False)
st.download_button(
    "📥 Download CSV",
    csv,
    "meta_ads_data.csv",
    "text/csv"
)

# Visualizations
st.subheader("📈 Analytics")

tab1, tab2, tab3 = st.tabs(["Spending Analysis", "Engagement Metrics", "Category Distribution"])

with tab1:
    chart_data = filtered_df.groupby(['category', 'countries'])['spend'].mean().reset_index()
    st.bar_chart(chart_data, x='category', y='spend', color='countries')

with tab2:
    scatter_data = filtered_df[['spend', 'engagement_rate', 'category']]
    st.scatter_chart(scatter_data, x='spend', y='engagement_rate', color='category')

with tab3:
    category_counts = filtered_df['category'].value_counts()
    st.plotly_chart({
        'data': [{
            'type': 'pie',
            'labels': category_counts.index.tolist(),
            'values': category_counts.values.tolist()
        }]
    }, use_container_width=True)

# AI Insights (simulated)
st.subheader("🤖 AI-Powered Insights")
if st.button("Generate Insights"):
    with st.spinner("Analyzing data..."):
        # Simulated AI analysis
        insights = f"""
        ## 📊 Insights for {', '.join(selected_categories)} in {', '.join(selected_countries)}
        
        **Top Performing Categories:**
        - {filtered_df.groupby('category')['engagement_rate'].mean().idxmax()} has highest engagement
        - Average spend: ${filtered_df['spend'].mean():.0f}
        
        **Engagement Trends:**
        - Overall engagement rate: {filtered_df['engagement_rate'].mean():.2%}
        - Best performing ads have shorter copy (<100 characters)
        
        **Recommendations:**
        - Focus on {filtered_df.groupby('category')['spend'].sum().idxmax()} for maximum impact
        - Test different ad formats for better engagement
        """
        st.markdown(insights)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>📊 Advertising Analytics Dashboard | Demo Mode</p>
    <p><small>Add Meta API credentials for real data access</small></p>
</div>
""", unsafe_allow_html=True)
