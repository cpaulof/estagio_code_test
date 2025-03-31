import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

database_script = """
DROP DATABASE IF EXISTS dev_estagio;
CREATE DATABASE dev_estagio;
USE dev_estagio;

"""


ods = "REGISTRO_OPERADORA\tTexto\t6\nCNPJ\tTexto\t14\nRazao_Social\tTexto\t140\nNome_Fantasia\tTexto\t140\nModalidade\tTexto\t2\nLogradouro\tTexto\t40\nNúmero\tTexto\t20\nComplemento\tTexto\t40\nBairro\tTexto\t30\nCidade\tTexto\t30\nUF\tTexto\t2\nCEP\tTexto\t8\nDDD\tTexto\t4\nTelefone\tTexto\t20\nFax\tTexto\t20\nEndereco_eletronico\tTexto\t255\nRepresentante\tTexto\t50\nCargo_Representante\tTexto\t40\nRegiao_de_Comercializacao\tNumero\t1\nData_Registro_ANS\tData\t8"
type_mysql = {
    "texto": "VARCHAR",
    "numero": "INTEGER",
    "data": "DATE"
}
script = "CREATE TABLE operadoras(\n  ID int not null,\n{},\n  PRIMARY KEY(ID)\n);\n"
rows_script = []
for line in ods.splitlines():
    
    row_name, row_type, row_size = line.rstrip().lower().split("\t")
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

script = "CREATE TABLE demonstracoes(\n  ID int not null,\n{},\n  PRIMARY KEY(ID)\n);\n"
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

with open(os.path.join(BASE_DIR, "database.sql"), "w") as file:
    file.write(database_script)
    file.close()


