# Importa request e jsonify para manipular dados de solicitação e resposta no formato JSON
from flask import request, jsonify
# Importa o banco de dados db e o modelo User
from . import db
from .models import User
# Importa a biblioteca para gerar conteúdo com a API do Google
import google.generativeai as genai
# Importa a biblioteca jwt para geração e verificação de tokens JWT
import jwt
import datetime
# Importa wraps para criar decoradores personalizados
from functools import wraps

# Define uma chave secreta para assinar e verificar os tokens JWT
SECRET_KEY = "rafa_rsi_rafa_rsi"

# Decorador para verificar se a solicitação inclui um token válido
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Obtém o token dos cabeçalhos da solicitação
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({"message": "Token is missing"}), 403

        try:
            # Decodifica o token JWT usando a chave secreta
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # Obtém o usuário atual do banco de dados com base no ID do token
            current_user = User.query.filter_by(id=data['user_id']).first()
        except Exception as e:
            return jsonify({"message": "Token is invalid"}), 403

        # Passa o usuário atual para a função decorada
        return f(current_user, *args, **kwargs)

    return decorated

# Função para inicializar as rotas
def init_routes(app):

    # Rota para a página inicial
    @app.route('/', methods=['GET'])
    def hw():
        return "Hello World"

    # Rota de login para autenticar um usuário e gerar um token JWT
    @app.route('/login', methods=['POST'])
    def login():
        data = request.form
        if not data:
            return jsonify({"message": "No data provided"}), 400

        # Obtém o nome de usuário e senha enviados no formulário
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"message": "Username and password are required"}), 400

        # Verifica se o usuário existe no banco de dados
        user = User.query.filter_by(username=username).first()

        # Verifica as credenciais e gera um token JWT
        if user and user.password == password:
            token = jwt.encode({
                'user_id': user.id,
                'username': user.username,
                'password': user.password,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, SECRET_KEY, algorithm="HS256")
            return jsonify({"message": "Login successful", "token": token}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401

    # Rota para criar um novo usuário
    @app.route('/signup', methods=['POST'])
    def signup():
        data = request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Verifica se todos os campos obrigatórios foram preenchidos
        if not username or not email or not password:
            return jsonify({"message": "Username, email, and password are required"}), 400

        # Verifica se o usuário já existe
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return jsonify({"message": "User already exists"}), 400

        # Cria e salva o novo usuário no banco de dados
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201

    # Rota para gerar uma resposta usando a API do Google Generative AI
    @app.route('/generate_response', methods=['POST'])
    @token_required  # Verifica se o usuário está autenticado
    def generate_response(current_user):

        # Verifica se o usuário possui créditos suficientes para usar a função
        if current_user.credits <= 0:
            return jsonify({"message": "Insufficient credits"}), 403

        # Obtém o prompt da solicitação JSON
        data = request.get_json()
        prompt = data.get('prompt', 'Crie um roteiro de viagem...')

        # Configura a chave da API e o modelo de geração de conteúdo
        genai.configure(api_key="AIzaSyBWTnGlT6hdGKu50IHaYP8-MgiSlKCWS-k")
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Gera conteúdo com base no prompt
        response = model.generate_content(prompt)

        # Deduz um crédito do usuário e salva no banco de dados
        current_user.credits -= 1
        db.session.commit()

        # Retorna a resposta gerada
        return jsonify({"text": response.text}), 200

    # Rota para obter os créditos restantes do usuário autenticado
    @app.route('/get_credits', methods=['GET'])
    @token_required  # Verifica se o usuário está autenticado
    def get_credits(current_user):
        return jsonify({"credits": current_user.credits}), 200
