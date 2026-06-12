from flask import Flask, jsonify, request, render_template, send_from_directory, redirect, url_for
import dados

biblioteca = dados.carregar_do_arquivo()

app = Flask(__name__)

def deletar_livro(isbn):
    for l in biblioteca:
        if l['isbn'] == isbn:
            biblioteca.remove(l)
            dados.salvar_no_arquivo(biblioteca)
            return True
    return False


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/media/<path:path>')
def serve_media(path):
    return send_from_directory('media', path)


@app.route('/')
def hello():
    return render_template('hello.html')


@app.route('/<nome>')
def meu_nome(nome=None):
    return render_template('meunome.html', nome=nome)


@app.route('/api/biblioteca', methods=['GET', 'POST'])
@app.route('/api/biblioteca/<isbn>', methods=['GET', 'DELETE', 'PUT'])
def manipula_livros(isbn=None):
    """ Função API para Biblioteca
    """
    if request.method == 'GET':
        if isbn:
            for l in biblioteca:
                if l['isbn'] == isbn:
                    return jsonify(l)
            return jsonify("message: livro não localizado"), 404
        else:
            return jsonify(biblioteca)
    elif request.method == 'POST':
        novo_livro = request.get_json()
        for l in biblioteca:
            if l['isbn'] == novo_livro['isbn']:
                return jsonify("Livro já está cadastrado"), 200
        biblioteca.append(novo_livro)
        dados.salvar_no_arquivo(biblioteca)
        return jsonify("message: livro cadastrado com sucesso"), 201
    elif request.method == 'DELETE':
        for l in biblioteca:
            if l['isbn'] == isbn:
                biblioteca.remove(l)
                dados.salvar_no_arquivo(biblioteca)
                return jsonify("mensagem: livro deletado com sucesso"), 200
        return jsonify("message: livro não localizado"), 404
    elif request.method == 'PUT':
        alteracoes = request.get_json()
        for livro in biblioteca:
            if livro['isbn'] == isbn:
                for key, value in alteracoes.items():
                    livro[key] = value
                dados.salvar_no_arquivo(biblioteca)
                return jsonify("mensagem: livro alterado com sucesso"), 200
        return jsonify("message: livro não localizado"), 404
    else:
        return 'Solicitação não aceita', 503


@app.route('/biblioteca', methods=['GET', 'POST'])
def interface_web():
    """ Função para gerenciamento via interface web
    """
    biblioteca = dados.carregar_do_arquivo()
    return render_template('biblioteca.html',biblioteca=biblioteca)

@app.route('/biblioteca/criar', methods=['GET', 'POST'])
def cria_livro():
    if request.method == 'POST':
        novo_livro = {
                    'isbn': request.form.get('isbn'),
                    'titulo': request.form.get('titulo'),
                    'autor': request.form.get('autor'),
                    "genero": request.form.get('genero'),
                    "ano_publicacao": request.form.get('ano_publicacao'),
                    "editora": request.form.get('editora'),
                    "paginas": request.form.get('paginas'),
                    "status": request.form.get('status'),
                    "localizacao": request.form.get('localizacao')
                }
        for l in biblioteca:
            if l['isbn'] == novo_livro['isbn']:
                return jsonify("Livro já está cadastrado"), 200
        biblioteca.append(novo_livro)
        dados.salvar_no_arquivo(biblioteca)
        return redirect(interface_web)
    else:
        return render_template('criar_livro.html')

if __name__ == '__main__':
    app.run(debug=True)