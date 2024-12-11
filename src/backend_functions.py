# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
import joblib
from pathlib import Path
from scrape_local_epc import EnergyCertificateScraper


# Send request to server based on postcode
def get_addresses(postcode: str) -> list[str]:
    postcode.replace(" ", "")
    url = f"https://find-energy-certificate.service.gov.uk/find-a-certificate/search-by-postcode?postcode={postcode}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200: 
        return None # Error handling??!?!
    else:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='govuk-table epb-search-results')
    
    headers = [th.text.strip() for th in table.find_all('th')]
    rows = []
    for tr in table.find_all('tr'):
        head = [tr.find('th').text.strip()]
        cells = [td.text.strip() for td in tr.find_all('td')]
        head += cells
        
        if head[0] != 'Address': 
            rows.append(head)
            
    df = pd.DataFrame(rows, columns=['address', 'rating', 'expired'])
    
    return df["address"].tolist()