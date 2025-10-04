No nosso projeto, estamos desenvolvendo a partir dos seguintes temas disponibilizados na atividade:

APIs:
➢ COVID-19 API (https://disease.sh/docs/ ) — dados diários da pandemia por país

➢ World Bank API (https://datahelpdesk.worldbank.org/) — indicadores
socioeconômicos (PIB, desemprego, educação, etc.)

Temas para os 5 ETLs:
1. Dados Diários de COVID-19 por País:
Extração dos dados oficiais, transformação para calcular taxas de crescimento, médias móveis e tendências.

3. Indicadores Socioeconômicos por País:
Extração e transformação de indicado.

Observações importantes para dar continuidade ao código a partir de agora (03/10/25 - 15:03):

1. Ainda é preciso criar um usuário, senha e cluster de
banco de dados no site do MongoDB (Tentei na minha conta
mas não funcionou)

2. Conectar com o MongoDB Compass para ver se funcionou
corretamente, depois colocar a URL de conexão no .env do
Código do projeto.

3. Fazendo isso, já dá pa rodas os seguintes comandos no
terminal do código:

1. - python etl_covid.py

2. - python etl_worldbank.py

3. - python etl_integration.py

4. - python dashboard.py

5. - Acesse no navegador: http://127.0.0.1:8050
- 📊 O que você verá:
- Gráfico de dispersão: Casos de COVID vs PIB (bolha = taxa de desemprego, cor = educação)
- Linha temporal: Evolução de Casos x PIB x Desemprego por ano
- Barras: Indicador de Educação ao longo do tempo


Se tudo funcionou corretamente, então beleza. Caso não, há
outros passos que podemos dar para continuar o projeto:

- Gerar arquivos CSV caso precise;
- Fazer o dashboard a partir de outra ferramenta como
POWER BI
- Implementar o uso de Docker
