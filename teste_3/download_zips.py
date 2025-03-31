import requests
import os
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin


#extrai os links que terminam com .zip de cada url 2023, 2024
def get_zip_files(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    zip_files = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.endswith('.zip'):
            zip_files.append({
                'name': link.text.strip(),
                'url': urljoin(url, href)
            })
    return zip_files

def download_file(url, filename):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    block_size = 8192
    
    print(f"Downloading {filename}...")
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=block_size):
            if chunk:
                file.write(chunk)
    print(f"Downloaded {filename}")

# baixa todos os .zip de 2023 e 2024, salva-os na pasta downloads dentro de teste_3
def main():
    base_url = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis"
    years = ['2023', '2024']
    os.makedirs('downloads', exist_ok=True)
    
    for year in years:
        year_url = f"{base_url}/{year}/"
        print(f"\nProcessing {year} folder...")
        
        zip_files = get_zip_files(year_url)
        
        for zip_file in zip_files:
            filename = os.path.join('downloads', zip_file['name'])
            try:
                download_file(zip_file['url'], filename)
                time.sleep(10)
            except Exception as e:
                print(f"Error downloading {zip_file['name']}: {str(e)}")

if __name__ == "__main__":
    main() 