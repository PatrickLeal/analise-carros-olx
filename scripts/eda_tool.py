import pandas as pd
from pandas import DataFrame
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List, Literal

type ColumnName = str
type ColumnsList = List[ColumnName]

def make_eda_plots(
        data:DataFrame, features:List[ColumnName] | ColumnsList, kde:bool=False,
        kind:Literal['histplot', 'boxplot', 'barplot']='histplot',
        hue:ColumnName|None= None, color:str=None,
        figsize=(24, 12)) -> None:

        try:
                qtd_features = len(features)
                qtd_rows = qtd_features // 3 + (qtd_features % 3 > 0)

                fig, axes = plt.subplots(qtd_rows, 3, figsize=figsize)

                for i, feature in enumerate(features):
                        row = i // 3
                        col = i % 3

                        ax = axes[row, col] if qtd_rows > 1 else axes[col]

                        if kind == 'boxplot':
                                # PLOT BOXPLOT
                                sns.boxplot(data=data, x=feature, ax=ax, color=color)
                                ax.ticklabel_format(style='plain', axis='x')
                        elif kind == 'barplot':
                                __plot_barplot(data=data, feature=feature, ax=ax)
                        else:   
                                sns.histplot(data=data, x=feature, kde=kde, ax=ax,)
                                ax.ticklabel_format(style='plain', axis='x')
                                
                        ax.set_title(feature)  
                        ax.set_xlabel('')

                if qtd_features < len(axes.flat):
                        for j in range(qtd_features, len(axes.flat)):
                                fig.delaxes(axes.flat[j])
                plt.tight_layout()

        except Exception as e:
                raise(e)

def __plot_barplot(data, feature, ax, color=None,
                   bar_label_dist:float=.5, bar_orientation:Literal['y', 'x']='y') -> None:
        data_grouped = data.groupby([feature])[[feature]].count()\
                           .rename(columns={feature: 'count'}).reset_index()
        data_grouped['pctg'] = data_grouped['count'] / data_grouped['count'].sum() * 100
        data_grouped = data_grouped.sort_values(by='pctg', ascending=True)

        ax.barh(bar_orientation=data_grouped[feature], width=data_grouped['pctg'])

        if pd.api.types.is_numeric_dtype(data_grouped[feature]):
                ax.invert_yaxis()
                                
        for index, value in enumerate(data_grouped['pctg']): # rotulando as barras
                ax.text(value + bar_label_dist, index, f'{value:.1f}%', va='center', fontsize=15)

        ax.ticklabel_format(style='plain', axis='x')
        ax.set_yticks(ticks=range(data_grouped[feature].nunique()),
                        labels=data_grouped[feature].tolist(), fontsize=15)
        ax.get_xaxis().set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.grid(False)
        ax.set_title(feature)
        
def check_outliers(data: DataFrame, features: ColumnName|ColumnsList) -> None:
        outlier_counts = {}
        outlier_indexes = {}
        total_outliers = 0

        for feature in features:
                Q1 = data[feature].quantile(0.25)
                Q3 = data[feature].quantile(0.75)
                
                IQR = Q3 - Q1
                
                lower = Q1 - 1.5 * IQR
                upper = Q3 + 1.5 * IQR
                
                feature_outliers = data[(data[feature] < lower) | (data[feature] > upper)]
                outlier_indexes[feature] = feature_outliers.index.tolist()
                outlier_count = len(feature_outliers)
                outlier_counts[feature] = outlier_count
                total_outliers += outlier_count

        print(f'Há {total_outliers} outliers no dataset.\n')
        print(f'Quantidade e porcentagem outliers por feature: \n')
        for feature, count in outlier_counts.items():
                print(f'{feature}: {count} ({round(count/len(data)*100, 2)})%')