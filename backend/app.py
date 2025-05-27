from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
import random
from flask import Flask
from pymongo import MongoClient


app = Flask(__name__)

@app.route('/')
def hello():
    return "Bem-vindo á API de análise de casos criminais "

if __name__ == '__main__':
    app.run(debug=True)





# MongoDb Connection

MONGO_URI =  "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client["meu_banco"]
colecao = db["meus_dados"]

@dataclass
class Vitima:
    etnia: str
    idade: int

@dataclass
class Caso:
    data_do_caso:str
    tipo_do_caso:str
    localizacao:str
    vitima:Vitima

    def to_dict(self):
        return {
            "data_do_caso": self.data_do_caso,
            "tipo_do_caso":self.tipo_do_caso,
            "localizacao:":self.localizacao,
            "vitima":asdict(self.vitima)

        }
    
def gerar_dados_aleatorios(n=20):
    tipo_casos = ["Furto", "Assalto", "Violência doméstica", "Tráfico"]
    locais = ["Centro", "Bairro A", "Bairro B", "Zona rural"]
    etnias = ["Branca", "Preta", "Parda", "Indígena", "Amarela"]
    casos = []
    base_date = datetime.now()
    for i in range(n):
        data_caso = (base_date - timedelta(days=random.randint(0, 365))).date().isoformat()
        caso = Caso(
            data_do_caso = data_caso,
            tipo_do_caso = random.choice(tipo_casos),
            localizacao = random.choice(locais),
            vitima = Vitima(
                etnia=random.choice(etnias),
                idade=random.randint(1,90)
            )
        )
        casos.append(caso.to_dict())
        return casos
    
if __name__ == "__main__":
    if colecao.count_documents({}) == 0:
        print("Inserindo dados inicias...")
        dados_iniciais = gerar_dados_aleatorios(20)
        colecao.insert_many(dados_iniciais)
    app.run(debug=True)
    