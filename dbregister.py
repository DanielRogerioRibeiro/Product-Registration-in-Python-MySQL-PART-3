#Cadastro de Produtos
#Importando PyQt5
from PyQt5 import  uic,QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="cadastro_produtos"
)

#Função Global
numero_id = 0

#Função para criar o PDF
def gerar_pdf():
#mostrar a tabela
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("cadastro_produtos.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200,800, "Produtos Cadastrados:")
    pdf.setFont("Times-Bold", 18)

    pdf.drawString(10,750, "ID")
    pdf.drawString(110,750, "CODIGO")
    pdf.drawString(210,750, "PRODUTO")
    pdf.drawString(310,750, "PREÇO")
    pdf.drawString(410,750, "CATEGORIA")

    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10,750 -y, str(dados_lidos[i][0]))
        pdf.drawString(110,750 -y, str(dados_lidos[i][1]))
        pdf.drawString(210,750 -y, str(dados_lidos[i][2]))
        pdf.drawString(310,750 -y, str(dados_lidos[i][3]))
        pdf.drawString(410,750 -y, str(dados_lidos[i][4]))
    
    pdf.save() 
    print("********PDF GERADO COM SUCESSO!!!!********")





def funcao_principal():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()
    
    categoria = ""

    if formulario.radioButton.isChecked() :
        print("Categoria Produtos selecionada")
        categoria = "Produtos"
    elif formulario.radioButton_2.isChecked() :
        print("Categoria Serviços selecionada")
        categoria = "Serviços"
    else :
        print("Categoria Outros selecionada")
        categoria = "Outros"

    print("Código:",linha1)
    print("Descrição:",linha2)
    print("Preco",linha3)

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO produtos (codigo,descrição,preco,categoria) VALUES (%s,%s,%s,%s)"
    dados = (str(linha1),str(linha2),str(linha3),categoria)
    cursor.execute(comando_SQL,dados)
    banco.commit()
    #Apagando o texto da tela
    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")

#Criando a função para chamar a segunda tela
def chama_segunda_tela():
    segunda_tela.show()

#mostrar a tabela
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

#exibindo os dados cadastrados na tabela   
    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            segunda_tela.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))



def excluir_registro():
    #Excluindo registro apenas da tabela
    linha = segunda_tela.tableWidget.currentRow()
    segunda_tela.tableWidget.removeRow(linha)

    #Excluindo registro do banco de dados
    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM produtos WHERE id=" + str(valor_id))

def editar_registro():
    global numero_id
    #Editando registro apenas da tabela
    linha = segunda_tela.tableWidget.currentRow()
    
    #Excluindo registro do banco de dados
    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM produtos WHERE id=" + str(valor_id))
    produto = cursor.fetchall()
    tela_editar.show()

    numero_id = valor_id
 
    #Exibindo a linha selecionada na janela menu_editar
    tela_editar.lineEdit.setText(str(produto [0][0]))
    tela_editar.lineEdit_2.setText(str(produto[0][1]))
    tela_editar.lineEdit_3.setText(str(produto[0][2]))
    tela_editar.lineEdit_4.setText(str(produto[0][3]))
    tela_editar.lineEdit_5.setText(str(produto[0][4]))


def salvar_dados_editados():
    #Traz o numero id
    global numero_id
    
    #Valor digitado no LineEdit
    codigo    = tela_editar.lineEdit_2.text()
    descrição = tela_editar.lineEdit_3.text()
    preco     = tela_editar.lineEdit_4.text()
    categoria = tela_editar.lineEdit_5.text()
    #Atulizando os dados no banco
    cursor = banco.cursor()
    cursor.execute("UPDATE produtos SET codigo ='{}', descrição ='{}', preco ='{}', categoria ='{}' WHERE id = {}".format(codigo,descrição,preco,categoria,numero_id))
    #Atualizar as janelas
    tela_editar.close()
    segunda_tela.close()
    chama_segunda_tela()
    


def fecha_segunda_janela():
    segunda_tela.destroy()
    return

def fecha_formulario():
    formulario.close()
    return

def fecha_tela_editar():
    tela_editar.close()
    return

app=QtWidgets.QApplication([])
formulario=uic.loadUi("formulario.ui")
segunda_tela=uic.loadUi("lista_de_cadastro.ui")
tela_editar=uic.loadUi("menu_editar.ui")
#Botões da tela formulario
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(chama_segunda_tela)
formulario.pushButton_3.clicked.connect(fecha_formulario)
#Botões da tela lista_de_cadastro
segunda_tela.pushButton.clicked.connect(gerar_pdf)
segunda_tela.pushButton_2.clicked.connect(fecha_segunda_janela)
segunda_tela.pushButton_3.clicked.connect(excluir_registro)
segunda_tela.pushButton_4.clicked.connect(editar_registro)
#botões da tela menu_editar
tela_editar.pushButton.clicked.connect(salvar_dados_editados)
tela_editar.pushButton_2.clicked.connect(fecha_tela_editar)



formulario.show()
app.exec()



# criando a tabela
"""create table produtos (
    id INT NOT NULL AUTO_INCREMENT,
    codigo INT,
    descrição VARCHAR(50),
    preco DOUBLE,
    categoria VARCHAR (20),
    PRIMARY KEY (id)
); """

#INSERT INTO produtos (codigo,descrição,preco,categoria) VALUES (123,"Caneca Anjo",76.00,"produtos");