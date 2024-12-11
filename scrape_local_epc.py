# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd

class EnergyCertificateScraper:
    def __init__(self, postcode):
        self.postcode = postcode.replace(" ", "%20")
        self.url = f"https://find-energy-certificate.service.gov.uk/find-a-certificate/search-by-postcode?postcode={self.postcode}"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        self.response = requests.get(self.url, headers=self.headers)
        print(f"Status Code: {self.response.status_code}")
        
        if self.response.status_code == 200:
            self.soup = BeautifulSoup(self.response.content, 'html.parser')
            self.table = self.soup.find('table', class_='govuk-table epb-search-results')
        else:
            return f"Failed to retrieve data, status code: {self.response.status_code}"
    
    def parse_table(self):
        headers = [th.text.strip() for th in self.table.find_all('th')]
        rows = []
        for tr in self.table.find_all('tr'):
            head = [tr.find('th').text.strip()]
            cells = [td.text.strip() for td in tr.find_all('td')]
            head += cells
            if head[0] != 'Address':
                rows.append(head)
        self.df = pd.DataFrame(rows, columns=['address', 'rating', 'expired'])
    
    def remove_address(self, address):
        self.adress = address
        self.df = self.df[self.df['address'] != address]
        
        # Get your data
        user = self.df[self.df['address'] == address]
        return user
        if not user.empty:
            self.epc =  user['rating'].values[0]
            print(f"Rating: {self.epc}")
            return self.epc
    
    def return_df(self):
        return self.df

postcode = "YO105BZ"
scraper = EnergyCertificateScraper(postcode)
scraper.parse_table()

scraper.remove_address("1, Barbican Mews, YORK, YO10 5BZ")

