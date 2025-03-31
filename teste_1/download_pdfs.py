import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import os
BASE_DIR =  os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append(os.path.dirname(BASE_DIR))
from utils import create_zip


def read_url():
    with open(os.path.join(BASE_DIR, 'url.txt'), 'r') as file:
        return file.read().strip()

def find_pdf_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all links
    links = soup.find_all('a')
    
    # Find PDF links containing "Anexo I" and "Anexo II"
    anexo_links = {}
    for link in links:
        href = link.get('href')
        if href:
            if 'Anexo I.' in link.text:
                anexo_links['Anexo I'] = urljoin(url, href)
            elif 'Anexo II' in link.text:
                anexo_links['Anexo II'] = urljoin(url, href)
    
    return anexo_links

def download_pdf(url, filename):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
    return filename

# def create_zip(pdf_files):
#     zip_filename = 'anexos.zip'
#     with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
#         for pdf_file in pdf_files:
#             zipf.write(pdf_file)
#     return zip_filename

def main():
    try:
        # Read URL from file
        url = read_url()
        print(f"URL read successfully: {url}")
        
        # Find PDF links
        pdf_links = find_pdf_links(url)
        if not pdf_links:
            print("No PDF links found!")
            return
        
        print("Found PDF links:")
        for name, link in pdf_links.items():
            print(f"{name}: {link}")
        
        # Download PDFs
        downloaded_files = []
        for name, link in pdf_links.items():
            filename = os.path.join(BASE_DIR, f"{name}.pdf")
            print(f"Downloading {name}...")
            downloaded_files.append(download_pdf(link, filename))
            print(f"Downloaded {filename}")
        
        # Create zip file
        zip_filename = create_zip(downloaded_files, os.path.join(BASE_DIR, "anexos.zip"))
        print(f"Created zip file: {zip_filename}")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 