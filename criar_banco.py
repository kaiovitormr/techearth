import sqlite3

conn = sqlite3.connect('techearth.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS indicadores')

cursor.execute('''
CREATE TABLE indicadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    ticker TEXT,
    pegada_carbono_ton_co2 REAL,        -- Emissões GEE em toneladas de CO2 equivalente
    intensidade_energetica_kwh_receita REAL,  -- kWh por R$ 1M de receita
    gestao_residuos_percent REAL,       -- % de resíduos desviados de aterros
    eficiencia_hidrica_m3 REAL,         -- Eficiência hídrica (m³/tonelada produzida)
    valor_mercado_bi REAL,              -- Valor de mercado em bilhões
    roi_sustentabilidade REAL           -- ROI da sustentabilidade (%)
)
''')

# Dados fictícios para demonstração, inspirados em padrões reais de sustentabilidade corporativa
empresas = [
    ('Floresta Verde', 'FLRV3', 150000, 85.2, 78.5, 2.1, 15.4, 12.8),
    ('PetroSol', 'PTRL4', 2500000, 245.8, 45.2, 8.9, 450.2, 8.4),
    ('Hidrabras', 'HDBR3', 850000, 156.7, 65.8, 3.2, 210.5, 10.2),
    ('Mineração Azul', 'MZLA3', 1800000, 198.4, 52.1, 6.8, 320.8, 9.1)
]

cursor.executemany('''
INSERT INTO indicadores (nome, ticker, pegada_carbono_ton_co2, intensidade_energetica_kwh_receita, gestao_residuos_percent, eficiencia_hidrica_m3, valor_mercado_bi, roi_sustentabilidade)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', empresas)

conn.commit()
conn.close()