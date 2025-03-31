import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

database_script = """
DROP DATABASE IF EXISTS dev_estagio;
CREATE DATABASE dev_estagio;
USE dev_estagio;

"""


ods = "REGISTRO_OPERADORA\tTexto\t100\nCNPJ\tTexto\t14\nRazao_Social\tTexto\t140\nNome_Fantasia\tTexto\t140\nModalidade\tTexto\t2\nLogradouro\tTexto\t40\nNúmero\tTexto\t20\nComplemento\tTexto\t40\nBairro\tTexto\t30\nCidade\tTexto\t30\nUF\tTexto\t2\nCEP\tTexto\t8\nDDD\tTexto\t4\nTelefone\tTexto\t20\nFax\tTexto\t20\nEndereco_eletronico\tTexto\t255\nRepresentante\tTexto\t50\nCargo_Representante\tTexto\t40\nRegiao_de_Comercializacao\tNumero\t1\nData_Registro_ANS\tData\t8"
type_mysql = {
    "texto": "VARCHAR",
    "numero": "INTEGER",
    "data": "DATE"
}
script = "CREATE TABLE operadoras(\n{}\n);\n"
rows_script = []

####### TAMANHO DOS CAMPOS INDICADO NO ODS NAO FUNCIONA!!!

for line in ods.splitlines():
    
    row_name, row_type, row_size = line.rstrip().lower().split("\t")
    if row_type!="data":
        row_type ='texto'
    row_size = 200
    size = f"({row_size})"
    if "data" in row_type: size = ""
    row_script = f"  {row_name} {type_mysql[row_type]}{size}"
    rows_script.append(row_script)
table_script = ",\n".join(rows_script)
script = script.format(table_script)
print(script)

with open(os.path.join(BASE_DIR, "tabela_operadoras.sql"), "w") as file:
    file.write(script)
    file.close()

database_script += script

##############

script = "CREATE TABLE demonstracoes(\n{}\n);\n"
rows_script = []

demonstrações_header = '"DATA";"REG_ANS";"CD_CONTA_CONTABIL";"DESCRICAO";"VL_SALDO_INICIAL";"VL_SALDO_FINAL"'.lower().split(";")
demonstrações_types = ["date", "int", "int", "varchar(200)", "decimal(17, 2)", "decimal(17, 2)"]

for row_name, row_type in zip(demonstrações_header, demonstrações_types):
    row_script = f"  {row_name.replace(" ", "_").replace('"', "")}_ {row_type}"
    rows_script.append(row_script)
table_script = ",\n".join(rows_script)
script = script.format(table_script)
print(script)

with open(os.path.join(BASE_DIR, "tabela_demonstracoes.sql"), "w") as file:
    file.write(script)
    file.close()

database_script += script
##############################3




# necessario para realizar inserts no mysql utilizando arquivos csv
SECURE_PRIVATE_DIR = r'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/'
filenames = [file for file in os.listdir(os.path.join(BASE_DIR, "downloads")) if file.startswith("cleaned_") and file.endswith(".csv")]

def create_insert_file(table, filename):
    return f'''LOAD DATA INFILE '{SECURE_PRIVATE_DIR+filename}'
INTO TABLE {table}
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\\r\\n'
IGNORE 1 ROWS;'''

for filename in filenames:
    tablename = "operadoras" if "cadop" in filename else "demonstracoes"
    text = create_insert_file(tablename, filename)
    database_script += text+"\n"




with open(os.path.join(BASE_DIR, "database.sql"), "w") as file:
    file.write(database_script)
    file.close()


