1. Ainda é preciso criar um usuário, senha e cluster de
banco de dados no site do MongoDB (Tentei na minha conta
mas não funcionou)
2. Conectar com o MongoDB Compass para ver se funcionou
corretamente, depois colocar a URL de conexão no .env do
Código do projeto.

Fazendo isso, já dá pa rodas os seguintes comandos no
terminal do código:

- python etl_covid.py

- python etl_worldbank.py

- python etl_integration.py

- python dashboard.py

- Acesse no navegador: http://127.0.0.1:8050
📊 O que você verá
- Gráfico de dispersão: Casos de COVID vs PIB (bolha = taxa de desemprego, cor = educação)
- Linha temporal: Evolução de Casos x PIB x Desemprego por ano
- Barras: Indicador de Educação ao longo do tempo


Se tudo funcionou corretamente, então beleza. Caso não, há
outros passos que podemos dar para continuar o projeto:

- Gerar arquivos CSV caso precise;
- Fazer o dashboard a partir de outra ferramenta como
POWER BI
- Implementar o uso de Docker
