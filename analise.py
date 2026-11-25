import sys
import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

# ==============================
# 1. LER O FICHEIRO EXCEL
# ==============================

# O ficheiro com as respostas do questionário não está incluído neste repositório.
# Uso: python analise.py respostas.xlsx   (ou deixar o ficheiro "respostas.xlsx" nesta pasta)
caminho = sys.argv[1] if len(sys.argv) > 1 else "respostas.xlsx"
df = pd.read_excel(caminho)

print("Ficheiro lido com sucesso!\n")

# Colunas disponíveis
print("COLUNAS DO DATAFRAME:")
for col in df.columns:
    print(" -", col)
print("\n")

# ==============================
# 2. ESCOLHER AS VARIÁVEIS
# ==============================

# Escolhe as colunas pelo texto da pergunta
exp_col   = df.filter(like="nível de experiência com tecnologias", axis=1).columns[0]
conf_col  = df.filter(like="Confia nas respostas / resultados que a IA fornece", axis=1).columns[0]
prod_col  = df.filter(like="Considera que o uso de IA aumenta a sua produtividade", axis=1).columns[0]
horas_col = df.filter(like="Quantas horas estima ter poupado por semana graças à IA", axis=1).columns[0]

print("Coluna experiência:", exp_col)
print("Coluna confiança :", conf_col)
print("Coluna produtividade:", prod_col)
print("Coluna horas poupadas:", horas_col, "\n")

# Variáveis base
exp   = df[exp_col]          # já vem como 1,2,3,4
conf  = df[conf_col]
prod  = df[prod_col]
horas = df[horas_col]

# ==============================
# 3. MAPEAR RESPOSTAS DE TEXTO PARA NÚMEROS (ESCALAS ORDINAIS)
# ==============================

# Valores únicos de cada escala (confirmação)
print("Valores únicos - Confiança:", conf.unique())
print("Valores únicos - Produtividade:", prod.unique())
print("Valores únicos - Horas:", horas.unique(), "\n")

# Mapeamento das escalas ordinais
conf_map = {
    "Nada confiante": 1,
    "Pouco confiante": 2,
    "Muito confiante": 3,
    "Totalmente confiante": 4,
}

prod_map = {
    "Nada": 1,
    "Pouco": 2,
    "Muito": 3,
    "Extremamente": 4,
}

horas_map = {
    "<1 hora": 1,
    "1–3 horas": 2,   # atenção: é um travessão (en dash), igual ao do Excel
    "3–5 horas": 3,
    ">5 horas": 4,
}

# Aplicar mapeamento
conf_num  = conf.map(conf_map)
prod_num  = prod.map(prod_map)
horas_num = horas.map(horas_map)

# Construir dataframes limpos (sem NaN)
data_exp_conf   = pd.DataFrame({"exp": exp, "conf": conf_num}).dropna()
data_prod_horas = pd.DataFrame({"prod": prod_num, "horas": horas_num}).dropna()

print(f"Nº de respostas válidas (Experiência/Confiança): {len(data_exp_conf)}")
print(f"Nº de respostas válidas (Produtividade/Horas): {len(data_prod_horas)}\n")

# ==============================
# 4. TESTES DE NORMALIDADE (SHAPIRO-WILK)
#    (só para justificar que não é normal)
# ==============================

for nome, serie in [
    ("Experiência", data_exp_conf["exp"]),
    ("Confiança", data_exp_conf["conf"]),
    ("Produtividade", data_prod_horas["prod"]),
    ("Horas poupadas", data_prod_horas["horas"]),
]:
    stat, p = stats.shapiro(serie)
    print(f"Shapiro - {nome}: stat = {stat:.3f}, p = {p:.3g}")
print("\n")

# ==============================
# 5. CORRELAÇÃO DE SPEARMAN
# ==============================

rho1, p1 = stats.spearmanr(data_exp_conf["exp"], data_exp_conf["conf"])
rho2, p2 = stats.spearmanr(data_prod_horas["prod"], data_prod_horas["horas"])

print("Correlação de Spearman - Experiência vs Confiança")
print(f"rs = {rho1:.3f}, p-value = {p1:.5f}\n")

print("Correlação de Spearman - Produtividade vs Horas poupadas")
print(f"rs = {rho2:.3f}, p-value = {p2:.5f}\n")

