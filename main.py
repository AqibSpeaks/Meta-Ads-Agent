import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io

from config import DEFAULT_COUNTRIES, DEFAULT_CATEGORIES
from utils.api_client import MetaAdClient
from utils.data_processor import DataProcessor
from utils.ai_analyzer import AIAnalyzer

# Page configuration
st.set_page_config(
    page_title="Meta Ad Intelligence Bot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize classes
api_client = MetaAdClient()
data_processor = DataProcessor()
ai_analyzer = AIAnalyzer()

# Sidebar
st.sidebar.title("🔍 Search Filters")
st.sidebar.markdown("---")

# Search parameters
search_query = st.sidebar.text_input("Search Terms", placeholder="e.g., election, software, health")
selected_countries = st.sidebar.multiselect("Countries", DEFAULT_COUNTRIES, default=['US'])
selected_categories = st.sidebar.multiselect("Categories", DEFAULT_CATEGORIES, default=DEFAULT_CATEGORIES)
spend_range = st.sidebar.slider("Spending Range ($)", 0, 100000, (1000, 50000))
min_engagement = st.sidebar.slider("Minimum Engagement Rate", 0.0, 1.0, 0.01, 0.01)

# Main content
st.title("📊 Meta Ad Intelligence Bot")
st.markdown("Real-time advertising insights from Meta Ad Library")

# Search button
if st.sidebar.button("🚀 Search Ads", type="primary"):
    with st.spinner("Fetching ads data..."):
        # Fetch data
        df = api_client.search_ads(
            search_terms=search_query if search_query else None,
            countries=selected_countries,
            limit=200
        )
        
        if not df.empty:
            # Process data
            df = data_processor.categorize_ads(df)
            df = data_processor.calculate_engagement_metrics(df)
            df = data_processor.extract_landing_pages(df)
            
            # Filter by selected categories and spending
            df = df[df['category'].isin(selected_categories)]
            df = df[(df['spend_lower'] >= spend_range[0]) & (df['spend_upper'] <= spend_range[1])]
            df = df[df['engagement_rate'] >= min_engagement]
            
            st.session_state.ads_data = df
        else:
            st.error("No ads found with current filters")

# Display results
if 'ads_data' in st.session_state and not st.session_state.ads_data.empty:
    df = st.session_state.ads_data
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Ads", len(df))
    with col2:
        st.metric("Total Spend Estimate", f"${df['spend_lower'].sum():,}")
    with col3:
        st.metric("Avg Engagement Rate", f"{df['engagement_rate'].mean():.2%}")
    with col4:
        st.metric("Avg Days Active", f"{df['days_active'].mean():.1f}")
    
    # Data table
    st.subheader("📋 Ads Data")
    
    # Enhanced dataframe display
    st.dataframe(
        df[['page_name', 'category', 'countries', 'spend_lower', 
            'engagement_rate', 'days_active', 'ad_title']].head(50),
        use_container_width=True
    )
    
    # Export options
    col1, col2 = st.columns(2)
    with col1:
        csv = df.to_csv(index=False)
        st.download_button(
            "📥 Download CSV",
            csv,
            "meta_ads_data.csv",
            "text/csv"
        )
    with col2:
        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer, index=False)
        st.download_button(
            "📥 Download Excel",
            excel_buffer.getvalue(),
            "meta_ads_data.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    # Visualizations
    st.subheader("📈 Insights & Analytics")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Spending Analysis", "Engagement Metrics", "Category Distribution", "AI Insights"])
    
    with tab1:
        fig = px.bar(df, x='category', y='spend_lower', color='countries',
                    title='Spending by Category and Country')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = px.scatter(df, x='spend_lower', y='engagement_rate', color='category',
                        size='impressions_lower', hover_data=['page_name'],
                        title='Engagement vs Spending')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        fig = px.pie(df, names='category', title='Ad Distribution by Category')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.info("🤖 AI-Powered Insights")
        if st.button("Generate AI Analysis"):
            with st.spinner("Generating insights..."):
                insights = ai_analyzer.generate_insights(
                    df, 
                    category=', '.join(selected_categories),
                    country=', '.join(selected_countries)
                )
                st.markdown(insights)
    
    # Detailed view
    st.subheader("🔍 Ad Details")
    selected_ad = st.selectbox("Select an ad to view details", df['ad_title'].tolist())
    
    if selected_ad:
        ad_details = df[df['ad_title'] == selected_ad].iloc[0]
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Ad Copy:**")
            st.write(ad_details['ad_copy'][:500] + "..." if len(ad_details['ad_copy']) > 500 else ad_details['ad_copy'])
            
            st.write("**Landing Page:**")
            st.write(ad_details['landing_page'] if ad_details['landing_page'] else "Not detected")
        
        with col2:
            st.write("**Metrics:**")
            st.metric("Spent", f"${ad_details['spend_lower']:,.2f}")
            st.metric("Impressions", f"{ad_details['impressions_lower']:,.0f}")
            st.metric("Engagement Rate", f"{ad_details['engagement_rate']:.2%}")
            st.metric("Days Active", ad_details['days_active'])

else:
    st.info("👆 Use the sidebar filters to search for Meta ads. Click 'Search Ads' to get started.")
    st.image("https://via.placeholder.com/800x400?text=Meta+Ad+Intelligence+Dashboard", use_column_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Powered by Meta Ad Library API | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
