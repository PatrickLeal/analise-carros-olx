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
        bar_metric:Literal['pctg', 'mean']='pctg',
        hue:ColumnName|None= None, color:str=None, feature_target:ColumnName=None,
        figsize=(24, 12)) -> None:
        """Função para facilitar na exibição de gráficos.

        Args:
            data (DataFrame): dataset usado
            features (List[ColumnName] | ColumnsList): coluna ou lista com colunas a serem exibidas
            kde (bool, optional): _description_. Defaults to False.
            kind (Literal[&#39;histplot&#39;, &#39;boxplot&#39;, &#39;barplot&#39;], optional): Qual tipo de gráfico será exibido. Defaults to 'histplot'.
            bar_metric (Literal[&#39;pctg&#39;, &#39;mean&#39;], optional): _description_. Defaults to 'pctg'.
            hue (ColumnName | None, optional): _description_. Defaults to None.
            color (str, optional): _description_. Defaults to None.
            feature_target (ColumnName, optional): _description_. Defaults to None.
            figsize (tuple, optional): _description_. Defaults to (24, 12).
        """
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
                                sns.boxplot(data=data, x=feature, ax=ax, color=color, hue=hue)
                                ax.ticklabel_format(style='plain', axis='x')
                        elif kind == 'barplot':
                                __plot_barplot(data=data, feature=feature, ax=ax, color=color,
                                               bar_metric=bar_metric, feature_target=feature_target)
                        else:   
                                sns.histplot(data=data, x=feature, kde=kde, ax=ax,
                                             color=color, hue=hue)
                                ax.ticklabel_format(style='plain', axis='x')
                                
                        ax.set_title(feature)  
                        ax.set_xlabel('')

                # removendo axes não usados
                if qtd_features < len(axes.flat):
                        for j in range(qtd_features, len(axes.flat)):
                                fig.delaxes(axes.flat[j])

                plt.tight_layout()

        except Exception as e:
                raise(e)

def __plot_barplot(data, feature, ax, bar_metric, feature_target=None, color=None,
                   bar_label_dist:float=.5, bar_orientation:Literal['y', 'x']='y',
                   ) -> None:
        
        if bar_metric == 'mean':
              if feature_target == None:
                      msg = "É necessário preencher a variável que será usada para medir a média."
                      raise Exception(msg)
              data_grouped = data.groupby([feature])[[feature_target]].mean().reset_index()
              data_grouped[feature_target] = round(data_grouped[feature_target], 2)
              data_grouped = data_grouped.sort_values(by=feature_target, ascending=True)
              ax.barh(y=data_grouped[feature], width=data_grouped[feature_target]) 

              for index, value in enumerate(data_grouped[feature_target]):
                # Ajustando a posição do texto
                ax.text(value + value * .05, index, f'{value:_.0f} R$', va='center', fontsize=15) 
        else:
                data_grouped = data.groupby([feature])[[feature]].count()\
                                .rename(columns={feature: 'count'}).reset_index()
                data_grouped['pctg'] = data_grouped['count'] / data_grouped['count'].sum() * 100
                data_grouped = data_grouped.sort_values(by='pctg', ascending=True)
                if bar_orientation == 'y':
                        ax.barh(y=data_grouped[feature], width=data_grouped['pctg'], color=color)
                else:
                        ax.barh(x=data_grouped[feature], width=data_grouped['pctg'], color=color)

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
        """Função para auxiliar na compreensão dos Outiliers das variáveis

        Args:
            data (DataFrame): dados a serem usados
            features (ColumnName | ColumnsList): colunas que devem ser verificadas.
        """

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