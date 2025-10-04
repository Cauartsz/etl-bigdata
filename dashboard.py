import pandas as pd
from db_connection import get_db
from dash import Dash, dcc, html
import plotly.express as px

# Função para buscar dados integrados do MongoDB (mais robusta)
def load_integrated_data(country="BR"):
    """
    Carrega os dados integrados do MongoDB.
    Retorna um DataFrame do Pandas ou um DataFrame vazio em caso de erro.
    """
    try:
        db = get_db()
        # Verifica se a coleção existe antes de tentar acessá-la
        if "integrated_data" not in db.list_collection_names():
            print("Aviso: A coleção 'integrated_data' não foi encontrada no banco de dados.")
            return pd.DataFrame() # Retorna um DataFrame vazio
            
        data = list(db["integrated_data"].find({"country": country}))
        
        if not data:
            print(f"Aviso: Nenhum dado encontrado para o país '{country}' na coleção 'integrated_data'.")
            return pd.DataFrame()

        df = pd.DataFrame(data)
        return df
    
    except Exception as e:
        print(f"Erro ao conectar ou carregar dados do MongoDB: {e}")
        return pd.DataFrame()


# Gerar Dashboard
def create_dashboard(country="BR"):
    """
    Cria e executa o dashboard com os dados integrados.
    """
    df = load_integrated_data(country)
    
    # INICIALIZAÇÃO DO APP MOVIDA PARA FORA DO BLOCO TRY
    # Isso garante que a variável 'app' sempre exista.
    app = Dash(__name__)

    # VERIFICAÇÃO SE O DATAFRAME NÃO ESTÁ VAZIO ANTES DE CRIAR OS GRÁFICOS
    if not df.empty:
        try:
            # Garante que as colunas necessárias existem
            required_columns = ["year", "total_cases", "PIB", "Desemprego", "Educação"]
            if not all(col in df.columns for col in required_columns):
                 raise ValueError("Uma ou mais colunas necessárias para os gráficos não foram encontradas no DataFrame.")

            df = df.sort_values("year")

            app.layout = html.Div([
                html.H1(f"Impacto da COVID-19 nos Indicadores - {country}", style={"textAlign": "center"}),

                # Gráfico de dispersão: Casos de COVID vs PIB
                dcc.Graph(
                    figure=px.scatter(
                        df, x="total_cases", y="PIB", size="Desemprego",
                        color="Educação", hover_name="year",
                        title="Casos de COVID x PIB (Tamanho = Desemprego, Cor = Educação)"
                    )
                ),

                # Gráfico de linha - Evolução temporal
                dcc.Graph(
                    figure=px.line(
                        df, x="year", y=["total_cases", "PIB", "Desemprego"],
                        title="Tendência Temporal: Casos, PIB e Desemprego",
                        markers=True # Adiciona marcadores para melhor visualização
                    )
                ),

                # Gráfico de barras - Educação
                dcc.Graph(
                    figure=px.bar(
                        df, x="year", y="Educação",
                        title="Evolução da Educação (%)"
                    )
                ),
            ])

        except Exception as e:
            print(f"Erro ao criar os gráficos do dashboard: {e}")
            # Layout de erro se algo falhar durante a criação do gráfico
            app.layout = html.Div([
                html.H1("Erro ao Gerar o Dashboard", style={"textAlign": "center", "color": "red"}),
                html.P(f"Ocorreu um erro durante a criação dos gráficos. Verifique os logs do terminal para mais detalhes."),
                html.P(f"Detalhes do erro: {e}")
            ])
    else:
        # LAYOUT ALTERNATIVO PARA QUANDO NÃO HÁ DADOS
        app.layout = html.Div([
            html.H1("Dados Não Encontrados", style={"textAlign": "center"}),
            html.P("Não foi possível carregar os dados para gerar o dashboard.", style={"textAlign": "center"}),
            html.P("Por favor, execute os scripts de ETL na seguinte ordem e verifique se não há erros:", style={"textAlign": "center"}),
            html.Code("1. python etl_covid.py", style={"display": "block", "textAlign": "center"}),
            html.Code("2. python etl_worldbank.py", style={"display": "block", "textAlign": "center"}),
            html.Code("3. python etl_integration.py", style={"display": "block", "textAlign": "center"}),
        ])

    # Executa o servidor do Dash
    app.run(debug=True)


if __name__ == "__main__":
    create_dashboard("BR")