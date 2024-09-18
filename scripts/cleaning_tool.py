"""
Esse script é responsável por auxiliar na limpeza dos dataframes.
"""
import pandas as pd
from pandas import DataFrame
import ast
  
def limpar_dados_silver(data: DataFrame) -> DataFrame:
    df = data.copy()
    df = df.drop_duplicates()
    df = df.drop(columns=['TIPO_ANUNCIO', 'FINAL_DE_PLACA', 'CATEGORIA']).reset_index(drop=True)

    df.OPCIONAIS = df.OPCIONAIS.apply(lambda x: ast.literal_eval(x))
    idx_list = [idx for idx, linha in enumerate(df['OPCIONAIS']) if len(linha) < 1]     
    df = df.drop(index=idx_list) # removendo os registros que não tem 'opcionais'
    df['qtd_opcionais'] = [len(opc) for opc in df.OPCIONAIS]

    df = df.dropna().reset_index(drop=True)
    df.ANO = df.ANO.str.replace('ou anterior', '').str.strip().astype(int)
    df.PORTAS = df.PORTAS.str.replace('portas', '').str.strip().astype(int)
    df.POTENCIA_DO_MOTOR = df.POTENCIA_DO_MOTOR.astype('category')

    df.columns = df.columns.str.lower()

    return df
