# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
import joblib
from pathlib import Path
from statistics import median



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

# Request certificates
def get_certificates(address: str, postcode: str) -> list[str,str]:
    postcode.replace(" ", "")
    url = f"https://find-energy-certificate.service.gov.uk/find-a-certificate/search-by-postcode?postcode={postcode}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
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
            if head[0].lower() == address.lower():
                epc = head[1]
                cert_url = tr.find('th').find("a").get("href")
                cert_url = f"https://find-energy-certificate.service.gov.uk{cert_url}"
            else:
                rows.append(head)
    
    df = pd.DataFrame(rows, columns=['address', 'rating', 'expired'])
    
    rating_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}
    inverse_rating_map = {v: k for k, v in rating_map.items()}
        
    # Convert ratings to numerical values
    df['rating_num'] = df['rating'].map(rating_map)
    
    # Calculate the median of the numerical ratings
    median_num = df['rating_num'].median()
    
    # Convert the numerical median back to a letter
    median_rating = inverse_rating_map[median_num]
    
    df = pd.DataFrame(rows, columns=['address', 'rating', 'expired'])
    
    return epc, median_rating


# Model electricity usage
def mwh_usage(epc: str, user_inputs: list[str]):
    

    print(epc)
    new = []
    # Begin awful code
    new.extend(user_inputs[3:-1])
    new.extend([0]*11)
    if user_inputs[0] != 0:
        new[2+user_inputs[0]] = 1
    if user_inputs[1] == "Flat": new.extend([1,0,0])
    elif user_inputs[1] == "Semi-detached": new.extend([0,1,0])
    elif user_inputs[1] == "Terraced": new.extend([0,0,1])
    else: new.extend([0,0,0])
    if epc in ("D","E"): new.extend([1,0])
    elif epc in ("F","G"): new.extend([0,1])
    else: new.extend([0,0])
    if user_inputs[-1] == 1: new.extend([1])
    else: new.extend([0])
    
    # Load the model
    loaded_model = joblib.load(Path('src/model/lr_model.pkl'))
    features = list(loaded_model.feature_names_in_)
    user_data = {}
    for i in range(len(features)):
        user_data[str(features[i])] = new[i]
    user_data  = pd.DataFrame(user_data, index=[0])
    
    print(user_data, new)
    return loaded_model.predict(user_data)[0]


get_addresses("MK5 7HE")
get_certificates('4, Bushey Bartrams, Shenley Brook End, MILTON KEYNES, MK5 7HE', 'MK5 7HE')
print(mwh_usage("E", [0,"Flat",1000,1,1,1,1]))