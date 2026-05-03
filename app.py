from flask import Flask, render_template, make_response
import sqlite3
import pandas as pd
from xhtml2pdf import pisa  # Nova biblioteca para o PDF
import io  # Para lidar com o arquivo na memória

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('techearth.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projetos')
def projetos():
    return render_template('projetos.html')

@app.route('/impacto')
def impacto():
    # Crie uma lista vazia ou com dados para o loop não quebrar
    empresas_demo = [
        {'nome': 'Empresa A', 'pegada_carbono_ton_co2': 150, 'intensidade_energetica_kwh_receita': 12.5, 'gestao_residuos_percent': 85, 'roi_sustentabilidade': 18.2}
    ]
    
    return render_template('impacto.html', 
                           empresas=empresas_demo, 
                           media_pegada_carbono=150, 
                           media_intensidade_energetica=12.5, 
                           media_gestao_residuos=85)

# NOVA ROTA PARA PDF (Substituindo a de .doc)
@app.route('/impacto/resumo.pdf')
def impacto_resumo_pdf():
    # 1. Busca os dados no banco de dados
    conn = get_db_connection()
    df = pd.read_sql_query('SELECT nome, ticker, pegada_carbono_ton_co2, intensidade_energetica_kwh_receita, gestao_residuos_percent, eficiencia_hidrica_m3, valor_mercado_bi, roi_sustentabilidade FROM indicadores', conn)
    conn.close()

    empresas = df.to_dict(orient='records')
    
    # 2. Renderiza o HTML (aquele código ABNT que você me mandou)
    # Certifique-se que o nome do arquivo abaixo é o mesmo que você salvou na pasta templates
    html = render_template('resumo_abnt.html', empresas=empresas)
    
    # 3. Transforma o HTML em PDF
    out = io.BytesIO()
    pisa.CreatePDF(io.BytesIO(html.encode('utf-8')), dest=out)
    
    # 4. Envia o arquivo para o navegador
    response = make_response(out.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    # 'inline' faz abrir no navegador, 'attachment' faz baixar direto
    response.headers['Content-Disposition'] = 'inline; filename=Resumo_TechEarth_ABNT.pdf'
    
    return response

if __name__ == '__main__':
    app.run(debug=True)