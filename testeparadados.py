import random
import math
import os
import csv
from collections import defaultdict
import time 

# NOVOS DADOS: Mapeamento de Idade/Início dos Diagnósticos 

IDADE_DATA = {
    "Raizes": {
        "Síndrome de Williams-Beuren" : {"inicio_tipico": 3, "janela" : 4},
        "Síndrome de Kinnefelter" : {"inicio_tipico": 14, "janela" : 6},
        "Síndrome de Dawn" : {"inicio_tipico" : 0, "janela" : 1},
        "TEA": {"inicio_tipico": 2, "janela": 3},
        "TDAH": {"inicio_tipico": 6, "janela": 4},
        "Dislexia": {"inicio_tipico": 7, "janela": 3},
        "Altas Habilidades / Superdotação": {"inicio_tipico": 8, "janela": 4},
        "Prematuridade": {"inicio_tipico": 0, "janela": 0},
        "Baixo Peso ao Nascer": {"inicio_tipico": 0, "janela": 0},
        "Desenvolvimento neurobiológico atrasado": {"inicio_tipico": 1, "janela": 2}
    },
    "Frutos": {
        "Depressao": {"inicio_tipico": 12, "janela": 4},
        "Distimia": {"inicio_tipico": 10, "janela": 5},
        "Ansiedade Generalizada": {"inicio_tipico": 8, "janela": 5},
        "Ansiedade Social": {"inicio_tipico": 10, "janela": 4},
        "Transtorno do Pânico": {"inicio_tipico": 15, "janela": 3},
        "Burnout": {"inicio_tipico": 16, "janela": 2},
        "Problemas de Autoestima": {"inicio_tipico": 6, "janela": 8},
        "Isolamento Social": {"inicio_tipico": 10, "janela": 5},
        "TAG infantil/adulto": {"inicio_tipico": 7, "janela": 6},
        "TOC" : {"inicio_tipico" :14 , "janela" : 5},
        "TOD" : {"inicio_tipico" :6 , "janela" : 4},
        "Transtorno Bipolar" : {"inicio_tipico" : 20, "janela" : 6},
        "Esquizofrenia" : {"inicio_tipico" : 22, "janela" : 5},
    }
}



# FUNÇÕES DE UTILIDADE E CARREGAMENTO DE DADOS 

def load_json(path):
  
    if path == "raizes.json":
        hipoteses_data = {
            "Síndrome de Williams-Beuren" : {
                "peso_base": 4,
                "tendencias": {
                    "Psicológicos": ["Hipersociabilidade indiscriminada", "Ansiedade elevada", "Dificuldades visuoespaciais", "Fobias específicas (sons)"],
                    "Biologicos": ["Traços faciais distintos", "Problemas cardíacos", "Desenvolvimento neurobiológico atrasado"],
                    "Ambientais": ["Ambiente superprotetor"],
                    "Individuais": ["Interação com pares adequada"]
                }
            },
            "Síndrome de Kinnefelter" : {
                "peso_base": 3,
                "tendencias": {
                    "Psicológicos": ["Comunicação limitada", "Tendência ao isolamento", "Dificuldade de leitura", "Imaturidade emocional"],
                    "Biologicos": ["Baixa aptidão física", "Desenvolvimento neurobiológico atrasado"],
                    "Ambientais": ["Bullying frequente"],
                    "Individuais": ["Ambiente afetivo"]
                }
            },
            "Síndrome de Dawn" : {
                "peso_base": 3,
                "tendencias": {
                    "Psicológicos": ["Dificuldade de regulação emocional", "Pensamento rígido", "Afetividade excessiva", "Atraso em marcos comportamentais"],
                    "Biologicos": ["Saúde fragilizada", "Traços faciais distintos", "Marco motor atrasado"],
                    "Ambientais": ["Pouca estimulação cognitiva"],
                    "Individuais": ["Apoio de cuidadores"]
                }
            },
            "TEA": {"peso_base": 4, "tendencias": {"Psicológicos": ["Dificuldade de regulação emocional", "Tendência ao isolamento", "Distorções cognitivas frequentes", "Comunicação limitada", "Apego a rotinas fixas", "Respostas sensoriais exageradas", "Dificuldade para interpretar sinais sociais", "Hipo ou hiper-reatividade emocional"], "Ambientais": ["Ambiente ruidoso ou caótico", "Ambiente escolar hostil", "Bullying frequente", "Negligência emocional", "Isolamento prolongado"], "Individuais": ["Rede de apoio", "Ambiente estável", "Interação com pares adequada"]}},
            "TDAH": {"peso_base": 3, "tendencias": {"Psicológicos": ["Impulsividade elevada", "Baixa capacidade de autocontrole", "Desatenção persistente", "Dificuldade em planejamento", "Oscilações de humor", "Desorganização acadêmica"], "Ambientais": ["Rotina desorganizada", "Ambiente ruidoso ou caótico", "Superexposição a telas", "Baixa supervisão adulta"], "Individuais": ["Rotina estável", "Sono regulado", "Acompanhamento pedagógico adequado"]}},
            "Dislexia": {"peso_base": 2, "tendencias": {"Escolares": ["Dificuldade de leitura", "Troca de letras", "Problemas de interpretação textual", "Desempenho irregular", "Baixo rendimento escolar", "Falta de acompanhamento pedagógico"], "Individuais": ["Acompanhamento pedagógico adequado", "Ambiente estável"]}},
            "Altas Habilidades / Superdotação": {"peso_base": 1, "tendencias": {"Psicológicos": ["Inteligência emocional reduzida", "Impulsividade elevada"], "Escolares": ["Clima escolar hostil", "Bullying frequente"], "Individuais": ["Ambiente afetivo", "Rede de apoio"]}},
            "Prematuridade": {"peso_base": 3, "tendencias": {"Biologicos": ["Saúde fragilizada", "Desenvolvimento neurobiológico atrasado", "Problemas de sono"], "Ambientais": ["Ambiente instável", "Baixa supervisão adulta"], "Individuais": ["Apoio de cuidadores", "Ambiente estável"]}},
            "Baixo Peso ao Nascer": {"peso_base": 3, "tendencias": {"Biologicos": ["Baixa aptidão física", "Sistema imunológico comprometido"], "Ambientais": ["Fatores biológicos associados", "Ambiente com poucos cuidados"], "Individuais": ["Boa alimentação", "Supervisão adequada"]}},
            "Desenvolvimento neurobiológico atrasado": {"peso_base": 4, "tendencias": {"Biologicos": ["Saúde fragilizada", "Baixa capacidade de autocontrole", "Marco motor atrasado"], "Ambientais": ["Ambiente instável", "Pouca estimulação cognitiva"], "Individuais": ["Ambiente afetivo", "Interação com cuidadores"]}}
        }
        return {"Raizes": hipoteses_data}
    
   
    elif path == "fatores_data":
        return {
            "Fatores": {
                "Sintomas": {"Psicológicos": {"Dificuldade de regulação emocional": 3, "Tendência ao isolamento": 2, "Distorções cognitivas frequentes": 2, "Impulsividade elevada": 3, "Baixa capacidade de autocontrole": 3, "Baixa autoeficácia": 2, "Habilidades sociais prejudicadas": 2, "Inteligência emocional reduzida": 1, "Estresse crônico": 2, "Ansiedade elevada": 3, "Irritabilidade frequente": 2, "Desatenção persistente": 3, "Hiperfoco irregular": 2, "Oscilações de humor": 2, "Baixa tolerância à frustração": 2, "Dificuldade em planejamento": 3, "Pensamento rígido": 2, "Comunicação limitada": 3, "Baixa iniciativa social": 2, "Dificuldade para interpretar sinais sociais": 3, "Respostas sensoriais exageradas": 3, "Hipo ou hiper-reatividade emocional": 2, "Atraso em marcos comportamentais": 2, "Preocupação excessiva": 2, "Apego a rotinas fixas": 2, "Hipersociabilidade indiscriminada": 2, "Imaturidade emocional": 2, "Afetividade excessiva": 1}, "Escolares": {"Baixo rendimento escolar": 3, "Dificuldade de leitura": 3, "Troca de letras": 2, "Problemas de interpretação textual": 3, "Rotinas escolares inconsistentes": 2, "Desempenho irregular": 2, "Falta de acompanhamento pedagógico": 2, "Dificuldade de memorização": 2, "Desorganização acadêmica": 2, "Evitação de atividades escolares": 2, "Dificuldade em seguir instruções": 3, "Dificuldades visuoespaciais": 2}, "Biológicos": {"Saúde fragilizada": 2, "Desenvolvimento neurobiológico atrasado": 3, "Baixa aptidão física": 1, "Sistema imunológico comprometido": 2, "Prematuridade prévia": 3, "Baixo peso ao nascer": 3, "Marco motor atrasado": 2, "Dificuldade alimentar": 2, "Problemas de sono": 2, "Traços faciais distintos": 2, "Problemas cardíacos": 3}},
                "Fatores_Risco": {"Ambientais": {"Ambiente ruidoso ou caótico": -2, "Rotina desorganizada": -2, "Ambiente instável": -2, "Exposição a conflitos constantes": -3, "Ausência de rotina": -2, "Pouca estimulação cognitiva": -2, "Negligência emocional": -3, "Ambiente escolar hostil": -3, "Bullying frequente": -3, "Superexposição a telas": -2, "Baixa supervisão adulta": -2, "Ambiente superprotetor": -1}, "Familiares": {"Histórico familiar de TDAH": 3, "Histórico familiar de TEA": 3, "Histórico familiar de ansiedade": 3, "Pais com baixa responsividade emocional": -2, "Conflitos familiares constantes": -3, "Separação traumática": -2, "Pais com sintomas internalizantes": -1, "Ambiente crítico e rígido": -2}, "Sociais": {"Dificuldade de socialização": 2, "Isolamento prolongado": 2, "Rejeição de pares": 3, "Pouca rede de apoio": -2, "Falta de atividades sociais estruturadas": -1, "Experiências sociais negativas repetidas": 2}},
                "Fatores_Protecao": {"Individuais": {"Rede de apoio": 2, "Sono regulado": 2, "Ambiente estável": 2, "Interação com pares adequada": 2, "Autoestima preservada": 2, "Estratégias de coping": 2, "Boa alimentação": 1, "Capacidade de adaptação": 1}, "Ambientais": {"Rotina estável": 2, "Ambiente afetivo": 2, "Acompanhamento pedagógico adequado": 2, "Baixo nível de estresse familiar": 2, "Apoio de cuidadores": 2, "Estilo parental responsivo": 1}}
            }
        }
    
    # DADOS frutos.json (Atualizado com novos frutos)
    elif path == "frutos.json":
        return {
            "Frutos": {
                "Depressao": {"sensibilidade": 3, "gatilhos_comuns": ["Estresse crônico", "Tendência ao isolamento", "Ambiente instável", "Negligência emocional", "Bullying frequente"], "descricao": "Queda persistente de humor, baixa energia e perda de interesse."},
                "Distimia": {"sensibilidade": 2, "gatilhos_comuns": ["Experiências negativas acumuladas", "Vida desestruturada", "Personalidade vulnerável ao estresse"], "descricao": "Humor deprimido crônico e moderado por longos períodos."},
                "Ansiedade Generalizada": {"sensibilidade": 3, "gatilhos_comuns": ["Alta exposicao ao estresse", "Ambiente ruidoso ou caótico", "Rotinas imprevisíveis", "Situações imprevisíveis"], "descricao": "Preocupação excessiva e constante sem causa aparente."},
                "Ansiedade Social": {"sensibilidade": 2, "gatilhos_comuns": ["Bullying frequente", "Tendência ao isolamento", "Habilidades sociais prejudicadas"], "descricao": "Medo intenso de interação social e avaliação negativa."},
                "Transtorno do Pânico": {"sensibilidade": 1, "gatilhos_comuns": ["Eventos traumáticos recorrentes", "Ambiente caótico"], "descricao": "Crises súbitas de medo intenso acompanhadas de sintomas físicos."},
                "Burnout": {"sensibilidade": 2, "gatilhos_comuns": ["Estresse crônico", "Baixa autoeficácia", "Alta exigência escolar"], "descricao": "Exaustão física e mental por sobrecarga."},
                "Problemas de Autoestima": {"sensibilidade": 1, "gatilhos_comuns": ["Baixo rendimento escolar", "Conflitos familiares constantes", "Experiências negativas acumuladas"], "descricao": "Autoimagem fragilizada e insegurança persistente."},
                "Isolamento Social": {"sensibilidade": 2, "gatilhos_comuns": ["Bullying frequente", "Tendência ao isolamento", "Vida desestruturada"], "descricao": "Retraimento severo da convivência social."},
                "TAG infantil/adulto": {"sensibilidade": 3, "gatilhos_comuns": ["Falta de rotina de sono", "Família disfuncional", "Eventos traumáticos"], "descricao": "Ansiedade persistente ao longo da vida, iniciando na infância."},
                "TOC": {"sensibilidade": 2, "gatilhos_comuns": ["Estresse agudo", "Eventos traumáticos", "Histórico familiar"], "descricao": "Presença de obsessões (pensamentos intrusivos) e/ou compulsões (comportamentos repetitivos)."},
                "TOD": {"sensibilidade": 3, "gatilhos_comuns": ["Conflitos familiares", "Disciplina inconsistente", "Exposição à violência ou negligência"], "descricao": "Padrão de humor irritável, comportamento argumentativo/desafiador ou vingativo."},
                "Transtorno Bipolar": {"sensibilidade": 1, "gatilhos_comuns": ["Privação de sono", "Uso de substâncias", "Estresse intenso"], "descricao": "Alterações de humor extremas, variando entre episódios de mania/hipomania e depressão."},
                "Esquizofrenia": {"sensibilidade": 1, "gatilhos_comuns": ["Uso de substâncias (maconha, estimulantes)", "Estresse severo", "Eventos traumáticos"], "descricao": "Transtorno que afeta a capacidade de pensar, sentir e se comportar com clareza (sintomas psicóticos)."}
            }
        }
        
    if path == "idade_data":
        return IDADE_DATA
    
    return {}

# Funções Matemáticas e de Normalização (Mantidas)
def normalizar_dict(d):
    total = sum(d.values())
    if total == 0:
        n = len(d)
        return {k: 1.0/n for k in d}
    return {k: v / total for k, v in d.items()}

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def peso_to_likelihood(peso, scale=3.0):
    p = sigmoid(peso / scale)
    return min(max(p, 0.01), 0.99)


# INICIALIZAÇÃO E CARREGAMENTO DE DADOS 

raizes = load_json("raizes.json")
fatores_data = load_json("fatores_data")
frutos_data = load_json("frutos.json")
idade_data = load_json("idade_data") 

positivos = {}
negativos = {}

F = fatores_data.get("Fatores", {})
for cat_group, sign in [("Sintomas", "positivo"), ("Fatores_Risco", "positivo"), ("Fatores_Protecao", "protecao")]:
    group = F.get(cat_group, {})
    for subcat, items in group.items():
        for nome, info in items.items():
            entry = {"peso": info if isinstance(info, int) else info.get("peso", 1), "prob": {}, "ausencia": {}, "categoria": subcat, "raw_group": cat_group}
            if sign == "positivo":
                positivos.setdefault(subcat, {})[nome] = entry
            else:
                negativos.setdefault(subcat, {})[nome] = entry

hipoteses = list(raizes["Raizes"].keys())
priors = normalizar_dict({h: 1.0 for h in hipoteses}) 


# FUNÇÕES ESSENCIAIS 

def ajustar_prior_para_raiz_unica(raiz_escolhida, priors_in, prior_boost=0.99999):
    nova = {}
    n = len(priors_in)
    nova[raiz_escolhida] = prior_boost
    prior_restante = 1.0 - prior_boost
    if n > 1:
        peso_residual = prior_restante / (n - 1)
        for h in priors_in:
            if h != raiz_escolhida: nova[h] = peso_residual
    else:
        return {raiz_escolhida: 1.0}
    return normalizar_dict(nova)

def calcular_probabilidades_selecao_raiz(raizes_data, nivel_vulnerabilidade):
    pesos = {}
    for nome, info in raizes_data["Raizes"].items():
        peso_base = info["peso_base"]
        peso_raw = peso_base * nivel_vulnerabilidade 
        ruido = max(0.1, random.gauss(0.5, 1.0))
        pesos[nome] = peso_raw * (1 + ruido) 
    return normalizar_dict(pesos)

def calcular_fator_idade(idade_atual, nome_diagnostico, tipo="Raizes"):
    dados_idade = IDADE_DATA.get(tipo, {})
    info_idade = dados_idade.get(nome_diagnostico)
    if not info_idade: return 1.0 
    inicio = info_idade["inicio_tipico"]
    janela = max(1, info_idade["janela"]) 
    if info_idade["janela"] == 0: return 1.0 
    desvio = idade_atual - inicio
    argumento_exp = -0.5 * (desvio / janela)**2
    fia = math.exp(argumento_exp)
    return max(0.1, fia) 

def sortear_idade_focada(raiz_foco, idade_min_abs=1, idade_max_abs=35):
    info_idade = IDADE_DATA["Raizes"].get(raiz_foco)
    
    if not info_idade or info_idade["janela"] == 0:
        return random.randint(idade_min_abs, idade_max_abs)
    
    inicio = info_idade["inicio_tipico"]
    janela = info_idade["janela"] 
    
    # Usa a lógica do código mais recente para sortear
    idade_raw = random.gauss(inicio, janela) 
    
    idade_final = max(idade_min_abs, min(idade_max_abs, round(idade_raw)))
    
    return idade_final

def coletar_itens_raiz(raiz_info):
    itens = set()
    for v in raiz_info.get("tendencias", {}).values():
        if isinstance(v, list): itens.update(v)
    return itens

def amostrar_evidencias_focadas(raiz_foco, n_present, n_absent, foco_ratio=0.6):
    pool_total = []
    for cat, itens in positivos.items():
        for nome, info in itens.items(): pool_total.append(("positivo", cat, nome, info))
    for cat, itens in negativos.items():
        for nome, info in itens.items():
            tipo = "protecao" if info.get("raw_group") == "Fatores_Protecao" else "negativo"
            pool_total.append((tipo, cat, nome, info))

    itens_foco = coletar_itens_raiz(raizes["Raizes"][raiz_foco])
    pool_foco = [item for item in pool_total if item[2] in itens_foco]
    pool_geral = pool_total

    n_foco_base = int(n_present * foco_ratio)
    n_aleatorio_base = n_present - n_foco_base
    
    # Adicionando ruído na amostragem
    n_foco = max(1, int(n_foco_base * random.uniform(0.8, 1.2)))
    n_aleatorio = max(0, int(n_aleatorio_base * random.uniform(0.8, 1.2)))
    n_present = n_foco + n_aleatorio
    n_absent = max(1, int(n_absent * random.uniform(0.8, 1.2)))
    
    present, chosen = [], set()
    for _ in range(n_foco):
        if not pool_foco: break
        item = random.choice(pool_foco)
        key = (item[1], item[2])
        if key in chosen: continue
        chosen.add(key)
        present.append((True, item[0], item[1], item[2], item[3]))
        pool_foco.remove(item)

    for _ in range(n_aleatorio):
        item = random.choice(pool_geral)
        key = (item[1], item[2])
        if key in chosen: continue
        chosen.add(key)
        present.append((True, item[0], item[1], item[2], item[3]))
        
    absent, chosen_abs = [], set()
    for _ in range(n_absent):
        item = random.choice(pool_total)
        key = (item[1], item[2])
        if key in chosen_abs or key in chosen: continue
        chosen_abs.add(key)
        absent.append((False, item[0], item[1], item[2], item[3]))
        
    random.shuffle(present + absent)
    return present + absent

def likelihood_por_raiz(hipoteses, info, presença=True):
    peso = info.get("peso", 1) if isinstance(info, dict) else info
    lik = {}
    for r in hipoteses:
        lik[r] = peso_to_likelihood(peso) if presença else 1 - peso_to_likelihood(peso)
    return lik

def aplicar_bayes(prior, evidencia_likelihood):
    numeradores = {r: prior[r] * evidencia_likelihood[r] for r in prior}
    return normalizar_dict(numeradores)
    
def calcular_risco_por_hipotese(hipoteses, evidencias, priors, ruido_experiencia_max=0.5):
    posterior = dict(priors)
    risco_scores = {r: 0.0 for r in hipoteses}
    for (presenca, tipo, cat, nome, info) in evidencias:
        lik = likelihood_por_raiz(hipoteses, info, presença=presenca)
        posterior = aplicar_bayes(posterior, lik)
        peso_raw = info.get("peso", 0) if isinstance(info, dict) else info
        ruido_exp = random.uniform(-ruido_experiencia_max, ruido_experiencia_max)
        peso_modulado = max(0.1, peso_raw + ruido_exp) 
        for r in hipoteses:
            ajuste = 0
            if tipo == "protecao" and presenca: ajuste = -peso_modulado * posterior[r] 
            elif tipo != "protecao" and presenca: ajuste = peso_modulado * posterior[r]  
            elif tipo == "protecao" and not presenca: ajuste = peso_modulado * posterior[r]  
            else: ajuste = -peso_modulado * posterior[r] 
            risco_scores[r] += ajuste
    return posterior, risco_scores

def calcular_probabilidade_frutos(risco_scores_raizes, raizes_data, frutos_data, idade_sujeito):
    frutos = frutos_data.get("Frutos", {})
    probabilidades = {}
    mapa_raiz_para_fruto = {f_nome: {} for f_nome in frutos}
    
    for r_nome, r_info in raizes_data["Raizes"].items():
        r_itens = coletar_itens_raiz(r_info)
        for f_nome, f_info in frutos.items():
            f_gatilhos = set(f_info["gatilhos_comuns"])
            interseccao = len(r_itens.intersection(f_gatilhos))
            mapa_raiz_para_fruto[f_nome][r_nome] = interseccao

    for f_nome, f_info in frutos.items():
        sensibilidade = f_info["sensibilidade"]
        contribuicao_total = 0.0
        fia_fruto = calcular_fator_idade(idade_sujeito, f_nome, tipo="Frutos") 
        max_interseccao = max(mapa_raiz_para_fruto[f_nome].values()) if mapa_raiz_para_fruto[f_nome] else 1
        max_interseccao = max(1, max_interseccao)
        
        for r_nome, r_score in risco_scores_raizes.items():
            interseccao = mapa_raiz_para_fruto[f_nome].get(r_nome, 0)
            peso_raiz = interseccao / max_interseccao
            contribuicao_total += r_score * peso_raiz
            
        contribuicao_total *= fia_fruto 
            
        scale_factor = 3.0
        argumento = (contribuicao_total * sensibilidade) / scale_factor
        prob_final = sigmoid(argumento)
        
        probabilidades[f_nome] = max(min(prob_final, 0.99), 0.01)

    return normalizar_dict(probabilidades)


# FLUXO DA SIMULAÇÃO INDIVIDUAL

def simular_caso_individual(n_present_base=15, n_absent_base=10):
    """
    Roda a simulação completa para um único indivíduo.
    """
    
    # Define a semente aleatória dentro de cada caso para garantir independência
    random.seed(os.urandom(16))
    
    # 1. Sortear Vulnerabilidade e Raiz Foco
    NIVEL_VULNERABILIDADE = random.randint(1, 5) 
    raizes_disponiveis = list(raizes["Raizes"].keys())
    probabilidades_selecao = calcular_probabilidades_selecao_raiz(raizes, NIVEL_VULNERABILIDADE)
    pesos_selecao = [probabilidades_selecao[r] for r in raizes_disponiveis]
    raiz_foco = random.choices(raizes_disponiveis, weights=pesos_selecao, k=1)[0]
    
    # 2. Sortear Idade Focada na Raiz
    idade_sujeito = sortear_idade_focada(raiz_foco)
    
    # 3. Modulação de Priors pela Idade e Foco
    priors_mod = dict(priors)
    for r in priors_mod:
        fia_r = calcular_fator_idade(idade_sujeito, r, tipo="Raizes")
        priors_mod[r] *= fia_r
        
    priors_mod = normalizar_dict(priors_mod) 
    priors_cond = ajustar_prior_para_raiz_unica(raiz_foco, priors_mod)

    # 4. Amostrar evidências
    evidencias = amostrar_evidencias_focadas(raiz_foco, n_present_base, n_absent_base, foco_ratio=0.6) 

    # 5. Calcular Scores de Risco
    _, risco_scores = calcular_risco_por_hipotese(hipoteses, evidencias, priors_cond)
    
    # 6. Calcular Probabilidade dos Frutos
    probabilidade_frutos = calcular_probabilidade_frutos(risco_scores, raizes, frutos_data, idade_sujeito)
    
    # 7. Determinar o Fruto Final 
    maior_fruto = max(probabilidade_frutos, key=lambda k: probabilidade_frutos[k])
    
    return {
       
        "id": int(time.time() * 100000) + random.randint(1, 99999), 
        "idade": idade_sujeito,
        "vulnerabilidade": NIVEL_VULNERABILIDADE,
        "raiz_inicial": raiz_foco,
        "fruto_final": maior_fruto,
        "probabilidade_fruto": round(probabilidade_frutos[maior_fruto], 4)
    }


# EXECUÇÃO DA SIMULAÇÃO E SAÍDA CSV 

def executar_simulacao_e_salvar(num_individuos=700, nome_arquivo="results_simulation.csv"):
    """
    Executa a simulação para N indivíduos e salva os dados no arquivo CSV.
    """
    
    start_time = time.time()
    
    print(f"Iniciando simulação de Monte Carlo para **{num_individuos} indivíduos**...")
    print(f"Saída será salva em: **{nome_arquivo}**")
    
    # Cabeçalho do CSV
    fieldnames = ["id", "idade", "vulnerabilidade", "raiz_inicial", "fruto_final", "probabilidade_fruto"]
    
    # Abre o arquivo CSV para escrita
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(num_individuos):
            try:
                # Chama a função de simulação individual
                resultado = simular_caso_individual()
                writer.writerow(resultado)
                if (i + 1) % 50 == 0:
                    print(f" Processado {i + 1}/{num_individuos} casos.")
            except Exception as e:
                print(f" Erro ao processar o caso {i+1}: {e}. Pulando.")
                continue

    end_time = time.time()
    duration = round(end_time - start_time, 2)
    print(f"\n🎉 Simulação concluída em {duration} segundos.")
    print(f"Resultados prontos para análise 3D em '{nome_arquivo}'.")

if __name__ == "__main__":
    
    executar_simulacao_e_salvar(num_individuos=700)
