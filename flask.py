from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def conectar_banco():
    return mysql.connector.connect(
        host="10.60.47.60",
        user="kevin",
        password="kali",
        database="projeto_senac"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    
    if nome == "" or email == "" or senha == "":
        flash("Todos os campos são obrigatórios")
        return redirect(url_for('index'))
    
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        sql = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
        valores = (nome, email, senha)
        cursor.execute(sql, valores)
        conn.commit()
        flash("Usuário cadastrado com sucesso")
    except mysql.connector.Error as err:
        flash(f"Erro ao conectar ao banco de dados: {err}")
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
