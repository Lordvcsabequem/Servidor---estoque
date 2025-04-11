<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Formulário de Teste com API</title>
  <style>
    body { font-family: sans-serif; background: #f4f4f4; padding: 20px; }
    form, pre { background: #fff; padding: 20px; border-radius: 8px; max-width: 600px; margin: auto; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
    input, textarea, button, select { width: 100%; margin-top: 10px; padding: 10px; border-radius: 5px; border: 1px solid #ccc; }
    button { background-color: #333; color: white; font-weight: bold; cursor: pointer; }
    pre { white-space: pre-wrap; margin-top: 20px; }
  </style>
</head>
<body>
  <form id="form-api">
    <h2>Teste com API Flask</h2>

    <label>Tipo:</label>
    <select id="tipo">
      <option value="Saída">Saída</option>
      <option value="Perda">Perda</option>
    </select>

    <label>Produtos:</label>
    <textarea id="produtos" rows="4">Água 10
Coca 5</textarea>

    <label>Responsável:</label>
    <input type="text" id="responsavel" value="Weberth">

    <label>Motivo (se for perda):</label>
    <input type="text" id="motivo">

    <button type="submit">Testar Envio</button>
  </form>

  <pre id="resposta">Resposta aparecerá aqui...</pre>

  <script>
    const form = document.getElementById("form-api");
    const resposta = document.getElementById("resposta");

    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const dados = {
        tipo: document.getElementById("tipo").value,
        produtos: document.getElementById("produtos").value,
        responsavel: document.getElementById("responsavel").value,
        motivo: document.getElementById("motivo").value,
      };

      resposta.textContent = "Enviando...";

      try {
        const r = await fetch("https://servidor-estoque.onrender.com/enviar", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(dados)
        });

        const res = await r.json();
        resposta.textContent = JSON.stringify(res, null, 2);
      } catch (err) {
        resposta.textContent = "Erro: " + err;
      }
    });
  </script>
</body>
</html>
