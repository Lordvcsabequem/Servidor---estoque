from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

EMAIL_REMETENTE = "seuemail@gmail.com"
SENHA_APP = "sua_senha_de_app"
EMAIL_DESTINO = "seuemail@gmail.com"

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
