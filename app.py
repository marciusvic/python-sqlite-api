from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///livros.db'
db = SQLAlchemy(app)

class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(255), nullable=False)
    autor = db.Column(db.String(255), nullable=False)

# Home
@app.route('/')
def home():
    return render_template('index.html')

# GetAll
@app.route('/livros', methods=['GET'])
def obter_livros():
    livros = Livro.query.all()
    livros_json = [{'id': livro.id, 'titulo': livro.titulo, 'autor': livro.autor} for livro in livros]
    return jsonify(livros_json)

# GetById
@app.route('/livro/<int:id>', methods=['GET'])
def obter_livro(id):
    livro = Livro.query.get(id)
    if livro:
        return jsonify({'id': livro.id, 'titulo': livro.titulo, 'autor': livro.autor})
    else:
        return jsonify({'erro': 'Livro não encontrado'}), 404

# Create
@app.route('/livro', methods=['POST'])
def criar_livro():
    try:
        dados_livro = request.get_json()
        novo_livro = Livro(titulo=dados_livro['titulo'], autor=dados_livro['autor'])
        db.session.add(novo_livro)
        db.session.commit()
        return jsonify({'id': novo_livro.id, 'titulo': novo_livro.titulo, 'autor': novo_livro.autor}), 201
    except Exception as e:
        return jsonify({'erro': f'Erro ao criar livro: {str(e)}'}), 500

# Update
@app.route('/livro/<int:id>', methods=['PUT'])
def atualizar_livro(id):
    try:
        livro_atualizado = request.get_json()
        livro = Livro.query.get(id)
        if livro:
            livro.titulo = livro_atualizado['titulo']
            livro.autor = livro_atualizado['autor']
            db.session.commit()
            return jsonify({'id': livro.id, 'titulo': livro.titulo, 'autor': livro.autor})
        else:
            return jsonify({'erro': 'Livro não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': f'Erro ao atualizar livro: {str(e)}'}), 500

# Delete
@app.route('/livro/<int:id>', methods=['DELETE'])
def deletar_livro(id):
    try:
        livro = Livro.query.get(id)
        if livro:
            db.session.delete(livro)
            db.session.commit()
            return jsonify({'mensagem': 'Livro removido com sucesso'})
        else:
            return jsonify({'erro': 'Livro não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': f'Erro ao deletar livro: {str(e)}'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, host='localhost', debug=True)
