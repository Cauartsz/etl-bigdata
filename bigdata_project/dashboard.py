import pandas as pd
from db_connection import get_db
from dash import Dash, dcc, html
import plotly.express as px


#Função para buscar dados integrados do MongoDB
def load_integrated_data(country="BR"):

    try:
        db = get_db()
        data = list(db["integrated_data"].find({"country": country}))
        df = pd.DataFrame(data)
        return df
    
    except:
        print("Erro dashboard [1]")


#Gerar Dashboard
def create_dashboard(country="BR"):

    try:
        df = load_integrated_data(country)
        df = df.sort_values("year")

        app = Dash(__name__)

        app.layout = html.Div([
            html.H1(f"Impacto da COVID-19 nos Indicadores - {country}", style={"textAlign": "center"}),

            # Gráfico de casos totais x PIB
            dcc.Graph(
                figure=px.scatter(
                    df, x="total_cases", y="PIB", size="Desemprego",
                    color="Educação", hover_data=["year"],
                    title="Casos de COVID x PIB (tamanho = desemprego, cor = educação)"
                )
            ),

            # Gráfico de linha - Evolução temporal
            dcc.Graph(
                figure=px.line(
                    df, x="year", y=["total_cases", "PIB", "Desemprego"],
                    title="Tendência Temporal: Casos, PIB e Desemprego"
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

    except:
        print("Erro dashboard [2]")


    app.run_server(debug=True)


if __name__ == "__main__":
    create_dashboard("BR")
