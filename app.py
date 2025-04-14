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
def enviar():
    data = request.get_json(force=True)
    print("Dados recebidos:", data)

    tipo = data.get("tipo")
    produtos = data.get("produtos")
    responsavel = data.get("responsavel")
    motivo = data.get("motivo")

    corpo = f"""
    Tipo: {tipo}
    Produtos:
    {produtos}
    Responsável: {responsavel}
    """
    if motivo:
        corpo += f"\nMotivo da perda: {motivo}"

    try:
        msg = MIMEText(corpo)
        msg["Subject"] = "Registro de Saída ou Perda"
        msg["From"] = EMAIL_REMETENTE
        msg["To"] = EMAIL_DESTINO

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_REMETENTE, SENHA_APP)
            server.sendmail(EMAIL_REMETENTE, EMAIL_DESTINO, msg.as_string())

        return jsonify({"mensagem": "Dados enviados por e-mail com sucesso!"}), 200

    except Exception as e:
        print("Erro ao enviar e-mail:", e)
        return jsonify({"erro": "Falha ao enviar o e-mail."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
