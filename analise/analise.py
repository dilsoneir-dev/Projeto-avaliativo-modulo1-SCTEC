# ====================================================================
# Projeto Avaliativo - Módulo 1 (SCTEC / SENAI)
# Script de Análise Exploratória (EDA) em Python
# ====================================================================

import pandas as pd
import matplotlib.pyplot as plt

# 1. Carregar os dois arquivos CSV gerados no FreeSQL
print("Carregando os dados...")
df_dept = pd.read_csv("CSV/query_01.csv")
df_regiao = pd.read_csv("CSV/query_02.csv")

print(f"Total de registros na Query 1: {len(df_dept)}")
print(f"Total de registros na Query 2: {len(df_regiao)}")

# 2. Estatísticas básicas dos salários (geral)
media = df_dept["SALARY"].mean()
mediana = df_dept["SALARY"].median()
menor_salario = df_dept["SALARY"].min()
maior_salario = df_dept["SALARY"].max()

print("\n--- RESUMO DOS SALÁRIOS ---")
print(f"Média: R$ {media:.2f}")
print(f"Mediana: R$ {mediana:.2f}")
print(f"Menor salário: R$ {menor_salario:.2f}")
print(f"Maior salário: R$ {maior_salario:.2f}")

# Observação sobre a diferença
diff = media - mediana
print(f"Diferença entre média e mediana: R$ {diff:.2f}")
if diff > 0:
    print("A média é maior que a mediana porque os salários mais altos (diretoria) puxam o valor pra cima.")

# 3. Média e contagem de salários por departamento
print("\n--- SALÁRIOS POR DEPARTAMENTO ---")
dept_resumo = df_dept.groupby("DEPARTMENT_NAME")["SALARY"].agg(["count", "mean", "median", "min", "max"])
dept_resumo = dept_resumo.rename(columns={
    "count": "Qtd",
    "mean": "Média",
    "median": "Mediana",
    "min": "Mínimo",
    "max": "Máximo"
}).sort_values(by="Média", ascending=False)
print(dept_resumo.round(2))

# 4. Funcionários e salários por região
print("\n--- SALÁRIOS POR REGIÃO ---")
regiao_resumo = df_regiao.groupby("REGION_NAME")["SALARY"].agg(["count", "mean", "median", "min", "max"])
regiao_resumo = regiao_resumo.rename(columns={
    "count": "Qtd",
    "mean": "Média",
    "median": "Mediana",
    "min": "Mínimo",
    "max": "Máximo"
})
print(regiao_resumo.round(2))

# 5. Gerando os gráficos

# Gráfico 1: Histograma com linha de média e mediana
plt.figure(figsize=(8, 5))
plt.hist(df_dept["SALARY"], bins=10, color="steelblue", edgecolor="black")
plt.axvline(media, color="red", linestyle="--", label=f"Média: {media:.0f}")
plt.axvline(mediana, color="green", linestyle="-", label=f"Mediana: {mediana:.0f}")
plt.title("Distribuição dos Salários (HR)")
plt.xlabel("Salário ($)")
plt.ylabel("Quantidade de Funcionários")
plt.legend()
plt.tight_layout()
plt.savefig("analise/graficos/histograma_salarios.png")
plt.close()
print("\n[OK] Histograma salvo em analise/graficos/histograma_salarios.png")

# Gráfico 2: Boxplot dos salários por departamento
# Vou filtrar apenas departamentos com pelo menos 3 funcionários para o gráfico não ficar poluído
principais_depts = df_dept["DEPARTMENT_NAME"].value_counts()[lambda x: x >= 3].index
dados_filtrados = df_dept[df_dept["DEPARTMENT_NAME"].isin(principais_depts)]

dados_grafico = [dados_filtrados[dados_filtrados["DEPARTMENT_NAME"] == d]["SALARY"] for d in principais_depts]

plt.figure(figsize=(9, 5))
plt.boxplot(dados_grafico, tick_labels=principais_depts)
plt.title("Variação dos Salários por Departamento")
plt.xlabel("Departamento")
plt.ylabel("Salário ($)")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("analise/graficos/boxplot_salarios.png")
plt.close()
print("[OK] Boxplot salvo em analise/graficos/boxplot_salarios.png")

# Gráfico 3: Quantidade de funcionários por região
plt.figure(figsize=(6, 4))
df_regiao["REGION_NAME"].value_counts().plot(kind="bar", color="cornflowerblue", edgecolor="black")
plt.title("Quantidade de Funcionários por Região")
plt.xlabel("Região")
plt.ylabel("Número de Pessoas")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("analise/graficos/funcionarios_por_regiao.png")
plt.close()
print("[OK] Gráfico de barras salvo em analise/graficos/funcionarios_por_regiao.png")

print("\nAnálise finalizada com sucesso!")
