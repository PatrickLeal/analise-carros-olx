import pandas as pd
from pandas import DataFrame
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List

type ColumnName = str

def make_eda_plots(
        data:DataFrame, features:List[ColumnName], histplot:bool=True,
        kde:bool=False, hue:ColumnName|None= None, color:str=None,
        figsize=(24, 12)) -> None:

        try:
                qtd_features = len(features)
                qtd_rows = qtd_features // 3 + (qtd_features % 3 > 0)

                fig, axes = plt.subplots(qtd_rows, 3, figsize=figsize)

                for i, feature in enumerate(features):
                        row = i // 3
                        col = i % 3

                        ax = axes[row, col] if qtd_rows > 1 else axes[col]

                        sns.histplot(data=data, x=feature, kde=kde, ax=ax,)

                        ax.set_title(feature)  
                        plt.ticklabel_format(style='plain', axis='x')
                        ax.set_xlabel('')

                if qtd_features < len(axes.flat):
                        for j in range(qtd_features, len(axes.flat)):
                                fig.delaxes(axes.flat[j])
                plt.tight_layout()
        except Exception as e:
                raise(e)