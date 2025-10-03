import requests
import pandas as pd
from db_connection import get_db


def extract_worldbank_data(indicator="NY.GDP.MKTP.CD", country="BR", start=2015, end=2022):
    
    try:
        url = f"http://api.worldbank.org/v2/country/{country}/indicator/{indicator}?date={start}:{end}&format=json"
        response = requests.get(url)
        data = response.json()[1]  # os dados ficam no índice 1
        return data
    
    except:
        print("Erro de extração worldbank_data [1]")


def transform_worldbank_data(raw_data, indicator_name):

    try:
        df = pd.DataFrame(raw_data)
        df = df[["date", "value"]]
        df.rename(columns={"value": indicator_name}, inplace=True)
        df["date"] = pd.to_datetime(df["date"], format="%Y")
        df.sort_values("date", inplace=True)
        return df
    
    except:
        print("Erro de transformação worldbank_data [2]")


def load_worldbank_data(df, indicator_name, country="BR"):

    try:
        db = get_db()
        collection = db["socioeconomic_data"]
        records = df.to_dict(orient="records")
        for record in records:
            record["country"] = country
            record["indicator"] = indicator_name
        collection.insert_many(records)
        print(f"Inserted {len(records)} records for {indicator_name} in {country}")

    except:
        print("Erro de carregamento worldbank_data [3]")


if __name__ == "__main__":
    indicators = {
        "PIB": "NY.GDP.MKTP.CD",
        "Desemprego": "SL.UEM.TOTL.ZS",
        "Educação": "SE.ENR.PRSC.FM.ZS"
    }

    for name, code in indicators.items():
        raw = extract_worldbank_data(code, "BR", 2015, 2022)
        df = transform_worldbank_data(raw, name)
        load_worldbank_data(df, name, "BR")
