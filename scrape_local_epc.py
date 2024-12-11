# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

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
                    cert_url = tr.find('th').find("a").get("href")
                    self.cert_url: str = f"https://find-energy-certificate.service.gov.uk{cert_url}"
                else: 
                    rows.append(head)
        self.rows = rows
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
    
    def scrape_current_certificate(self) -> None:     
        if self.cert_url is None:
            self.parse_table()
        self.cert_response = requests.get(self.cert_url)
        print(f"Certificate Status Code: {self.cert_response.status_code}")
        
        if self.cert_response.status_code == 200:
            self.cert_soup: BeautifulSoup = BeautifulSoup(self.cert_response.content, 'html.parser')
        else:
            return f"Failed to retrieve data, status code: {self.cert_response.status_code}"

    def parse_current_certificate(self) -> None:
        if self.cert_soup is None:
            self.scrape_current_certificate()
        
        # Get potential energy rating
        self.potential_energy_rating: str = re.findall(
            r"energy rating is [A-G]\. It has the potential to be [A-G]",
            str(self.cert_soup),
            flags=re.IGNORECASE
        )[0][-1]
        # Get potential environmental impact rating
        self.potential_environmenal_impact_rating: str = re.findall(
            r"environmental impact rating is [A-G]\. It has the potential to be [A-G]",
            str(self.cert_soup),
            flags=re.IGNORECASE
        )[0][-1]

        recommendations_section = self.cert_soup.find("h2", string="Steps you could take to save energy")
        # self.recommendations: str = ""
        for sib in recommendations_section.find_all_next():
            # where improvement tables are kept
            if sib.name=="div" and " ".join(sib.get("class")) == "govuk-body printable-area epb-recommended-improvements":
                recommendations_div = sib.find("hr")
                break
        self.recommendations_df: pd.DataFrame = pd.DataFrame({
            "recommendation": pd.Series(
                [
                    re.sub(r"Step [1-9][0-9]*:\s(.+)", r"\1", child.text)
                    for child in recommendations_div.find_all("h3")
                ],
                dtype=str,
            ),
            "min_typical_installation_cost_gbp": pd.Series(
                [
                    int(
                        re.findall(
                            r"£[1-9][0-9,]*", child.find_next("dd").text.strip()
                        )[0].replace(",", "").replace("£", "")
                    )
                    for child in recommendations_div.find_all("h3")
                ],
                dtype=int),
            "max_typical_installation_cost_gbp": pd.Series(
                [
                    int(
                        re.findall(
                            r"£[1-9][0-9,]*", child.find_next("dd").text.strip()
                        )[-1].replace(",", "").replace("£", "")
                    )
                    for child in recommendations_div.find_all("h3")
                ],
                dtype=int),
            "typical_yearly_saving": pd.Series(
                [
                    int(
                        re.findall(
                            r"£[1-9][0-9,]*", child.find_next("dd").find_next("dd").text.strip()
                        )[0].replace(",", "").replace("£", "")
                    )
                    for child in recommendations_div.find_all("h3")
                ],
                dtype=int),
        })
     
    def return_df(self):
        return self.df
    
    def return_epc(self):
        return self.epc


# scraper = EnergyCertificateScraper('5, Barbican Mews, YORK, YO10 5BZ', "YO105BZ")
scraper = EnergyCertificateScraper("1C HERIOT ROAD, HENDON, LONDON, NW4 2EG", "NW42EG")
scraper.parse_table()
avg_rating = scraper.average_rating()
print(f"Average rating: {scraper.average_rating()},\n Your rating: {scraper.return_epc()}")
scraper.scrape_current_certificate()
# print(scraper.cert_soup)
scraper.parse_current_certificate()
print(scraper.recommendations_df)