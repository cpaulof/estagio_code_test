import tabula
import pandas as pd
import unicodedata
import re
from PyPDF2 import PdfReader
# import csv
import os
BASE_DIR =  os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
import sys
sys.path.append(ROOT_DIR)
from utils import create_zip



# Limpeza inicial do texto, para evitar erros de codificação
def clean_text(text):
    if isinstance(text, str):
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
        text = ' '.join(text.split())
    return text

# Extração da legenda do PDF (como todas as legendas são iguais, 
# utilizei somente a página 4)
# utiliza regex para encontrar a legenda e transforma em
#  dicionário as combinações de SIGLA: DESCRIÇÃO
def extract_legend_from_pdf():
    try:
        reader = PdfReader(os.path.join(ROOT_DIR, "teste_1", "Anexo I.pdf"))
        
        page = reader.pages[4]
        text = page.extract_text()
        legend_match = re.search(r'Legenda:(.*?)(?=\n\n|\Z)', text, re.DOTALL)
        
        if legend_match:
            legend_text = legend_match.group(1).strip()
            legend_dict = {}
            for line in legend_text.split('\n'):
                if ':' in line:
                    abbr, desc = line.split(':', 1)
                    legend_dict[abbr.strip()] = desc.strip()
            return legend_dict
    except Exception as e:
        print(f"Error extracting legend: {str(e)}")
    return {}

# Substitui as siglas pela descrição correspondente
def replace_abbreviations(text, legend_dict):
    if not isinstance(text, str):
        return text
    sorted_abbrs = sorted(legend_dict.keys(), key=len, reverse=True)
    
    for abbr in sorted_abbrs:
        text = re.sub(r'\b' + re.escape(abbr) + r'\b', legend_dict[abbr], text)
    return text

# utiliza a biblioteca tabula para extrair as tabelas do PDF
def extract_table_from_pdf():
    try:
        legend_dict = extract_legend_from_pdf()
        tables = tabula.read_pdf(
            os.path.join(ROOT_DIR, "teste_1", "Anexo I.pdf"),
            pages="all",
            guess=False,
            multiple_tables=True,
            lattice=True,
            stream=True,   
            encoding='charmap'
        )
        
        if not tables:
            print("No tables found in the PDF!")
            return
        
        print(f"Found {len(tables)} tables in the PDF")
        
        
        # combina todas as tabelas em um único DataFrame e em seguida salva em csv
        combined_df = pd.concat(tables, ignore_index=True)
        combined_df = combined_df.dropna(how='all')
        combined_df = combined_df.dropna(axis=1, how='all')

        for column in combined_df.columns:
            combined_df[column] = combined_df[column].apply(clean_text)
            combined_df[column] = combined_df[column].apply(lambda x: replace_abbreviations(x, legend_dict))
        
        combined_df = combined_df.reset_index(drop=True)
        output_file = os.path.join(BASE_DIR, "rol_procedimentos.csv")

        combined_df.to_csv(output_file, index=False, encoding='utf-8')

        zip_filename = create_zip([output_file], os.path.join(BASE_DIR, "Teste_Paulo_Fernando.zip"))
        
        print(f"saved: {output_file}")
        print(f"length: {len(combined_df)}")
        print(f"Zip file created: {zip_filename}")
        
        print(combined_df.head())
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    extract_table_from_pdf() 