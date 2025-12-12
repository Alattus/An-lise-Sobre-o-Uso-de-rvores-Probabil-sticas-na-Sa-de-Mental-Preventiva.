import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ======================================================
# CONFIGURAÇÃO DE VISUALIZAÇÃO 3D
# ======================================================
def gerar_grafo_molecular_3d(nome_arquivo_csv="results_simulation.csv"):
    """
    Carrega os dados da simulação e gera um grafo 3D interativo
    onde os eixos representam as dimensões do estudo: Idade, Frutos e Raízes.
    """
    try:
        df = pd.read_csv(nome_arquivo_csv)
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{nome_arquivo_csv}' não encontrado.")
        print("Certifique-se de que 'simulacao_data.py' foi executado primeiro.")
        return

    # --- Mapeamento para Eixos X, Y, Z ---
    
    # Eixo Y: Idade (Contínua)
    y_data = df['idade']
    
    # Eixo Z: Raiz Inicial (Categórica)
    # Plotly trata automaticamente variáveis categóricas para Z
    z_data = df['raiz_inicial']
    
    # Eixo X: Fruto Final (Categórica)
    # Plotly trata automaticamente variáveis categóricas para X
    x_data = df['fruto_final']

    # --- Geração do Grafo de Dispersão 3D ---
    
    fig = px.scatter_3d(
        df, 
        x='fruto_final',
        y='idade',
        z='raiz_inicial',
        color='raiz_inicial',  # Colore os pontos pela Raiz Inicial
        size='probabilidade_fruto', # O tamanho do ponto reflete a força da ligação (probabilidade)
        opacity=0.8,
        symbol='vulnerabilidade', # Usa o nível de vulnerabilidade como forma
        title='🧬 Grafo Molecular 3D: Relações Raízes (Z), Idade (Y) e Frutos (X) 🍎'
    )
    
    # --- Configurações do Layout para um aspecto "molecular" ---
    
    fig.update_layout(
        scene=dict(
            xaxis=dict(title='Fruto Final (Eixo X)'),
            yaxis=dict(title='Idade (Anos) (Eixo Y)'),
            zaxis=dict(title='Raiz Inicial (Eixo Z)'),
            bgcolor='white' # Fundo branco para melhor contraste
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )

    # --- Adicionar Arestas (Linhas de Ligação - Opcional, mas dá o aspecto de molécula) ---
    # Para simular arestas, podemos ligar pontos com a mesma Raiz Inicial.
    
    for raiz in df['raiz_inicial'].unique():
        sub_df = df[df['raiz_inicial'] == raiz]
        
        # Cria uma linha que conecta os pontos da mesma Raiz
        # Note: A ordem dos pontos em sub_df define a ordem da linha.
        line_data = go.Scatter3d(
            x=sub_df['fruto_final'],
            y=sub_df['idade'],
            z=sub_df['raiz_inicial'],
            mode='lines',
            line=dict(color='gray', width=1),
            name=f'Arestas: {raiz}',
            hoverinfo='none'
        )
        fig.add_trace(line_data)

    # Mostrar o gráfico interativo
    fig.show()

if __name__ == "__main__":
    # Certifique-se de que o arquivo CSV foi gerado pela parte 1!
    gerar_grafo_molecular_3d()
# Salve este código como visualizacao_3d.py