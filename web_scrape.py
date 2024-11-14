import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function to get the HTML content
def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as err:
        print(f'HTTP error occurred: {err}')
        return None
    except Exception as err:
        print(f'Other error occurred: {err}')
        return None

# Function to parse the HTML content
def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = []
    headlines = soup.find_all('h2')
    for headline in headlines:
        data.append(headline.text.strip())
    return data

# Function to save data to a CSV file
def save_to_csv(data, filename='data.csv'):
    df = pd.DataFrame(data, columns=['Headline'])
    df.to_csv(filename, index=False)
    print(f'Data saved to {filename}')

# Main function to scrape multiple pages
def scrape_website(base_url, num_pages):
    all_data = []
    for page in range(1, num_pages + 1):
        url = f'{base_url}?page={page}'
        print(f'Scraping page {page}: {url}')
        html = get_html(url)
        if html:
            page_data = parse_html(html)
            all_data.extend(page_data)
        time.sleep(1)
    return all_data

if __name__ == '__main__':
    base_url = 'https://www.example.url/'
    num_pages = 5  # Number of pages to scrape
    data = scrape_website(base_url, num_pages)
    if data:
        save_to_csv(data)