#Scraping Data through urls
import requests
from bs4 import BeautifulSoup
import pandas as pd

input_file_path = 'input.xlsx'
df = pd.read_excel(input_file_path)

for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']

    response = requests.get(url)

    if response.status_code == 200:#Request success
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text.strip() 
        if soup.find('title'):
            article_text = ""
        else:
            'No Title Found'
        
        article_text_element = soup.find('div', class_='td-post-content tagdiv-type')  #finding body texts
        if article_text_element:
            article_text = article_text_element.get_text().strip()

        # Saving the files
        output_file_path = f'{url_id}.txt'
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(f'{title}\n\n')
            file.write(f'\n{article_text}')

        print(f'Data extracted from {url} and saved to {output_file_path}')
    else:
        print(f'Failed to retrieve data from {url}')

