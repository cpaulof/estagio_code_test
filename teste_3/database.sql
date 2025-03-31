
DROP DATABASE IF EXISTS dev_estagio;
CREATE DATABASE dev_estagio;
USE dev_estagio;

CREATE TABLE operadoras(
  ID int not null,
  registro_operadora int,
  cnpj int,
  razao_social VARCHAR(140),
  nome_fantasia VARCHAR(140),
  modalidade VARCHAR(2),
  logradouro VARCHAR(40),
  número VARCHAR(20),
  complemento VARCHAR(40),
  bairro VARCHAR(30),
  cidade VARCHAR(30),
  uf VARCHAR(2),
  cep VARCHAR(8),
  ddd VARCHAR(4),
  telefone VARCHAR(20),
  fax VARCHAR(20),
  endereco_eletronico VARCHAR(255),
  representante VARCHAR(50),
  cargo_representante VARCHAR(40),
  regiao_de_comercializacao INTEGER(1),
  data_registro_ans DATE,
  PRIMARY KEY(ID)
);
CREATE TABLE demonstracoes(
  ID int not null,
  data_ date,
  reg_ans_ int,
  cd_conta_contabil_ int,
  descricao_ varchar(200),
  vl_saldo_inicial_ decimal(17, 2),
  vl_saldo_final_ decimal(17, 2),
  PRIMARY KEY(ID)
);
