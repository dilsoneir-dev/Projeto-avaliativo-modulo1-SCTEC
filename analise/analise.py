"""
Projeto Avaliativo - Módulo 1 (SCTEC / SENAI)
Visualização de Dados e Business Intelligence [T3]

Script de Análise Exploratória de Dados (EDA)
Dados: Esquema HR extraídos via FreeSQL (query_01.csv e query_02.csv)
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# Definir caminhos dos arquivos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_DIR = os.path.join(BASE_DIR, "CSV")
GRAFICOS_DIR = os.path.join(BASE_DIR, "analise", "graficos")

# Garantir que a pasta de gráficos existe
os.makedirs(GRAFICOS_DIR, exist_ok=True)

print("=" * 60)
print("1. CARREGAMENTO DOS DADOS")
print("=" * 60)

caminho_query1 = os.path.join(CSV_DIR, "query_01.csv")
caminho_query2 = os.path.join(CSV_DIR, "query_02.csv")

df_dept_job = pd.read_csv(caminho_query1)
df_regiao = pd.read_csv(caminho_query2)

print(f"Query 01 (Departamentos e Cargos): {df_dept_job.shape[0]} registros carregados.")
print(f"Query 02 (Regiões e Localização): {df_regiao.shape[0]} registros carregados.")

print("\n" + "=" * 60)
print("2. ESTATÍSTICAS BÁSICAS DE SALÁRIO (GERAL)")
print("=" * 60)

media_sal = df_dept_job["SALARY"].mean()
mediana_sal = df_dept_job["SALARY"].median()
min_sal = df_dept_job["SALARY"].min()
max_sal = df_dept_job["SALARY"].max()
desvio_sal = df_dept_job["SALARY"].std()

print(f"Média Salarial:   $ {media_sal:.2f}")
print(f"Mediana Salarial: $ {mediana_sal:.2f}")
print(f"Salário Mínimo:   $ {min_sal:.2f}")
print(f"Salário Máximo:   $ {max_sal:.2f}")
print(f"Desvio Padrão:    $ {desvio_sal:.2f}")

diff_media_mediana = media_sal - mediana_sal
print(f"\nDiferença (Média - Mediana): $ {diff_media_mediana:.2f}")
if diff_media_mediana > 0:
    print("Interpretação: A média é maior que a mediana. Isso indica uma distribuição")
    print("assimétrica à direita (positiva), com poucos cargos de alta liderança")
    print("puxando a média para cima.")

print("\n" + "=" * 60)
print("3. SALÁRIOS POR DEPARTAMENTO")
print("=" * 60)

stats_dept = df_dept_job.groupby("DEPARTMENT_NAME")["SALARY"].agg(
    Qtd_Funcionarios="count",
    Media="mean",
    Mediana="median",
    Minimo="min",
    Maximo="max"
).sort_values(by="Media", ascending=False)

print(stats_dept.round(2))

print("\n" + "=" * 60)
print("4. SALÁRIOS E FUNCIONÁRIOS POR REGIÃO")
print("=" * 60)

stats_regiao = df_regiao.groupby("REGION_NAME")["SALARY"].agg(
    Qtd_Funcionarios="count",
    Media="mean",
    Mediana="median",
    Minimo="min",
    Maximo="max"
).sort_values(by="Qtd_Funcionarios", ascending=False)

print(stats_regiao.round(2))

print("\n" + "=" * 60)
print("5. GERANDO GRÁFICOS")
print("=" * 60)

# -------------------------------------------------------------
# Gráfico 1: Histograma da Distribuição Salarial
# -------------------------------------------------------------
plt.figure(figsize=(9, 5))
plt.hist(df_dept_job["SALARY"], bins=12, color="#2b5c8f", edgecolor="black", alpha=0.8)
plt.axvline(media_sal, color="red", linestyle="--", linewidth=2, label=f"Média: ${media_sal:,.0f}")
plt.axvline(mediana_sal, color="green", linestyle="-", linewidth=2, label=f"Mediana: ${mediana_sal:,.0f}")

plt.title("Distribuição de Salários dos Funcionários (HR)", fontsize=13, pad=12)
plt.xlabel("Salário ($)", fontsize=11)
plt.ylabel("Quantidade de Funcionários", fontsize=11)
plt.grid(axis="y", linestyle=":", alpha=0.6)
plt.legend(fontsize=11)
plt.tight_layout()

caminho_hist = os.path.join(GRAFICOS_DIR, "histograma_salarios.png")
plt.savefig(caminho_hist, dpi=150)
plt.close()
print(f"[OK] Histograma salvo em: {caminho_hist}")

# -------------------------------------------------------------
# Gráfico 2: Boxplot de Salários (Geral e por Departamento)
# -------------------------------------------------------------
# Selecionar os departamentos com pelo menos 3 funcionários para visualização clara
depts_principais = df_dept_job["DEPARTMENT_NAME"].value_counts()[lambda x: x >= 3].index
df_filtrado_dept = df_dept_job[df_dept_job["DEPARTMENT_NAME"].isin(depts_principais)]

plt.figure(figsize=(10, 6))
# Boxplot por departamento
dados_por_dept = [df_filtrado_dept[df_filtrado_dept["DEPARTMENT_NAME"] == d]["SALARY"] for d in depts_principais]
plt.boxplot(dados_por_dept, tick_labels=depts_principais, patch_artist=True,
            boxprops=dict(facecolor="#90caf9", color="#1565c0"),
            medianprops=dict(color="red", linewidth=2))

plt.title("Variação Salarial por Departamento (Principais)", fontsize=13, pad=12)
plt.xlabel("Departamento", fontsize=11)
plt.ylabel("Salário ($)", fontsize=11)
plt.xticks(rotation=25, ha="right")
plt.grid(axis="y", linestyle=":", alpha=0.6)
plt.tight_layout()

caminho_box = os.path.join(GRAFICOS_DIR, "boxplot_salarios.png")
plt.savefig(caminho_box, dpi=150)
plt.close()
print(f"[OK] Boxplot salvo em: {caminho_box}")

# -------------------------------------------------------------
# Gráfico 3: Quantidade de Funcionários por Região
# -------------------------------------------------------------
plt.figure(figsize=(8, 4.5))
regioes_count = df_regiao["REGION_NAME"].value_counts()
plt.bar(regioes_count.index, regioes_count.values, color="#4caf50", edgecolor="black", width=0.5)

for i, v in enumerate(regioes_count.values):
    plt.text(i, v + 1, str(v), ha="center", fontsize=10, fontweight="bold")

plt.title("Distribuição de Funcionários por Região Geográfica", fontsize=13, pad=12)
plt.xlabel("Região", fontsize=11)
plt.ylabel("Número de Colaboradores", fontsize=11)
plt.ylim(0, max(regioes_count.values) + 10)
plt.grid(axis="y", linestyle=":", alpha=0.6)
plt.tight_layout()

caminho_barras = os.path.join(GRAFICOS_DIR, "funcionarios_por_regiao.png")
plt.savefig(caminho_barras, dpi=150)
plt.close()
print(f"[OK] Gráfico de Regiões salvo em: {caminho_barras}")

print("\n" + "=" * 60)
print("ANÁLISE E GERAÇÃO DE GRÁFICOS CONCLUÍDAS COM SUCESSO!")
print("=" * 60)
