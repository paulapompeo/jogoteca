from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = 'teste'


class Jogo:
    def __init__(self, nome, categoria, console):  # essa classe nao esta implementada do jeito correto
        self.nome = nome
        self.categoria = categoria
        self.console = console

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha

usuario1 = Usuario('paula', 'Paula Pompeo', '123456')
usuario2 = Usuario('bino', 'Bino Carneiro', 'passear')

usuarios = {usuario1.id: usuario1,
            usuario2.id: usuario2}

jogo1 = Jogo('Super Mario', 'Ação', 'SNES')
jogo2 = Jogo('Pokemon Gold', 'RPG', 'GBA')
lista = [jogo1, jogo2]


@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)  # é assim que renderiza um html no python


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')


@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Não logado, tente novamente!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))


app.run(debug=True)  # assim fica no modo de desenvolvimento -> nao é mais necessario reiniciar o servidor
# já da um reload automático, sem ter que salvar a casa atualizacao de codigo


# trecho da app -> Para definir a porta como 8080 e o host como 0.0.0.0 (acesso externo)
# app.run(host='0.0.0.0', port=8080)
