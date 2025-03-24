# Importa as bibliotecas necessárias do Flask e do psycopg2 para conexão com PostgreSQL
from flask import Flask, render_template, request, make_response, redirect, url_for
import psycopg2
import math


#LIBs para gerar o relatório em pdf (adicione o MAKE_RESPOSE acima)
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Table, TableStyle, Paragraph
# Inicializa a aplicação Flask
sistema = Flask(__name__)

# Função para conectar ao banco de dados PostgreSQL
def conecta_bd():
    conecta = psycopg2.connect(
        host='localhost',      # Host do banco de dados
        database='postgres',   # Nome do banco de dados
        user='postgres',       # Usuário do banco de dados
        password='1234',        # Senha do banco de dados
        port=5433
    )
    return conecta

# ====================================
# ROTAS DE NAVEGAÇÃO DO SISTEMA
# ====================================

# Rota principal (home)
@sistema.route("/")
def homepage():
    # Obtém mensagem da URL (se houver) para exibir no template
    mensagem = request.args.get('mensagem', '')
    return render_template('index.html', mensagem=mensagem)

# Rota de navegação para a página de compras (GET)
@sistema.route("/n_carregacompras", methods=['GET'])
def n_carregacompras():
    return render_template('compras.html')



# Rota para processar compras (GET e POST)
@sistema.route("/carregacompras", methods=['GET', 'POST'])
def carregacompras():
    if request.method == 'POST':
        # Obtém os valores do formulário
        produto = request.form['produto']
        quantidade = request.form['quantidade']
        preco = request.form['preco']
        total = int(quantidade) * float(preco)  # Calcula o total

        # Conecta ao banco e insere os dados na tabela "venda"
        conexao = conecta_bd()
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO venda (produto, quantidade, preco, total) VALUES (%s, %s, %s, %s)",
            (produto, quantidade, preco, total)
        )
        conexao.commit()
        cursor.close()
        conexao.close()

        # Redireciona para a página inicial com uma mensagem
        return redirect(url_for('homepage', mensagem='Produtos adicionados ao carrinho'))
    
    # Retorna a página de compras
    return render_template('compras.html')

# ====================================
# ROTAS DE NAVEGAÇÃO DO SISTEMA DE CADASTRO
# ====================================
# Rota para exibir a página de cadastro
@sistema.route("/n_cadastro", methods=['GET'])
def n_cadastro():
    return render_template('cadastro.html')

# Rota para processar cadastro de alunos
@sistema.route("/cadastro", methods=['POST'])
def cadastro():
    if request.method == 'POST':
        # Obtém os dados do formulário
        nome = request.form['nome']
        cpf = request.form['cpf']
        cidade = request.form['cidade']
        matricula = request.form['matricula']
        estado = request.form['estado']

        # Conecta ao banco e insere os dados na tabela "test1"
        conexao = conecta_bd()
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO test1 (nome, cpf, cidade, matricula, estado) VALUES (%s, %s, %s, %s, %s)",
            (nome, cpf, cidade, matricula, estado)
        )
        conexao.commit()
        cursor.close()
        conexao.close()

        # Redireciona para a página inicial com mensagem de sucesso
        return redirect(url_for('homepage', mensagem='Cadastrado com sucesso'))
    # ====================================

    # =============================================
# ROTAS DE NAVEGAÇÃO DO SISTEMA DE CADASTRO_PRODUTO
# =================================================

    #rota para  exibir a página cadastro_produtos
@sistema.route("/n_cadastro_produto", methods=['GET'])
def n_cadastro_produto():
    return render_template('cadastro_produto.html')
    # Rota para processar cadastro de produtos

@sistema.route("/cadastro_produto", methods=['POST'])
def cadastro_produto():
    if request.method == 'POST':
        # Obtém os dados do formulário
        produto = request.form['produto']
        preco = request.form['preco']
        quantidade = request.form['quantidade']
        

        # Conecta ao banco e insere os dados na tabela "test1"
        conexao = conecta_bd()
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO compras2 ( produto, preco, quantidade) VALUES (%s, %s, %s)",
            ( produto, preco, quantidade)
        )
        conexao.commit()
        cursor.close()
        conexao.close()

        # Redireciona para a página inicial com mensagem de sucesso
        return redirect(url_for('homepage', mensagem='Cadastrado com sucesso'))

# Rota para exibir a página de consulta (grid)
@sistema.route("/n_cadastro_produto", methods=['GET'])
def n_grid_produto():
    return render_template('cadastro_produto.html')
# ===============================================================================

# ================================
# CADASTROS DE CURSO
# ================================
@sistema.route("/n_cadastro_curso", methods=['GET'])
def n_cadastro_curso():
    return render_template('cadastro_curso.html')

    # Rota para processar cadastro de cursos
@sistema.route("/cadastro_curso", methods=['POST'])
def cadastro_curso():
    if request.method == 'POST':
        # Obtém os dados do formulário
        nome_curso = request.form['nome_curso']
        codigo_curso = request.form['codigo_curso']
        inicio_curso = request.form['inicio_curso']
        

        # Conecta ao banco e insere os dados na tabela "test1"
        conexao = conecta_bd()
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO cursos_teste ( nome_curso, codigo_curso, inicio_curso) VALUES (%s, %s, %s)",
            ( nome_curso, codigo_curso, inicio_curso)
        )
        conexao.commit()
        cursor.close()
        conexao.close()

        # Redireciona para a página inicial com mensagem de sucesso
        return redirect(url_for('homepage', mensagem='Cadastrado com sucesso'))
    
    # Rota para exibir a página de consulta (grid)
@sistema.route("/n_cadastro_curso", methods=['GET'])
def n_grid_curso():
    return render_template('cadastro_curso.html')
# =======================================================================================


# ==================================================================
# Rota de consulta
# ==================================================================
@sistema.route("/n_grid", methods=['GET'])
def n_grid():
    return render_template('consulta.html')
# Rota para processar a exibição da tabela de clientes
@sistema.route("/grid", methods=['GET', 'POST'])
def grid():
    if request.method == 'POST':
        # Conecta ao banco e busca todos os registros da tabela "test1"
        conexao = conecta_bd()
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM test1')
        clientes = cursor.fetchall()  # Obtém os resultados
        cursor.close()
        conexao.close()

        # Renderiza a página com os dados dos clientes
        return render_template('consulta.html', clientes=clientes)
    
    # Se for GET, apenas retorna a página sem clientes
    return render_template('consulta.html', clientes=None)






# Rota para exibir a página de cursos
@sistema.route("/n_cursos", methods=['GET'])
def n_cursos():
    return render_template('cursos.html')

# Rota para exibir os cursos cadastrados no banco
@sistema.route("/cursos", methods=['GET', 'POST'])
def cursos():
    if request.method == 'POST':
        # Conecta ao banco e busca todos os cursos na tabela "Cursos"
        conexao = conecta_bd()
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM Cursos')
        cursos = cursor.fetchall()
        cursor.close()
        conexao.close()

        # Renderiza a página com a lista de cursos
        return render_template('cursos.html', cursos=cursos)
    
    # Se for GET, retorna a página sem cursos
    return render_template('cursos.html', cursos=None)





# -----------------------
# FILTROS DE PESQUISA
# -----------------------

# Rota para exibir a página de filtro
@sistema.route("/n_filtro", methods=['GET'])
def n_filtro():
    return render_template('filtro.html')

# Rota para processar a pesquisa por nome na tabela "test1"
@sistema.route("/filtro", methods=['GET', 'POST'])
def filtro():
    if request.method == 'POST':
        # Obtém o valor digitado no formulário
        filtro_pesquisa = request.form['filtro_input']

        # Conecta ao banco e busca alunos pelo nome
        conexao = conecta_bd()
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT * FROM test1 WHERE LOWER(nome) LIKE LOWER(%s)",
            ('%' + filtro_pesquisa + '%',)
        )
        alunos = cursor.fetchall()
        cursor.close()
        conexao.close()

        # Retorna a página com os alunos encontrados
        return render_template('filtro.html', alunos=alunos)
    
    # Se for GET, retorna a página sem alunos
    return render_template('filtro.html', alunos=None)

#Rota da paginação
@sistema.route("/paginacao", methods=['GET', 'POST'])
def paginacao():
    page = request.args.get('page', 1, type=int)
    quantidade = 5

    conexao = conecta_bd()
    cursor = conexao.cursor()

    #Aqui ele vai contar a quantidade de registros
    cursor.execute('SELECT count(*) FROM cliente')
    total_items = cursor.fetchone()[0]

    #Calcular o número total de páginas
    total_pages = math.ceil(total_items / quantidade)

    #Calcular a saída da consulta
    offset = (page - 1) * quantidade

    cursor.execute('''SELECT nome, cpf, cidade, estado, profissao FROM cliente ORDER BY nome LIMIT %s OFFSET %s''', (quantidade, offset))

    clientes = cursor.fetchall()
    cursor.close()
    conexao.close()

    clientes_lista = []
    for cliente in clientes:
        clientes_lista.append({
            'nome':cliente[0],
            'cpf':cliente[1],
            'cidade':cliente[2],
            'estado':cliente[3],
            'profissao':cliente[4]
        })

    #return render_template('grid_completo.html', clientes=clientes_lista, page=page, total_pages=total_pages)
    return render_template('grid_completo.html', clientes=clientes_lista, page=page, total_pages=total_pages)


# ===============================
# INICIALIZA O SERVIDOR FLASK
# ===============================

if __name__ == "__main__":
    # Executa a aplicação Flask no modo debug
    sistema.run(debug=True, port=8085, host='127.0.0.1')