from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)
CORS(app)

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
SENHA_APP = os.getenv("SENHA_APP")
EMAIL_DESTINO = os.getenv("EMAIL_DESTINO")

@app.route("/enviar", methods=["POST"])
def enviar_email():
    data = request.json
    tipo = data.get("tipo")
    produtos = data.get("produtos")
    responsavel = data.get("responsavel")
    motivo = data.get("motivo")

    corpo = f"""
    Tipo: {tipo}
    Responsável: {responsavel}
    """

    if motivo:
        corpo += f"Motivo da perda: {motivo}\n"

    corpo += "\nProdutos:\n" + produtos

    mensagem = MIMEText(corpo)
    mensagem["Subject"] = f"{tipo} de Estoque"
    mensagem["From"] = EMAIL_REMETENTE
    mensagem["To"] = EMAIL_DESTINO

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_REMETENTE, SENHA_APP)
            smtp.send_message(mensagem)
        return jsonify({"status": "sucesso"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
