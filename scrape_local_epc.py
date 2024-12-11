# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd

class EnergyCertificateScraper:
    def __init__(self, address, postcode):
        self.postcode = postcode.replace(" ", "%20")
        self.address = address
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
                if head[0] == self.address:
                    self.epc = head[1]
                else: 
                    rows.append(head)
        self.df = pd.DataFrame(rows, columns=['address', 'rating', 'expired'])
    
    def average_rating(self):
        
        rating_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}
        inverse_rating_map = {v: k for k, v in rating_map.items()}
        
        # Convert ratings to numerical values
        self.df['rating_num'] = self.df['rating'].map(rating_map)
        
        # Calculate the median of the numerical ratings
        median_num = self.df['rating_num'].median()
        
        # Convert the numerical median back to a letter
        median_rating = inverse_rating_map[median_num]
        
        return median_rating

    
    def return_df(self):
        return self.df
    
    def return_epc(self):
        return self.epc


scraper = EnergyCertificateScraper('5, Barbican Mews, YORK, YO10 5BZ', "YO105BZ")
scraper.parse_table()
avg_rating = scraper.average_rating()
print(f"Average rating: {scraper.average_rating()},\n Your rating: {scraper.return_epc()}")