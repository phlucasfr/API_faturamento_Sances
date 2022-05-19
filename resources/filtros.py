# Metodo para padronizar os valores recebidos
def normalize_path_params(venda_id=None,
                          dia_min=1,
                          dia_max=31,
                          mes_min=1,
                          mes_max=12,
                          ano_min=0,
                          ano_max=3000,
                          limit=50,
                          offset=0, **dados):
    if venda_id:
        return {
            'dia_min': dia_min,
            'dia_max': dia_max,
            'mes_min': mes_min,
            'mes_max': mes_max,
            'ano_min': ano_min,
            'ano_max': ano_max,
            'venda_id': venda_id,
            'limit': limit,
            'offset': offset}
    return {
        'dia_min': dia_min,
        'dia_max': dia_max,
        'mes_min': mes_min,
        'mes_max': mes_max,
        'ano_min': ano_min,
        'ano_max': ano_max,
        'limit': limit,
        'offset': offset}

# Cursores sql
consulta_sem_vendas = "SELECT * FROM faturamentos \
WHERE (dia >= %s and dia <= %s) \
and (mes >= %s and mes <= %s) \
and (ano >= %s and ano <= %s) \
LIMIT %s OFFSET %s"

consulta_com_vendas = "SELECT * FROM faturamentos \
WHERE (dia >= %s and dia <= %s) \
and (mes >= %s and mes <= %s) \
and (ano >= %s and ano <= %s) \
and vendas = %s LIMIT %s OFFSET %s"
