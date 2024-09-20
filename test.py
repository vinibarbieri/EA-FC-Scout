import pandas as pd

# Função para converter valores abreviados em números
def convert_to_number(value):
    # Remove o símbolo de euro
    value = value.replace('€', '')
    # Se o valor já for numérico, retorna diretamente
    if isinstance(value, (int, float)):
        return value
    # Se o valor não for uma string, retorna NaN
    if not isinstance(value, str):
        return float('nan')
    # Verifica a unidade e converte o valor
    if 'K' in value:
        return float(value.replace('K', '')) * 1000
    elif 'M' in value:
        return float(value.replace('M', '')) * 1000000
    elif 'B' in value:
        return float(value.replace('B', '')) * 1000000000
    else:
        return float(value)  # Caso não tenha unidade, converte diretamente

# Exemplo de leitura de CSV
df = pd.read_csv('player-data-full.csv', low_memory=False)

# Supondo que a coluna com valores seja 'valor_abreviado'
df['valor_numerico'] = df['value'].apply(convert_to_number)

# Agora você pode comparar os valores normalmente
# Por exemplo, filtrando valores maiores que 1 milhão
df_filtrado = df[df['valor_numerico'] > 1000000]

# Exibindo o resultado filtrado
print(df['valor_numerico'])

