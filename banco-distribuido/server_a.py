from flask import Flask, request, jsonify, render_template
import requests
import json
import os

app = Flask(__name__)

PORTA = 5000
ARQUIVO = "dados_a.json"
SERVIDOR_B = "http://localhost:5001"


def carregar():
    if not os.path.exists(ARQUIVO):
        return []

    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()

            if not conteudo:
                return []

            return json.loads(conteudo)

    except json.JSONDecodeError:
        print("⚠ JSON corrompido, recriando banco vazio")
        return []


def salvar():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(banco, f, ensure_ascii=False, indent=4)


banco = carregar()

def sincronizar():
    try:
        resposta = requests.get(f"{SERVIDOR_B}/produtos", timeout=3)

        if resposta.status_code == 200:

            produtos_remotos = resposta.json()

            alterou = False

            for produto in produtos_remotos:

                existe = any(
                    p["id"] == produto["id"]
                    for p in banco
                )

                if not existe:
                    banco.append(produto)
                    alterou = True

            if alterou:
                salvar()

            print("Sincronização concluída")

    except:
        print("Outro servidor indisponível")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ping")
def ping():
    return "ok"


@app.route("/produtos", methods=["GET"])
def listar():
    return jsonify(banco)


@app.route("/produtos", methods=["POST"])
def cadastrar():
    dados = request.json

    if not any(p["id"] == dados["id"] for p in banco):
        banco.append(dados)
        salvar()

    try:
        requests.post(
            f"{SERVIDOR_B}/replicar",
            json=dados,
            timeout=2
        )
    except:
        print("Servidor B indisponível")

    return jsonify({"msg": "Produto salvo"})


@app.route("/replicar", methods=["POST"])
def replicar():
    dados = request.json

    if not any(p["id"] == dados["id"] for p in banco):
        banco.append(dados)
        salvar()

    return jsonify({"msg": "Replicado"})

@app.route("/produtos/<id>", methods=["DELETE"])
def deletar(id):

    global banco

    banco = [p for p in banco if p["id"] != id]
    salvar()

    try:
        requests.delete(f"{SERVIDOR_B}/replicar/{id}", timeout=2)
    except:
        pass

    return jsonify({"msg": "Removido"})

@app.route("/replicar/<id>", methods=["DELETE"])
def replicar_delete(id):

    global banco

    banco = [p for p in banco if p["id"] != id]
    salvar()

    return jsonify({"msg": "replicado delete"})

@app.route("/produtos/<id>", methods=["PUT"])
def editar(id):

    dados = request.json

    for p in banco:
        if p["id"] == id:
            p["nome"] = dados["nome"]
            p["preco"] = dados["preco"]

    salvar()

    try:
        requests.put(
            f"{SERVIDOR_B}/replicar/{id}",
            json=dados,
            timeout=2
        )
    except:
        pass

    return jsonify({"msg": "Atualizado"})

@app.route("/replicar/<id>", methods=["PUT"])
def replicar_update(id):

    dados = request.json

    for p in banco:
        if p["id"] == id:
            p["nome"] = dados["nome"]
            p["preco"] = dados["preco"]

    salvar()

    return jsonify({"msg": "replicado update"})


if __name__ == "__main__":
    sincronizar()
    app.run(port=5000)