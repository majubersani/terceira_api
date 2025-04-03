from flask import Flask, jsonify, request
from flask_pydantic_spec import FlaskPydanticSpec, Request, Response
from pydantic import BaseModel
from datetime import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

spec = FlaskPydanticSpec('flask',
                         title='terceira API de Validade',
                         version='1.0.0')
spec.register(app)

class ProdutoEntrada(BaseModel):
    data_fabricacao: str
    validade: int
    unidade: str

class ProdutoSaida(BaseModel):
    validade_fornecida: str
    data_validade: str

@app.route('/validade_produto', methods=['POST'])
def calcular_validade():
    """
    API para Cálculo de Validade de Produtos

    ## Endpoint:
    `GET /data/quantidade

    ## Parâmetros:
    - ** Data no formato "DD/MM/YYYY" ** (exemplo: "20/11/2025").
    - ** Qualquer outro formato resultará em erro. **

    ## Resposta (JSON):
    {
        "validade_fornecida": "0"
        "data_validade": "%Y/%m/%d"
        "unidade": "0"
        }

    ## Erros possíveis:
    - Se não estiver no formato correto(data), retorna erro ** 400 **
    Bad Request
    "json"

    :return: "validade_fornecida": 0
            "data_validade": "%Y/%m/%d"
    """

    dados = request.get_json()


    data_fabricacao = datetime.strptime('data_fabricacao', "%Y/%m/%d")
    validade = dados['validade']
    unidade = dados['unidade'].lower()


    if unidade == "dias":
        data_validade = data_fabricacao + relativedelta(days=validade)
    elif unidade == "semanas":
        data_validade = data_fabricacao + relativedelta(weeks=validade)
    elif unidade == "meses":
        data_validade = data_fabricacao + relativedelta(months=validade)
    elif unidade == "anos":
        data_validade = data_fabricacao + relativedelta(years=validade)
    else:
        return jsonify({"Use dias, semanas, meses ou anos."}), 400

    resposta = {
        "validade_fornecida": f"{validade} {unidade}",
        "data_validade": data_validade.strftime("%Y/%m/%d")
    }
    return jsonify(resposta)

if __name__ == '__main__':
    app.run(debug=True)

