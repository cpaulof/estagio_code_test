
DROP DATABASE IF EXISTS dev_estagio;
CREATE DATABASE dev_estagio;
USE dev_estagio;

CREATE TABLE operadoras(
  registro_operadora VARCHAR(200),
  cnpj VARCHAR(200),
  razao_social VARCHAR(200),
  nome_fantasia VARCHAR(200),
  modalidade VARCHAR(200),
  logradouro VARCHAR(200),
  número VARCHAR(200),
  complemento VARCHAR(200),
  bairro VARCHAR(200),
  cidade VARCHAR(200),
  uf VARCHAR(200),
  cep VARCHAR(200),
  ddd VARCHAR(200),
  telefone VARCHAR(200),
  fax VARCHAR(200),
  endereco_eletronico VARCHAR(200),
  representante VARCHAR(200),
  cargo_representante VARCHAR(200),
  regiao_de_comercializacao VARCHAR(200),
  data_registro_ans DATE
);
CREATE TABLE demonstracoes(
  data_ date,
  reg_ans_ int,
  cd_conta_contabil_ int,
  descricao_ varchar(200),
  vl_saldo_inicial_ decimal(17, 2),
  vl_saldo_final_ decimal(17, 2)
);
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/cleaned_1T2023.csv'
INTO TABLE demonstracoes
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/cleaned_1T2024.csv'
INTO TABLE demonstracoes
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/cleaned_2t2023.csv'
INTO TABLE demonstracoes
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/cleaned_2T2024.csv'
INTO TABLE demonstracoes
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/cleaned_3T2023.csv'
INTO TABLE demonstracoes
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/cleaned_3T2024.csv'
INTO TABLE demonstracoes
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/cleaned_4T2023.csv'
INTO TABLE demonstracoes
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/cleaned_4T2024.csv'
INTO TABLE demonstracoes
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/cleaned_Relatorio_cadop.csv'
INTO TABLE operadoras
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;
