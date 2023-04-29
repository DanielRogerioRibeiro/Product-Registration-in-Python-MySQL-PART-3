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

def fecha_segunda_janela():
    segunda_tela.destroy()
    return



app=QtWidgets.QApplication([])
formulario=uic.loadUi("formulario.ui")
segunda_tela=uic.loadUi("lista_de_cadastro.ui")
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(chama_segunda_tela)
segunda_tela.pushButton.clicked.connect(gerar_pdf)
segunda_tela.pushButton_2.clicked.connect(fecha_segunda_janela)


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