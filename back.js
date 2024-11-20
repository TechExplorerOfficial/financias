fetch("http://127.0.0.1:5000/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nome: "João Silva",
      email: "joao@email.com",
      senha: "senha123"
    })
  })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error("Erro:", error));
    fetch("http://127.0.0.1:5000/transacoes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          usuario_id: 1,
          descricao: "Compra de mercado",
          valor: -200.50,
          tipo: "despesa"
        })
      })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error("Erro:", error));
        fetch("http://127.0.0.1:5000/transacoes/1")
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error("Erro:", error));
              