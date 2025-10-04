import requests
import pandas as pd
from db_connection import get_db


def extract_covid_data(country="brazil"):

    try:
        url = f"https://disease.sh/v3/covid-19/historical/{country}?lastdays=all"
        response = requests.get(url)
        data = response.json()
        return data
    
    except:
        print("Erro de extração covid_data [1]")


def transform_covid_data(raw_data):

    try:
        timeline = raw_data["timeline"]["cases"]
        df = pd.DataFrame(list(timeline.items()), columns=["date", "cases"])
        df["date"] = pd.to_datetime(df["date"], format="%m/%d/%y")

        # Calcular crescimento diário
        df["daily_growth"] = df["cases"].diff().fillna(0)

        # Média móvel de 7 dias
        df["moving_avg_7d"] = df["daily_growth"].rolling(7).mean()
        return df
    
    except:
        print("Erro de transformação covid_data [2]")


def load_covid_data(df, country="brazil"):

    try:
        db = get_db()
        collection = db["covid_data"]
        records = df.to_dict(orient="records")
        for record in records:
            record["country"] = country
        collection.insert_many(records)
        print(f"Inserted {len(records)} records for {country}")
        
    except:
        print("Erro de carregamento covid_data [3]")


if __name__ == "__main__":
    raw = extract_covid_data("brazil")
    df = transform_covid_data(raw)
    load_covid_data(df, "brazil")
