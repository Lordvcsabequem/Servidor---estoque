from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/enviar", methods=["POST"])
def teste():
    data = request.get_json(force=True)
    print("Dados recebidos:", data)
    return jsonify({"mensagem": "Dados recebidos com sucesso!", "dados": data}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
