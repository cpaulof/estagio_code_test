use dev_estagio;
SELECT d.reg_ans_ as registro, nome_fantasia as nome, SUM(d.vl_saldo_inicial_-d.vl_saldo_final_) as despesa 
  FROM demonstracoes as d INNER JOIN operadoras as o ON d.reg_ans_=o.registro_operadora WHERE d.descricao_ 
  LIKE 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%' 
  AND d.data_ >= "2024-01-01"
  group by registro
  order by despesa 
  LIMIT 10