from flask import Flask, render_template, request, flash
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

app = Flask(__name__)
app.secret_key = '142-045-401'

@app.route("/")
def index():
    return render_template("index.html")

# Rota para exibir o formulário
@app.route("/form")
def process_form():
    return render_template("form.html")

# Rota para processar o formulário
@app.route("/form", methods=["POST"]) #criando formulário para inputar dados na tabela de 52
def submit():

    # Configurando as credenciais do Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(creds)
    #sheet = client.open("Plano 52 semanas - Manutenção Preventiva").sheet1
    sa = gspread.service_account('service_account.json')  
    worksheet = '52 semanas'
    name_sheet = 'Plano 52 semanas - Manutenção Preventiva'
    sh = sa.open(name_sheet)
    wks = sh.worksheet(worksheet)
    list1 = wks.get_all_records()
    table = pd.DataFrame(list1)

    # Obtendo os dados do formulário
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    # Adicionando os dados à planilha do Google Sheets
    row = [name, email, message]
    wks.append_row(row)

    if name != '':
        flash('inserido')
        return render_template('form.html')
    else:
        flash('existe')
        return render_template('form.html')
    
    return render_template('form.html')

@app.route("/table1") #criando a visualização da tabela de 52 semanas
def table():

    # Configurando as credenciais do Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(creds)
    #sheet = client.open("Plano 52 semanas - Manutenção Preventiva").sheet1
    sa = gspread.service_account('service_account.json')  
    worksheet = '52 semanas'
    name_sheet = 'Plano 52 semanas - Manutenção Preventiva'
    sh = sa.open(name_sheet)
    wks = sh.worksheet(worksheet)
    list1 = wks.get_all_records()
    table = pd.DataFrame(list1)

    data = wks.get_all_records()
    df = pd.DataFrame(data)
    table_html = df.to_html(classes='table')

    return render_template('table1.html', table_html=table_html)


if __name__ == "__main__":
    app.run(debug=True)