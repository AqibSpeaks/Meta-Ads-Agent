import openai
from config import OPENAI_API_KEY
import pandas as pd

class AIAnalyzer:
    def __init__(self):
        if OPENAI_API_KEY:
            openai.api_key = OPENAI_API_KEY
    
    def generate_insights(self, df: pd.DataFrame, category: str = None, country: str = None) -> str:
        """Generate AI-powered insights from ad data"""
        if df.empty:
            return "No data available for analysis."
        
        if not OPENAI_API_KEY:
            return "OpenAI API key not configured. Please add OPENAI_API_KEY to your environment variables."
        
        # Sample data for analysis
        sample_data = df.head(10).to_dict('records')
        
        prompt = f"""
        Analyze these Meta ads and provide insights:
        
        Context: Category: {category or 'All'}, Country: {country or 'Global'}
        
        Data Sample: {sample_data}
        
        Please provide:
        1. Top performing ad patterns
        2. Engagement trends
        3. Creative best practices
        4. Spending patterns
        5. Recommendations for advertisers
        
        Format response with clear sections and bullet points.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a digital marketing analyst expert in Meta advertising."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"AI analysis failed: {str(e)}"
