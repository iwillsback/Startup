from flask import Flask, request, jsonify, render_template
import openai
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roteiros.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo para armazenar roteiros
class Roteiro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_deficiencia = db.Column(db.String(50), nullable=False)
    destino = db.Column(db.String(100), nullable=False)
    datas = db.Column(db.String(100), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)


# Criação do banco de dados
with app.app_context():
    db.create_all()

# Rota para a página inicial
@app.route('/')
def home():
    return render_template('index.html')

# Rota para gerar roteiro
@app.route('/gerar_roteiro', methods=['POST'])
def gerar_roteiro():
    data = request.json
    tipo_deficiencia = data.get('tipo_deficiencia')
    destino = data.get('destino')
    datas = data.get('datas')

    prompt = (
        f"Crie um roteiro de viagem acessível para uma pessoa com deficiência {tipo_deficiencia}. "
        f"O destino é {destino} e as datas da viagem são {datas}. "
        "Inclua sugestões de atividades, restaurantes e dicas de acessibilidade."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    roteiro = response['choices'][0]['message']['content']
    return jsonify({'roteiro': roteiro})

# Rota para salvar roteiro
@app.route('/salvar_roteiro', methods=['POST'])
def salvar_roteiro():
    data = request.json
    novo_roteiro = Roteiro(
        tipo_deficiencia=data.get('tipo_deficiencia'),
        destino=data.get('destino'),
        datas=data.get('datas'),
        conteudo=data.get('conteudo')
    )
    db.session.add(novo_roteiro)
    db.session.commit()
    return jsonify({'message': 'Roteiro salvo com sucesso!'}), 201

if __name__ == '__main__':
    app.run(debug=True)
