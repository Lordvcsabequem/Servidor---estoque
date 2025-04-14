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

def montar_tabela_html(lista_produtos):
    linhas = lista_produtos.strip().split("\n")
    tabela = "<table border='1' cellpadding='6' cellspacing='0'><tr><th>Produto</th><th>Quantidade</th></tr>"
    for linha in linhas:
        if linha.strip() == "":
            continue
        partes = linha.rsplit(" ", 1)
        produto = partes[0]
        quantidade = partes[1] if len(partes) > 1 else ""
        tabela += f"<tr><td>{produto}</td><td>{quantidade}</td></tr>"
    tabela += "</table>"
    return tabela

@app.route("/enviar", methods=["POST"])
def enviar():
    try:
        data = request.get_json(force=True)

        tipo = data.get("tipo")
        produtos = data.get("produtos", "")
        responsavel = data.get("responsavel")
        motivo = data.get("motivo")

        tabela_produtos = montar_tabela_html(produtos)

        corpo_html = f"""
        <h3>{tipo} de Estoque</h3>
        <p><strong>Responsável:</strong> {responsavel}</p>
        {"<p><strong>Motivo:</strong> " + motivo + "</p>" if motivo else ""}
        <p><strong>Produtos:</strong></p>
        {tabela_produtos}
        """

        msg = MIMEText(corpo_html, "html")
        msg["Subject"] = f"{tipo} de Estoque"
        msg["From"] = EMAIL_REMETENTE
        msg["To"] = EMAIL_DESTINO

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_REMETENTE, SENHA_APP)
            smtp.send_message(msg)

        return jsonify({"mensagem": "E-mail enviado com sucesso!"}), 200

    except Exception as e:
        print("Erro:", e)
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
