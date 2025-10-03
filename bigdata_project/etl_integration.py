import pandas as pd
from db_connection import get_db


def integrate_data(country="BR"):

    try:
        db = get_db()
        
        #1. Buscar COVID (agregado por ano)
        covid_data = list(db["covid_data"].find({"country": "brazil"}))
        covid_df = pd.DataFrame(covid_data)
        covid_df["date"] = pd.to_datetime(covid_df["date"])
        covid_df["year"] = covid_df["date"].dt.year
        
        #Agregar: soma do crescimento diário por ano
        covid_yearly = covid_df.groupby("year")["daily_growth"].sum().reset_index()
        covid_yearly.rename(columns={"daily_growth": "total_cases"}, inplace=True)
        
        #2. Buscar Socioeconômicos
        socio_data = list(db["socioeconomic_data"].find({"country": country}))
        socio_df = pd.DataFrame(socio_data)
        socio_df["year"] = pd.to_datetime(socio_df["date"]).dt.year
        
        socio_pivot = socio_df.pivot_table(
            index="year", 
            columns="indicator", 
            values="value", 
            aggfunc="first"
        ).reset_index()
        
        #3. Juntar COVID + Socioeconômico
        merged = pd.merge(covid_yearly, socio_pivot, on="year", how="inner")
        
        #4. Salvar no Mongo
        collection = db["integrated_data"]
        records = merged.to_dict(orient="records")
        collection.delete_many({"country": country})  #evitar duplicados
        for record in records:
            record["country"] = country
        collection.insert_many(records)
        
        print("✅ Dados integrados salvos com sucesso!")
        print(merged)

    except:
        print("Erro na integração [1]")


if __name__ == "__main__":
    integrate_data("BR")
