SELECT d.reg_ans, 
       d.descricao,
       SUM(COALESCE(d.vl_saldo_inicial, 0) + COALESCE(d.vl_saldo_final, 0)) AS total_despesas
FROM despesas d
WHERE d.descricao ~* 'assistência|saúde|médico|hospitalar'
  AND d.data >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY d.reg_ans, d.descricao
ORDER BY total_despesas DESC
LIMIT 10;
