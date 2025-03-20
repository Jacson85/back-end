#chamando o framework
from flask import Flask, render_template,redirect, url_for, request
import psycopg2

sistema = Flask(__name__)

#conexão banco de dados
def conecta_bd():
    conecta = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='1234')
    return conecta
 
#nome do sistema


#rota principal
@sistema.route("/")
def homepage():
    mensagem = request.args.get('mensagem', '')
    return render_template('index.html', mensagem=mensagem)    

#compras
@sistema.route("/carregacompras", methods=('GET', 'POST'))
def carregacompras():
    
    if request.method == 'POST':
        produto = request.form['produto']
        quantidade = request.form['quantidade']
        preco = request.form['preco']
        total = int(quantidade) * float(preco) # calculando o total com base na quantidade

        #conexao com o banco de dados e inserir os dados
        conexao = conecta_bd()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO venda (produto, quantidade, preco, total) VALUES (%s, %s, %s,%s)", (produto, quantidade, preco, total))
        conexao.commit()
        cursor.close()
        conexao.close()

        #redirecionar com uma mensagem 
        return redirect(url_for('homepage', mensagem='Produtos adicionados ao carrinho'))
    #return render_template('teste.html)
    return render_template('compras.html')

#rota da cadastro    
@sistema.route("/cadastro", methods=['POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        cidade = request.form['cidade']
        matricula = request.form['matricula']
        estado = request.form['estado']
        
        # Conectar ao banco e inserir os dados
        conexao = conecta_bd()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO test1 (nome, cpf, cidade, matricula, estado) VALUES (%s, %s, %s, %s, %s)", (nome, cpf, cidade, matricula, estado))
        conexao.commit()
        cursor.close()
        conexao.close()

    #return render_template('teste.html)
    return redirect(url_for('homepage', mensagem='Cadastrado com sucesso'))
        
    #Tela de compras
# @sistema.route("/compra", methods=['POST'])
# def compras():
#     if request.method == 'POST':
#         produto = request.form['produto']
#         quantidade = request.form['quantidade']
#         preco = request.form['preco']
#         total = request.form['total']


#         conexao = conecta_bd()
#         cursor = conexao.cursor()
#         cursor.execute("INSERT INTO venda (produto, quantidade, preco, total, ) VALUES (%s, %s, %s,%s)", (produto, quantidade, preco, total,))
#         conexao.commit()
#         cursor.close()
#         conexao.close()
#     #return render_template('teste.html)
#     return redirect(url_for('homepage', mensagem='Produtos adicionados ao carrinho'))



#rota de consulta    
#@sistema.route("/consulta")
#def consulta():