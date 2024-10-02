import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL til nettsiden du vil skrape
url = 'https://www.komplett.no/'  # Replace with your target URL

# Legger til headers i forespørselen
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Send en GET-forespørsel for å hente sidens innhold
response = requests.get(url, headers=headers)

# Sjekk om forespørselen var vellykket
if response.status_code == 200:
    print("Successfully fetched the webpage!")
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
