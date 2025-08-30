import pandas as pd
import re
from typing import Dict, List

class DataProcessor:
    @staticmethod
    def categorize_ads(df: pd.DataFrame) -> pd.DataFrame:
        """Categorize ads based on content analysis"""
        categories = {
            'POLITICS': ['election', 'vote', 'politic', 'government', 'senate', 'congress'],
            'ECOMMERCE': ['sale', 'buy', 'shop', 'discount', 'offer', '% off'],
            'HEALTH': ['health', 'medical', 'doctor', 'hospital', 'wellness'],
            'TECH': ['tech', 'software', 'app', 'digital', 'AI', 'machine learning'],
            'EDUCATION': ['education', 'learn', 'course', 'university', 'school']
        }
        
        def detect_category(text):
            text = str(text).lower()
            for category, keywords in categories.items():
                if any(keyword in text for keyword in keywords):
                    return category
            return 'OTHER'
        
        df['category'] = df['ad_copy'].apply(detect_category)
        return df
    
    @staticmethod
    def calculate_engagement_metrics(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate estimated engagement metrics"""
        # These are estimates since exact engagement data isn't available via API
        df['estimated_likes'] = (df['impressions_lower'] * 0.02).astype(int)
        df['estimated_shares'] = (df['impressions_lower'] * 0.005).astype(int)
        df['estimated_comments'] = (df['impressions_lower'] * 0.003).astype(int)
        
        df['engagement_rate'] = (
            (df['estimated_likes'] + df['estimated_shares'] + df['estimated_comments']) / 
            df['impressions_lower'].replace(0, 1)
        ).round(4)
        
        return df
    
    @staticmethod
    def extract_landing_pages(df: pd.DataFrame) -> pd.DataFrame:
        """Extract landing pages from ad copy"""
        def extract_url(text):
            urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(text))
            return urls[0] if urls else ''
        
        df['landing_page'] = df['ad_copy'].apply(extract_url)
        return df
