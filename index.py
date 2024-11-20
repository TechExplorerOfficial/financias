from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permitir conexões do frontend

@app.route('/')
def home():
    return jsonify({"message": "API de Simulação Financeira Ativa!"})

# Endpoint para calcular saldo e projeções financeiras
@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        data = request.get_json()  # Recebe os dados enviados pelo frontend
        
        # Dados recebidos
        receitas = data.get('receitas', 0)
        despesas = data.get('despesas', 0)
        poupanca_mensal = data.get('poupanca_mensal', 0)  # Exemplo de meta de poupança
        meses = data.get('meses', 12)  # Período de projeção
        
        # Cálculos básicos
        saldo_atual = receitas - despesas
        poupanca_total = poupanca_mensal * meses
        saldo_futuro = saldo_atual + poupanca_total
        
        # Resposta com os resultados
        result = {
            "saldo_atual": round(saldo_atual, 2),
            "poupanca_total": round(poupanca_total, 2),
            "saldo_futuro": round(saldo_futuro, 2),
            "status": "Simulação realizada com sucesso!"
        }
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
fetch("http://127.0.0.1:5000/simulate", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    receitas: 5000,
    despesas: 3000,
    poupanca_mensal: 500,
    meses: 6
  })
})
  .then(response => response.json())
  .then(data => {
    console.log("Resultados da Simulação:", data);
    // Atualize o dashboard com os resultados
  })
  .catch(error => console.error("Erro na API:", error))
  import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados
db_config = {
    "host": "localhost",
    "user": "root",         # Substitua pelo seu usuário
    "password": "senha123", # Substitua pela sua senha
    "database": "analise_financeira"
}

# Conexão com o banco de dados
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return jsonify({"message": "API de Simulação Financeira Ativa!"})

# Endpoint para registrar usuário
@app.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        nome = data['nome']
        email = data['email']
        senha = generate_password_hash(data['senha'])
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
            (nome, email, senha)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Usuário registrado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para login
@app.route('/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        email = data['email']
        senha = data['senha']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['senha'], senha):
            return jsonify({"message": "Login bem-sucedido!", "user_id": user['id']}), 200
        else:
            return jsonify({"error": "Credenciais inválidas!"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para registrar transações
@app.route('/transacoes', methods=['POST'])
def add_transaction():
    try:
        data = request.get_json()
        usuario_id = data['usuario_id']
        descricao = data['descricao']
        valor = data['valor']
        tipo = data['tipo']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transacoes (usuario_id, descricao, valor, tipo) VALUES (%s, %s, %s, %s)",
            (usuario_id, descricao,
            