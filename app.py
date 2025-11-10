import mysql.connector
from flask import Flask, render_template, request

app = Flask(__name__)

def executar_comandos(query, value=None, fetchone=False, retornar_id=False):
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="JoãoVictor15",
        database="ldc"
    )
    cursor = conexao.cursor()

    cursor.execute(query, value)
    resultado = None

    comando = query.strip().split()[0].upper()

    if comando == "SELECT":
        resultado = cursor.fetchone() if fetchone else cursor.fetchall()
    elif comando == "INSERT" and retornar_id:
        conexao.commit()
        resultado = cursor.lastrowid
    else:
        conexao.commit()

    cursor.close()
    conexao.close()
    return resultado


@app.route("/", methods=['GET', 'POST'])
def principal():
    if request.method == 'POST':
        item = request.form['item']
        quant = request.form['number']

        # insere item e quantidade na tabela lista
        query = '''INSERT INTO lista (produto, quantidade) VALUES (%s, %s)'''
        value = (item, quant)
        executar_comandos(query, value)

    # busca todos os itens cadastrados
    query = '''SELECT id, produto, quantidade FROM lista'''
    resultado = executar_comandos(query)
    return render_template("lista.html", resultado=resultado)


if __name__ == "__main__":
    app.run(debug=True)
    