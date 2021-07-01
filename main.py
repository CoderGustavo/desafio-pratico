from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "jobs.visie.com.br"
app.config["MYSQL_USER"] = "gustavoornaghi"
app.config["MYSQL_PASSWORD"] = "Z3VzdGF2b29y"
app.config["MYSQL_DB"] = "gustavoornaghi"

mysql = MySQL(app)

@app.route("/", methods = ["GET", "POST"])
def inicio():
    if request.method == "POST":
        form = request.form
        nome = form["nome"]
        rg = form["rg"]
        cpf = form["cpf"]

        data_nascimento = list(form["nascimento"].split("-"))
        data_nascimento = data_nascimento[0]+"-"+data_nascimento[1]+"-"+data_nascimento[2]

        data_admissao = list(form["admissao"].split("-"))
        data_admissao = data_admissao[0]+"-"+data_admissao[1]+"-"+data_admissao[2]

        funcao = form["funcao"]

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO pessoas(nome, rg, cpf, data_nascimento, data_admissao, funcao) VALUES (%s,%s,%s,%s,%s,%s)", (nome, rg, cpf, data_nascimento, data_admissao, funcao))
        mysql.connection.commit()
        cur.close()

        return redirect("/")
    else:
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT id_pessoa,nome,rg,data_admissao FROM pessoas")
        if result > 0:
            pessoas = cur.fetchall()
        else:
            pessoas = []
        return render_template("index.html", pessoas = pessoas)

@app.route("/deletar/<string:id>")
def deletar_pessoa(id):

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM pessoas WHERE id_pessoa = %s" % (id))
    mysql.connection.commit()
    cur.close()
    return redirect("/")
app.run(debug=True)