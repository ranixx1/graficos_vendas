# Coleta dados do back-end para gerar gráficos
import jaydebeapi
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import jpype 


DB_NAME_TCP = "estoque_db" 

JDBC_DRIVER_CLASS = "org.h2.Driver"
H2_TCP_HOST = "localhost" 
H2_TCP_PORT = "9092"      
JDBC_URL = f"jdbc:h2:file:/home/ranilton/Área de Trabalho/estoque-vendas/data/estoque_db;DB_CLOSE_DELAY=-1"

DB_USER = "sa"
DB_PASSWORD = "" 


H2_DRIVER_PATH = "/home/ranilton/.m2/repository/com/h2database/h2/2.3.232/h2-2.3.232.jar" 

def conectar_e_extrair_dados():
    conn = None
    try:
        if not jpype.isJVMStarted():
            jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % H2_DRIVER_PATH)
        
        conn = jaydebeapi.connect(
            JDBC_DRIVER_CLASS,
            JDBC_URL, 
            [DB_USER, DB_PASSWORD],
            H2_DRIVER_PATH, 
        )
        print("Conexão com o banco de dados H2 estabelecida com sucesso!")
        
        # Consulta SQL para buscar dados dos produtos
        query = "SELECT NOME, QUANTIDADE_ESTOQUE, PRECO_VENDA FROM PRODUTOS" 
        
        # Carrega os dados no Pandas DataFrame
        df = pd.read_sql(query, conn)

        df.columns = ['NOME', 'QUANTIDADE_ESTOQUE', 'PRECO_VENDA']


        df['NOME'] = df['NOME'].apply(lambda x: str(x))

        print("\nDados extraídos (Primeiras 5 linhas):")
        print(df.head())
        return df

    except Exception as e:
        print(f"Erro ao conectar ou extrair dados: {e}")
        return None
    finally:
        if conn:
            conn.close()
            print("Conexão com o banco de dados H2 fechada.")

def gerar_grafico_estoque(df):
    if df is None or df.empty:
        print("Não há dados para gerar o gráfico de Quantidade em Estoque (Pizza).")
        return

    plt.figure(figsize=(8, 8))
    plt.pie(df['QUANTIDADE_ESTOQUE'], labels=df['NOME'], autopct='%1.1f%%', startangle=90)
    plt.title('Distribuição do Estoque por Produto (Gráfico de Pizza)')
    plt.tight_layout()
    plt.savefig("grafico_estoque_pizza.png")
    plt.close()

def gerar_grafico_preco_venda(df):
    if df is None or df.empty:
        print("Não há dados para gerar o gráfico de Preço de Venda (Linha).")
        return

    plt.figure(figsize=(10, 6))
    sns.lineplot(x='NOME', y='PRECO_VENDA', data=df, marker='o', sort=False)
    plt.title('Preço de Venda por Produto (Gráfico de Linha)')
    plt.xlabel('Produto')
    plt.ylabel('Preço de Venda (R$)')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("grafico_preco_venda_linha.png")
    plt.close()

def gerar_grafico_estoque_barras(df):
    if df is None or df.empty:
        print("Não há dados para gerar o gráfico de Quantidade em Estoque (Barras).")
        return

    plt.figure(figsize=(12, 7))
    sns.barplot(x='NOME', y='QUANTIDADE_ESTOQUE', data=df, palette='viridis', hue='NOME', legend=False)
    plt.title('Quantidade em Estoque por Produto (Gráfico de Barras)')
    plt.xlabel('Produto')
    plt.ylabel('Quantidade em Estoque')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("grafico_estoque_barras.png")
    plt.close()

def gerar_grafico_lollipop_preco_venda(df):
    if df is None or df.empty:
        print("Não há dados para gerar o Gráfico Pirulito de Preço de Venda.")
        return

    plt.figure(figsize=(12, 7))

    df_sorted = df.sort_values(by='PRECO_VENDA', ascending=False)

    # Criar o gráfico Lollipop
    plt.hlines(y=df_sorted['NOME'], xmin=0, xmax=df_sorted['PRECO_VENDA'], color='skyblue', alpha=0.7)
    plt.plot(df_sorted['PRECO_VENDA'], df_sorted['NOME'], "o", markersize=10, color='blue', alpha=0.9)

    # Adicionar rótulos para os valores dos preços
    for i, row in df_sorted.iterrows():
        plt.text(row['PRECO_VENDA'] + 5, row['NOME'], f'R${row["PRECO_VENDA"]:.2f}', va='center', ha='left', fontsize=9)

    plt.title('Preço de Venda por Produto (Gráfico Pirulito)', fontsize=16)
    plt.xlabel('Preço de Venda (R$)', fontsize=12)
    plt.ylabel('Produto', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("grafico_lollipop_preco_venda.png")
    plt.close()

def gerar_histograma_estoque(df):
    if df is None or df.empty:
        print("Não há dados para gerar o Histograma de Quantidade em Estoque.")
        return

    plt.figure(figsize=(10, 6))
    # Usando histplot do seaborn para melhor visualização e KDE 
    sns.histplot(df['QUANTIDADE_ESTOQUE'], bins=5, kde=True, color='skyblue', edgecolor='black')
    plt.title('Distribuição da Quantidade em Estoque', fontsize=16)
    plt.xlabel('Quantidade em Estoque', fontsize=12)
    plt.ylabel('Número de Produtos', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("histograma_quantidade_estoque.png")
    plt.close()

if __name__ == "__main__":
    print("Certifique-se de que sua aplicação Spring Boot 'EstoqueVendasApplication' está em execução.")
    print(f"O servidor TCP do H2 (porta {H2_TCP_PORT}) deve estar ativo para que o script possa se conectar.")
    
    dados_produtos = conectar_e_extrair_dados()
    
    if dados_produtos is not None:
        gerar_grafico_estoque(dados_produtos) # Gráfico de Pizza 
        gerar_grafico_preco_venda(dados_produtos) # Gráfico de Linha 
        gerar_grafico_estoque_barras(dados_produtos) # Novo: Gráfico de Barras
        gerar_grafico_lollipop_preco_venda(dados_produtos) # Novo: Gráfico Pirulito
        gerar_histograma_estoque(dados_produtos) # Novo: Histograma

