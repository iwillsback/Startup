# Importa a função create_app do módulo app, que inicializa a aplicação
from app import create_app

# Cria uma instância da aplicação Flask usando a função create_app
app = create_app()

# Define o comportamento ao executar o arquivo diretamente (modo script)
if __name__ == '__main__':
    # Inicia a aplicação em modo de depuração
    app.run(debug=True)
