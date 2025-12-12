import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def gerar_visualizacao_arvore(csv_file="arvore.csv", filename="arvore_diagnostico.png"):
    """
    Carrega o CSV, constrói um grafo e o visualiza como uma árvore hierárquica.
    Implementa regras de tamanho fixo para Raízes específicas e destaca a Raiz Foco.
    """
    print(f"--- Iniciando a visualização de '{csv_file}' ---")
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{csv_file}' não foi encontrado. Execute o código de simulação primeiro.")
        return
    except Exception as e:
        print(f"Erro ao carregar ou ler o CSV: {e}")
        return

    # 1. IDENTIFICANDO A RAIZ FOCO
    # Para a visualização, usaremos a Raiz que tem o maior score, 
    # pois é a que o código de simulação designou como a mais provável.
    raiz_foco_row = df[df['Tipo'] == 'Raiz'].sort_values(by='Valor', ascending=False).iloc[0]
    raiz_foco = raiz_foco_row['Nome_Nó']
    
    # Lista de Raízes que devem ter tamanho fixo (a partir de Dislexia)
    raizes_tamanho_fixo = {
        "Dislexia",
        "Altas Habilidades / Superdotação",
        "Prematuridade",
        "Baixo Peso ao Nascer",
        "Desenvolvimento neurobiológico atrasado"
    }
    TAMANHO_FIXO_RAIZ = 1200 # Tamanho fixo para o grupo 2
    
    # Cria o grafo e configura os nós (CÓDIGO DE CRIAÇÃO DO GRAFO OMITIDO PARA BREVIDADE, MAS INCLUÍDO NO ARQUIVO COMPLETO)
    # --- [CÓDIGO DE CRIAÇÃO DO GRAFO E ADIÇÃO DE NÓS/ARESTAS NÃO ALTERADO AQUI, ASSUMIDO CORRETO] ---
    
    G = nx.DiGraph()
    tipo_map = {'Sujeito': 0, 'Raiz': 1, 'Fruto': 2}
    sujeito_node = None 

    # 1.1 Configuração do Nó SUJEITO (Nível 0)
    sujeito_info = df[df['Tipo'] == 'Sujeito']
    if not sujeito_info.empty:
        sujeito_row = sujeito_info.iloc[0]
        sujeito_node = sujeito_row['Nome_Nó']
        G.add_node(sujeito_node)
        G.nodes[sujeito_node]['tipo'] = sujeito_row['Tipo']
        G.nodes[sujeito_node]['label'] = sujeito_row['Detalhes']
        G.nodes[sujeito_node]['subset'] = tipo_map['Sujeito']
        df_process = df[df['Tipo'] != 'Sujeito']
    else:
        print("Erro: Nó SUJEITO não encontrado no CSV.")
        return

    # 1.2 Adiciona Nós e Arestas (Raízes e Frutos)
    for index, row in df_process.iterrows():
        parent_node = row['Nó_Principal']
        child_node = row['Nome_Nó']
        node_type = row['Tipo']
        
        try:
            value = float(row['Valor'])
        except ValueError:
            value = 0.0

        if child_node not in G: G.add_node(child_node)
        G.nodes[child_node]['tipo'] = node_type
        G.nodes[child_node]['subset'] = tipo_map.get(node_type, 1)

        if parent_node not in G: G.add_node(parent_node) 
        
        if parent_node != child_node: G.add_edge(parent_node, child_node, weight=value)

        if node_type == 'Raiz':
            G.nodes[child_node]['score'] = value
            G.nodes[child_node]['prior'] = row['Prior_Mod_Idade']
        elif node_type == 'Fruto':
            G.nodes[child_node]['prob'] = value
            G.nodes[child_node]['descricao'] = row['Detalhes']
    
    # 2. Configuração de Layout e Plotagem (Mantida a tentativa de multipartite)
    
    nodes_to_remove = [n for n, data in G.nodes(data=True) if 'subset' not in data]
    G.remove_nodes_from(nodes_to_remove)

    try:
        pos = nx.multipartite_layout(G, subset_key='subset', align='vertical', scale=2.5)
    except Exception as e:
        print(f"Aviso: Layout multipartite falhou ({e}). Usando layout spring.")
        pos = nx.spring_layout(G, k=0.8, iterations=50) 

    for k in pos:
        pos[k][1] *= -1 

    # --- 3. Mapeamento de Cores e Tamanhos OTIMIZADO ---
    node_colors = []
    node_sizes = []
    node_labels = {}
    
    # Cálculo para Raízes que MANTÊM o dimensionamento variável (Síndromes, TEA, TDAH)
    raizes_variaveis = [G.nodes[n].get('score', 0) for n in G.nodes() if G.nodes[n].get('tipo') == 'Raiz' and n not in raizes_tamanho_fixo]
    max_raiz_score_variavel = max(raizes_variaveis) if raizes_variaveis else 1

    # Cálculo para Frutos (mantido o dimensionamento variável)
    all_probs = [G.nodes[n].get('prob', 0) for n in G.nodes() if G.nodes[n].get('tipo') == 'Fruto']
    max_fruto_prob = max(all_probs) if all_probs else 1
    
    for node in G.nodes():
        node_type = G.nodes[node].get('tipo')
        
        if node_type == 'Sujeito':
            node_colors.append('skyblue')
            node_sizes.append(2500)
            node_labels[node] = f"SUJEITO\n{G.nodes[node]['label']}"
            
        elif node_type == 'Raiz':
            score = G.nodes[node].get('score', 0)
            
            if node in raizes_tamanho_fixo:
                # REGRA 1 & 2: Tamanho fixo, cor escura apenas se for a Raiz Foco
                node_sizes.append(TAMANHO_FIXO_RAIZ)
                
                if node == raiz_foco:
                    # Raiz Foco neste grupo (COR ESCURA)
                    node_colors.append(plt.cm.Reds(0.9)) # Vermelho escuro
                    print(f"--> Destacando Raiz Foco (Fixa): {node}")
                else:
                    # Outras raízes fixas (COR PADRÃO)
                    node_colors.append(plt.cm.Reds(0.4)) # Vermelho claro/médio
            else:
                # Raízes com dimensionamento VARIÁVEL (Síndromes, TEA, TDAH)
                color_intensity = score / max_raiz_score_variavel if max_raiz_score_variavel > 0 else 0
                node_colors.append(plt.cm.Reds(color_intensity * 0.7 + 0.3))
                node_sizes.append(1000 + score * 1500)
                
                if node == raiz_foco:
                     # Se a Raiz Foco está no grupo variável (COR ESCURA)
                    node_colors[-1] = plt.cm.Reds(0.9) 
                    print(f"--> Destacando Raiz Foco (Variável): {node}")
                    
            node_labels[node] = f"{node}\nRisco: {score:.2f}"
            
        elif node_type == 'Fruto':
            prob = G.nodes[node].get('prob', 0)
            color_intensity = prob / max_fruto_prob if max_fruto_prob > 0 else 0
            node_colors.append(plt.cm.Greens(color_intensity * 0.7 + 0.3))
            node_sizes.append(1000 + prob * 1500)
            node_labels[node] = f"{node}\nProb: {prob:.2f}"
        else:
            node_colors.append('white')
            node_sizes.append(0) 

    # --- Desenho (Mantido o código anterior para desenho) ---
    
    plt.figure(figsize=(20, 16)) 
    
    draw_nodes = [n for i, n in enumerate(G.nodes()) if node_sizes[i] > 0]
    draw_colors = [c for i, c in enumerate(node_colors) if node_sizes[i] > 0]
    draw_sizes = [s for s in node_sizes if s > 0]
    
    draw_pos = {n: pos[n] for n in draw_nodes if n in pos}
    draw_labels = {n: node_labels[n] for n in draw_nodes}

    nx.draw_networkx_nodes(G, draw_pos, 
                           nodelist=draw_nodes,
                           node_color=draw_colors, 
                           node_size=draw_sizes, 
                           alpha=0.9, 
                           linewidths=1,
                           node_shape='o')
                           
    nx.draw_networkx_edges(G, pos, 
                           edge_color='gray', 
                           arrowsize=15,
                           width=1.0)
    
    nx.draw_networkx_labels(G, draw_pos, labels=draw_labels, font_size=9, font_weight='bold', bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))

    edge_labels = {
        (u, v): f"{G.edges[u, v]['weight']:.2f}" 
        for u, v in G.edges() 
    }
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=8, bbox=dict(facecolor='yellow', alpha=0.3, edgecolor='none'))

    plt.title(f"Modelo Hierárquico de Diagnóstico (Raízes e Frutos)\nSujeito: {sujeito_node}", fontsize=16)
    plt.axis('off') 
    plt.tight_layout()
    
    # --- 4. Salvar a Imagem ---
    try:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"\n✅ Visualização salva com sucesso em '{filename}'")
    except Exception as save_e:
        print(f"\n❌ Erro ao salvar a imagem: {save_e}. Exibindo na tela.")
        plt.show()
    finally:
        plt.close()
        
# Bloco de execução principal
if __name__ == "__main__":
    gerar_visualizacao_arvore(filename="arvore_diagnostico.png")