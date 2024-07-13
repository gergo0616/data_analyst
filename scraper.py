import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_tripadvisor(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    restaurants = soup.find_all('div', class_='_1llCuDZj')
    
    data = []
    for restaurant in restaurants:
        name = restaurant.find('a', class_='_15_ydu6b').text.strip()
        try:
            rating = float(restaurant.find('svg', class_='UctUV d H0')['aria-label'].split()[0])
        except:
            rating = None
        try:
            reviews = int(restaurant.find('span', class_='_10Iv7dOs').text.split()[0].replace(',', ''))
        except:
            reviews = None
        
        data.append({'name': name, 'rating': rating, 'reviews': reviews})
    
    return pd.DataFrame(data)