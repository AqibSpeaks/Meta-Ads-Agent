import requests
import pandas as pd
from config import META_ACCESS_TOKEN, ADS_ENDPOINT
import time

class MetaAdClient:
    def __init__(self, access_token=META_ACCESS_TOKEN):
        self.access_token = access_token
        self.session = requests.Session()
    
    def search_ads(self, search_terms=None, countries=None, categories=None, limit=100):
        """Search ads in Meta Ad Library"""
        params = {
            'access_token': self.access_token,
            'ad_reached_countries': countries or ['US'],
            'ad_type': 'POLITICAL_AND_ISSUE_ADS',
            'fields': ','.join([
                'id', 'ad_creative_body', 'ad_creative_link_title',
                'ad_creative_link_description', 'ad_creative_link_caption',
                'ad_snapshot_url', 'page_name', 'currency',
                'spend', 'impressions', 'demographic_distribution',
                'region_distribution', 'ad_delivery_start_time',
                'ad_delivery_stop_time', 'ad_archive_id'
            ]),
            'limit': min(limit, 100)
        }
        
        if search_terms:
            params['search_terms'] = search_terms
        if categories:
            params['ad_active_status'] = 'ACTIVE'
        
        try:
            response = self.session.get(ADS_ENDPOINT, params=params)
            response.raise_for_status()
            data = response.json().get('data', [])
            return self._process_response(data)
        except Exception as e:
            print(f"API Error: {e}")
            return pd.DataFrame()
    
    def _process_response(self, data):
        """Process API response into structured format"""
        processed_data = []
        
        for ad in data:
            processed_ad = {
                'ad_id': ad.get('id'),
                'ad_copy': ad.get('ad_creative_body', ''),
                'ad_title': ad.get('ad_creative_link_title', ''),
                'ad_description': ad.get('ad_creative_link_description', ''),
                'page_name': ad.get('page_name', ''),
                'spend_lower': ad.get('spend', {}).get('lower_bound', 0),
                'spend_upper': ad.get('spend', {}).get('upper_bound', 0),
                'impressions_lower': ad.get('impressions', {}).get('lower_bound', 0),
                'impressions_upper': ad.get('impressions', {}).get('upper_bound', 0),
                'currency': ad.get('currency', 'USD'),
                'ad_snapshot_url': ad.get('ad_snapshot_url', ''),
                'start_time': ad.get('ad_delivery_start_time', ''),
                'end_time': ad.get('ad_delivery_stop_time', ''),
                'countries': ', '.join(ad.get('ad_reached_countries', [])),
                'demographics': str(ad.get('demographic_distribution', [])),
                'regions': str(ad.get('region_distribution', []))
            }
            
            # Calculate days active
            if processed_ad['start_time']:
                start_date = pd.to_datetime(processed_ad['start_time'])
                end_date = pd.to_datetime(processed_ad['end_time']) if processed_ad['end_time'] else pd.Timestamp.now()
                processed_ad['days_active'] = (end_date - start_date).days
            
            processed_data.append(processed_ad)
        
        return pd.DataFrame(processed_data)
