from flask import Flask, render_template, make_response
import sqlite3
import pandas as pd

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
    conn = get_db_connection()
    df = pd.read_sql_query('SELECT nome, pegada_carbono_ton_co2, intensidade_energetica_kwh_receita, gestao_residuos_percent, eficiencia_hidrica_m3, valor_mercado_bi, roi_sustentabilidade FROM indicadores', conn)
    conn.close()
    
    # Calcular médias dos KPIs ambientais
    media_pegada_carbono = df['pegada_carbono_ton_co2'].mean()
    media_intensidade_energetica = df['intensidade_energetica_kwh_receita'].mean()
    media_gestao_residuos = df['gestao_residuos_percent'].mean()
    media_eficiencia_hidrica = df['eficiencia_hidrica_m3'].mean()
    
    return render_template('impacto.html', 
                          media_pegada_carbono=media_pegada_carbono,
                          media_intensidade_energetica=media_intensidade_energetica,
                          media_gestao_residuos=media_gestao_residuos,
                          media_eficiencia_hidrica=media_eficiencia_hidrica,
                          empresas=df.to_dict(orient='records'))

@app.route('/impacto/resumo.doc')
def impacto_resumo():
    conn = get_db_connection()
    df = pd.read_sql_query('SELECT nome, ticker, pegada_carbono_ton_co2, intensidade_energetica_kwh_receita, gestao_residuos_percent, eficiencia_hidrica_m3, valor_mercado_bi, roi_sustentabilidade FROM indicadores', conn)
    conn.close()

    empresas = df.to_dict(orient='records')
    html = render_template('resumo_doc.html', empresas=empresas)
    response = make_response(html)
    response.headers['Content-Type'] = 'application/msword'
    response.headers['Content-Disposition'] = 'attachment; filename=Resumo_Inteligencia_Ambiental.doc'
    return response

if __name__ == '__main__':
    app.run(debug=True)
