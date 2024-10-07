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

    df.OPCIONAIS = df.OPCIONAIS.str.replace('[', '').str.replace(']', '').str.replace("'", "")
    idx_list = [idx for idx, linha in enumerate(df['OPCIONAIS']) if len(linha) < 1]     
    df = df.drop(index=idx_list) # removendo os registros que não tem 'opcionais'
    df['qtd_opcionais'] = [len(opc.split(',')) for opc in df.OPCIONAIS]

    df = df.dropna().reset_index(drop=True)
    df.ANO = df.ANO.replace({'1950 ou anterior': 1950}).astype(int)
    df.PORTAS = df.PORTAS.str.replace('portas', '').str.strip().astype(int)
    df.POTENCIA_DO_MOTOR = df.POTENCIA_DO_MOTOR.astype('category')
    df.CEP = df.CEP.astype('category')
    df.PRECO_BRL = df.PRECO_BRL.astype(int)

    df.columns = df.columns.str.lower()

    return df
