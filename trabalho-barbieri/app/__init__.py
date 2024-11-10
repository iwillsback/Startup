# Importa a classe Flask para criar a aplicação, SQLAlchemy para o ORM (gerenciamento do banco de dados),
# e CORS para permitir o compartilhamento de recursos entre origens diferentes
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Importa a classe Config, que contém as configurações da aplicação
from config import Config

# Instancia o objeto db como uma instância do SQLAlchemy, que será usada para criar e gerenciar o banco de dados
db = SQLAlchemy()

# Função de fábrica da aplicação, que cria e configura uma instância do Flask
def create_app():
    # Cria a instância da aplicação Flask
    app = Flask(__name__)

    # Carrega as configurações da classe Config para a aplicação
    app.config.from_object(Config)

    # Habilita o CORS para a aplicação, permitindo que ela compartilhe recursos com origens diferentes
    CORS(app)

    # Inicializa o banco de dados com a aplicação
    db.init_app(app)

    # Cria um contexto de aplicação temporário para configurar rotas e o banco de dados
    with app.app_context():
        # Importa e inicializa as rotas, registrando-as na aplicação
        from .routes import init_routes
        init_routes(app)

        # Cria todas as tabelas definidas nos modelos, se elas ainda não existirem
        db.create_all()

    # Retorna a aplicação configurada
    return app
