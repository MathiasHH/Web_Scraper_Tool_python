import requests
from bs4 import BeautifulSoup
import pandas as pd

#Importert pga timeouts 
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# URL til nettsiden du vil skrape
url = 'https://www.komplett.no/'  # Replace with your target URL

# Legger til headers i forespørselen
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

s = requests.Session()

# Problem med timeout, så gir den 5 forskjellige forsøk
retries = Retry(total=10,  # Totale forsøk
                backoff_factor=1,  # Vent 1s, 2s, 4s, 8s før vi prøver på nytt
                status_forcelist=[500, 502, 503, 504])  # Prøver på nytt med desse forskjellige statuskodene
s.mount('https://', HTTPAdapter(max_retries=retries))

# Send en GET-forespørsel for å hente sidens innhold
response = s.get(url, headers=headers, timeout=30)
print(response.text)

# Sjekk om forespørselen var vellykket
if response.status_code == 200:
    print("Hentet nettsiden!")
else:
    print(f"Mislykket forsøk på å få informasjon. Status code: {response.status_code}")

# Analyser innholdet på siden med BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Trekk ut artikkeltitler og tilhørende lenker
titles = soup.find_all('h2', class_='title')

# Initialiser lister for å inneholde titler og URL-er
article_titles = []
article_links = []

for title in titles:
    # Trekk ut teksten til tittelen
    article_titles.append(title.get_text(strip=True))
    
    # Finn <a>-taggen i <h2>-taggen og trekk ut href-attributtet
    link = title.find('a')['href'] if title.find('a') else None
    
    # Sørg for at koblingen er absolutt ved å legge til domenet om nødvendig
    if link and not link.startswith('http'):
        link = requests.compat.urljoin(url, link)
    
    # Legg til lenken til listen article_links
    article_links.append(link)

# Skriv ut ekstraherte titler og lenker
for idx, (title, link) in enumerate(zip(article_titles, article_links), 1):
    print(f"{idx}. {title} - {link}")

# La oss nå skrape prisene ved å bruke klassen "product-price-now"
prices = soup.find_all(class_='product-price-now')

# Trekk ut teksten fra kvart priselement
product_prices = [price.get_text(strip=True) for price in prices]

# Skriv ut utdragne priser
for idx, price in enumerate(product_prices, 1):
    print(f"Product {idx}: {price}")

# Lagre titler, lenker og priser i en CSV-fil
df = pd.DataFrame({
    'Article Title': article_titles,
    'Article Link': article_links,
    'Product Price': product_prices
})

# Lagre dataene i en CSV-fil
df.to_csv('products_with_prices_and_links.csv', index=False)
print("Data saved to products_with_prices_and_links.csv")
