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
    # Aqui é onde você define a lista que vai aparecer na tabela
    lista_empresas = [
        {'nome': 'EcoLogic Tech', 'pegada_carbono_ton_co2': 120, 'intensidade_energetica_kwh_receita': 10.2, 'gestao_residuos_percent': 92, 'roi_sustentabilidade': 15.4},
        {'nome': 'BioSystems Store', 'pegada_carbono_ton_co2': 85, 'intensidade_energetica_kwh_receita': 8.5, 'gestao_residuos_percent': 88, 'roi_sustentabilidade': 12.1},
        {'nome': 'Green Solutions', 'pegada_carbono_ton_co2': 210, 'intensidade_energetica_kwh_receita': 14.8, 'gestao_residuos_percent': 75, 'roi_sustentabilidade': 19.5},
        {'nome': 'Pure Water Corp', 'pegada_carbono_ton_co2': 45, 'intensidade_energetica_kwh_receita': 5.2, 'gestao_residuos_percent': 95, 'roi_sustentabilidade': 8.9},
        {'nome': 'Future Energy', 'pegada_carbono_ton_co2': 320, 'intensidade_energetica_kwh_receita': 18.1, 'gestao_residuos_percent': 68, 'roi_sustentabilidade': 22.3}
    ]
    
    # Mandando a lista e as médias para o site
    return render_template('impacto.html', 
                           empresas=lista_empresas, 
                           media_pegada_carbono=156, 
                           media_intensidade_energetica=11.4, 
                           media_gestao_residuos=83.6)

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