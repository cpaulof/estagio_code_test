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
