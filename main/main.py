import json
import random
import math
import os
import csv 

NIVEL_VULNERABILIDADE_FIXO = 3
IDADE_SUJEITO_FIXA = 12

IDADE_DATA = {
    "Raizes": {
        "Neurotipico": {"inicio_tipico": 0, "janela": 0},
        "Síndrome de Williams-Beuren" : {"inicio_tipico": 3, "janela" : 4},
        "Síndrome de Kinnelfeter" : {"inicio_tipico": 14, "janela" : 6},
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
        "TOC" : {"inicio_tipico" :14 , "janela" : 5},
        "TOD" : {"inicio_tipico" :6 , "janela" : 4},
        "Transtorno Bipolar" : {"inicio_tipico" : 20, "janela" : 6},
        "Esquizofrenia" : {"inicio_tipico" : 22, "janela": 5},
        "TAG infantil/adulto": {"inicio_tipico": 7, "janela": 6},
    }
}

def load_json(path):
    if path == "raizes.json":
        hipoteses_data = {
            "Neurotipico": {
                "peso_base": 6,
                "tendencias": {
                    "Psicológicos": ["Boa capacidade de autocontrole", "Capacidade de adaptação"],
                    "Ambientais": [],
                    "Individuais": []
                }
            },
            "TEA": {
                "peso_base": 4,
                "tendencias": {
                    "Psicológicos": ["Dificuldade para interpretar sinais sociais", "Apego a rotinas fixas", "Respostas sensoriais exageradas", "Comunicação limitada", "Hiperfoco irregular", "Estereotipias motoras"],
                    "Ambientais": ["Ambiente ruidoso ou caótico", "Bullying frequente", "Isolamento prolongado"],
                    "Individuais": ["Atraso na fala", "Interesses restritos"]
                }
            },
            "TDAH": {
                "peso_base": 4, 
                "tendencias": {
                    "Psicológicos": ["Impulsividade elevada", "Desatenção persistente", "Dificuldade em planejamento", "Baixa capacidade de autocontrole", "Agitação motora excessiva", "Dificuldade em esperar a vez"],
                    "Ambientais": ["Ambiente escolar hostil", "Rotina desorganizada", "Superexposição a telas"],
                    "Individuais": ["Esquecimento frequente", "Dificuldade de organização"]
                }
            },
            "Síndrome de Williams-Beuren" : {
                "peso_base": 4,
                    "tendencias": {
                        "Psicológicos": ["Hipersociabilidade indiscriminada", "Ansiedade elevada", "Dificuldades visuoespaciais", "Fobias específicas (sons)"],
                        "Biológicos": ["Traços faciais distintos", "Problemas cardíacos", "Atraso no desenvolvimento"],
                        "Ambientais": ["Ambiente superprotetor"]
                    }
            },
            "Síndrome de Dawn" : {
                "peso_base": 3,
                    "tendencias": {
                        "Psicológicos": ["Deficiência intelectual", "Teimosia ou rigidez", "Afetividade excessiva", "Lentidão no processamento"],
                        "Biológicos": ["Hipotonia", "Envelhecimento precoce", "Traços faciais distintos"],
                        "Ambientais": ["Estimulação precoce (fator proteção)"]
                    }
            },
            "Síndrome de Kinnelfeter" : {
                "peso_base": 3,
                    "tendencias": {
                        "Psicológicos": ["Atraso de linguagem", "Timidez excessiva", "Dificuldade de leitura", "Imaturidade emocional"],
                        "Biológicos": ["Estatura alta", "Hipogonadismo/Baixa testosterona", "Baixa energia"],
                        "Ambientais": ["Bullying frequente"]
                    }
            },
            "Dislexia": {
                "peso_base": 2,
                "tendencias": {
                    "Escolares": ["Dificuldade de leitura", "Troca de letras", "Problemas de interpretação textual", "Lentidão na leitura", "Evitação de atividades escolares"],
                    "Individuais": ["Histórico familiar de dificuldades de aprendizagem"]
                }
            },
            "Altas Habilidades / Superdotação": {
                "peso_base": 1,
                "tendencias": {
                    "Psicológicos": ["Inteligência emocional reduzida", "Sensibilidade emocional elevada", "Perfeccionismo extremo", "Questionamento de autoridade"],
                    "Escolares": ["Tédio escolar", "Desempenho irregular"],
                    "Individuais": ["Vocabulário avançado", "Aprendizado rápido"]
                }
            },
            "Prematuridade": {
                "peso_base": 3,
                "tendencias": {
                    "Biologicos": ["Saúde fragilizada", "Desenvolvimento neurobiológico atrasado", "Problemas de sono", "Sensibilidade sensorial"],
                    "Ambientais": ["Internações frequentes na infância"],
                    "Individuais": ["Apoio de cuidadores"]
                }
            },
            "Baixo Peso ao Nascer": {
                "peso_base": 3,
                "tendencias": {
                    "Biologicos": ["Baixa aptidão física", "Imunidade baixa", "Atraso no crescimento"],
                    "Ambientais": ["Fatores biológicos associados"],
                    "Individuais": ["Necessidade de suporte nutricional"]
                }
            },
            "Desenvolvimento neurobiológico atrasado": {
                "peso_base": 4,
                "tendencias": {
                    "Biologicos": ["Marco motor atrasado", "Dificuldade na coordenação motora", "Atraso na fala"],
                    "Ambientais": ["Pouca estimulação cognitiva"],
                    "Individuais": ["Dificuldade de aprendizagem global"]
                }
            }
        }
        return {"Raizes": hipoteses_data}
        
    elif path == "fatores_data":
        return {
            "Fatores": {
                "Sintomas": {
                    "Psicológicos": {
                        "Impulsividade elevada": 5, 
                        "Baixa capacidade de autocontrole": 4,
                        "Desatenção persistente": 5, 
                        "Hiperfoco irregular": 3,
                        "Dificuldade de regulação emocional": 4, 
                        "Tendência ao isolamento": 4, 
                        "Distorções cognitivas frequentes": 3,
                        "Habilidades sociais prejudicadas": 4, 
                        "Ansiedade elevada": 4,
                        "Irritabilidade frequente": 3,
                        "Oscilações de humor": 4, 
                        "Pensamento rígido": 3, 
                        "Apego a rotinas fixas": 4, 
                        "Respostas sensoriais exageradas": 5, 
                        "Comunicação limitada": 4,
                        "Dificuldade para interpretar sinais sociais": 5, 
                        "Baixa autoeficácia": 3,
                        "Perfeccionismo extremo": 3,
                        "Agitação motora excessiva": 4
                    },
                    "Escolares": {
                        "Baixo rendimento escolar": 3,
                        "Dificuldade de leitura": 5, 
                        "Troca de letras": 4,
                        "Problemas de interpretação textual": 4,
                        "Desorganização acadêmica": 3,
                        "Evitação de atividades escolares": 3,
                        "Dificuldade de memorização": 3,
                        "Tédio escolar": 2
                    },
                    "Biológicos": {
                        "Desenvolvimento neurobiológico atrasado": 4,
                        "Marco motor atrasado": 4,
                        "Atraso na fala": 5, 
                        "Problemas de sono": 3,
                        "Saúde fragilizada": 2,
                        "Sensibilidade sensorial": 4
                    }
                },
                "Fatores_Risco": {
                    "Ambientais": {
                        "Bullying frequente": -5, 
                        "Negligência emocional": -5, 
                        "Ambiente escolar hostil": -4,
                        "Ambiente ruidoso ou caótico": -3,
                        "Rotina desorganizada": -3,
                        "Exposição a conflitos constantes": -4,
                        "Superexposição a telas": -2,
                        "Baixa supervisão adulta": -3
                    },
                    "Familiares": {
                        "Histórico familiar de transtorno mental": 5, 
                        "Pais com baixa responsividade emocional": -4,
                        "Conflitos familiares constantes": -4,
                        "Separação traumática": -3,
                        "Ambiente crítico e rígido": -3,
                        "Abuso físico ou psicológico": -5 
                    },
                    "Sociais": {
                        "Rejeição de pares": -4,
                        "Isolamento prolongado": -4,
                        "Pouca rede de apoio": -3,
                        "Dificuldade de socialização": 3 
                    }
                },
                "Fatores_Protecao": {
                    "Individuais": {
                        "Rede de apoio": 5, 
                        "Autoestima preservada": 4,
                        "Estratégias de coping": 4,
                        "Inteligência acima da média": 2, 
                        "Capacidade de adaptação": 3
                    },
                    "Ambientais": {
                        "Ambiente afetivo": 5, 
                        "Rotina estável": 4,
                        "Acompanhamento pedagógico adequado": 4,
                        "Estilo parental responsivo": 4
                    }
                }
            }
        }
    elif path == "frutos.json":
        return {
            "Frutos": {
                "Depressao": {
                    "sensibilidade": 3,
                    "gatilhos_comuns": ["Tendência ao isolamento", "Baixa autoeficácia", "Bullying frequente", "Negligência emocional", "Ambiente escolar hostil", "Histórico familiar de transtorno mental"],
                    "descricao": "Queda persistente de humor, anedonia e desesperança."
                },
                "Ansiedade Generalizada": {
                    "sensibilidade": 3,
                    "gatilhos_comuns": ["Ansiedade elevada", "Preocupação excessiva", "Ambiente ruidoso ou caótico", "Conflitos familiares constantes", "Perfeccionismo extremo", "Histórico familiar de transtorno mental"],
                    "descricao": "Preocupação excessiva e incontrolável sobre diversos eventos."
                },
                "Ansiedade Social": {
                    "sensibilidade": 2,
                    "gatilhos_comuns": ["Bullying frequente", "Rejeição de pares", "Habilidades sociais prejudicadas", "Timidez excessiva", "Dificuldade para interpretar sinais sociais"],
                    "descricao": "Medo intenso de julgamento em situações sociais."
                },
                "Burnout": {
                    "sensibilidade": 2,
                    "gatilhos_comuns": ["Estresse crônico", "Alta exigência escolar", "Perfeccionismo extremo", "Baixa autoeficácia", "Ambiente crítico e rígido"],
                    "descricao": "Exaustão física e mental ligada a demandas de desempenho."
                },
                "Problemas de Autoestima": {
                    "sensibilidade": 1,
                    "gatilhos_comuns": ["Baixo rendimento escolar", "Rejeição de pares", "Bullying frequente", "Ambiente crítico e rígido", "Distorções cognitivas frequentes"],
                    "descricao": "Visão negativa persistente sobre si mesmo."
                },
                "TOC": {
                    "sensibilidade": 2,
                    "gatilhos_comuns": ["Pensamento rígido", "Apego a rotinas fixas", "Ansiedade elevada", "Histórico familiar de transtorno mental", "Perfeccionismo extremo"],
                    "descricao": "Obsessões e compulsões que consomem tempo."
                },
                "TOD": {
                    "sensibilidade": 3,
                    "gatilhos_comuns": ["Impulsividade elevada", "Irritabilidade frequente", "Questionamento de autoridade", "Conflitos familiares constantes", "Disciplina inconsistente"],
                    "descricao": "Padrão persistente de comportamento desafiador e hostil."
                },
                "Transtorno Bipolar": {
                    "sensibilidade": 1,
                    "gatilhos_comuns": ["Oscilações de humor", "Histórico familiar de transtorno mental", "Impulsividade elevada", "Problemas de sono", "Abuso físico ou psicológico"],
                    "descricao": "Alternância entre episódios depressivos e maníacos/hipomaníacos."
                },
                "Esquizofrenia": {
                    "sensibilidade": 1,
                    "gatilhos_comuns": ["Distorções cognitivas frequentes", "Isolamento prolongado", "Histórico familiar de transtorno mental", "Uso de substâncias"],
                    "descricao": "Perda de contato com a realidade (psicose)."
                },
                "TDAH (Comorbidade Cruzada)": {
                     "sensibilidade": 3,
                     "gatilhos_comuns": ["Desatenção persistente", "Agitação motora excessiva", "Impulsividade elevada", "Histórico familiar de transtorno mental"],
                     "descricao": "Persistência ou agravamento dos sintomas de TDAH na vida adulta."
                }
            }
        }
    
    if path == "idade_data":
        return IDADE_DATA
    
    return {}

def normalizar_dict(d):
    total = sum(d.values())
    if total == 0:
        n = len(d)
        return {k: 1.0/n for k in d}
    return {k: v / total for k, v in d.items()}

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def peso_to_likelihood(peso, scale=3.0):
    peso_abs = abs(peso)
    p = sigmoid(peso_abs / scale)
    return min(max(p, 0.01), 0.99)

raizes = load_json("raizes.json")
fatores_data = load_json("fatores_data")
frutos_data = load_json("frutos.json")
idade_data = load_json("idade_data") 

positivos = {}
negativos = {}

F = fatores_data.get("Fatores", {})
for cat_group, sign in [
    ("Sintomas", "positivo"),
    ("Fatores_Risco", "positivo"),
    ("Fatores_Protecao", "protecao")
]:
    group = F.get(cat_group, {})
    for subcat, items in group.items():
        for nome, info in items.items():
            entry = {
                "peso": info if isinstance(info, int) else info.get("peso", 1),
                "prob": info.get("prob", {}) if isinstance(info, dict) else {},
                "ausencia": info.get("ausencia", {}) if isinstance(info, dict) else {},
                "categoria": subcat,
                "raw_group": cat_group
            }
            if sign == "positivo":
                positivos.setdefault(subcat, {})[nome] = entry
            else:
                negativos.setdefault(subcat, {})[nome] = entry

hipoteses = list(raizes["Raizes"].keys())

def construir_priors(hipoteses_dict):
    n = len(hipoteses_dict)
    return {h: 1.0/n for h in hipoteses_dict}

priors = construir_priors(raizes["Raizes"])

def ajustar_prior_para_raiz_unica(raiz_escolhida, priors_in, prior_boost=0.99999):
    nova = {}
    n = len(priors_in)
    
    nova[raiz_escolhida] = prior_boost
    
    prior_restante = 1.0 - prior_boost
    
    if n > 1:
        peso_residual = prior_restante / (n - 1)
        for h in priors_in:
            if h != raiz_escolhida:
                nova[h] = peso_residual
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

    if not info_idade:
        return 1.0 

    inicio = info_idade["inicio_tipico"]
    janela = max(1, info_idade["janela"]) 

    if info_idade["janela"] == 0: 
        return 1.0 
    
    desvio = idade_atual - inicio
    
    argumento_exp = -0.5 * (desvio / janela)**2
    
    fia = math.exp(argumento_exp)
    
    return max(0.1, fia) 

def coletar_itens_raiz(raiz_info):
    itens = set()
    for v in raiz_info.get("tendencias", {}).values():
        if isinstance(v, list):
            itens.update(v)
    return itens

def amostrar_evidencias_focadas(raiz_foco, n_present, n_absent, foco_ratio=0.6):
    pool_total = []
    for cat, itens in positivos.items():
        for nome, info in itens.items():
            pool_total.append(("positivo", cat, nome, info))
    for cat, itens in negativos.items():
        for nome, info in itens.items():
            tipo = "protecao" if info.get("raw_group") == "Fatores_Protecao" else "negativo"
            pool_total.append((tipo, cat, nome, info))

    itens_foco = coletar_itens_raiz(raizes["Raizes"][raiz_foco])
    pool_foco = [item for item in pool_total if item[2] in itens_foco]
    pool_geral = pool_total

    n_foco = int(n_present * foco_ratio)
    n_aleatorio = n_present - n_foco
    
    n_foco = max(1, int(n_foco * random.uniform(0.8, 1.2)))
    n_aleatorio = max(0, int(n_aleatorio * random.uniform(0.8, 1.2)))
    n_present = n_foco + n_aleatorio
    
    present = []
    chosen = set()

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
        
    n_absent = max(1, int(n_absent * random.uniform(0.8, 1.2)))

    absent = []
    chosen_abs = set()

    for _ in range(n_absent):
        item = random.choice(pool_total)
        key = (item[1], item[2])
        if key in chosen_abs or key in chosen: continue
        chosen_abs.add(key)
        absent.append((False, item[0], item[1], item[2], item[3]))
        
    random.shuffle(present + absent)
    print(f"Amostragem: {len(present)} fatores PRESENTE (Foco: {n_foco}) | {len(absent)} fatores AUSENTE.")
    return present + absent

def likelihood_por_raiz(hipoteses, info, presença=True):
    if isinstance(info, int):
        peso = info
        peso_eff = abs(peso)
        return {r: peso_to_likelihood(peso_eff) if presença else 1 - peso_to_likelihood(peso_eff)
                for r in hipoteses}

    peso = info.get("peso", 1)
    prob_map = info.get("prob", {}) or {}
    ausencia_map = info.get("ausencia", {}) or {}

    lik = {}
    for r in hipoteses:
        if presença:
            if r in prob_map and isinstance(prob_map[r], (int, float)):
                lik[r] = max(min(prob_map[r], 0.99), 0.01)
            else:
                lik[r] = peso_to_likelihood(abs(peso))
        else:
            if r in ausencia_map and isinstance(ausencia_map[r], (int, float)):
                lik[r] = max(min(ausencia_map[r], 0.99), 0.01)
            else:
                p = prob_map.get(r, peso_to_likelihood(abs(peso)))
                lik[r] = max(min(1 - p, 0.99), 0.01)

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
        peso_modulado = max(0.1, abs(peso_raw) + ruido_exp) 
        
        for r in hipoteses:
            ajuste = 0
            if tipo == "protecao" and presenca: ajuste = -peso_modulado * posterior[r] 
            elif tipo != "protecao" and presenca: ajuste = peso_modulado * posterior[r]  
            elif tipo == "protecao" and not presenca: ajuste = peso_modulado * posterior[r]  
            else: ajuste = -peso_modulado * posterior[r] 

            risco_scores[r] += ajuste
    
    risco_scores = {r: max(0.0, score) for r, score in risco_scores.items()}

    return posterior, risco_scores

def calcular_probabilidade_frutos_alostatica(risco_scores_raizes, raizes_data, frutos_data, idade_sujeito, evidencias, nivel_vulnerabilidade):
    frutos = frutos_data.get("Frutos", {})
    probabilidades = {}
    
    evidencias_presentes = set()
    carga_alostatica_global = 0.0
    
    for (presenca, tipo, cat, nome, info) in evidencias:
        if presenca:
            evidencias_presentes.add(nome)
            peso = abs(info.get("peso", 1) if isinstance(info, dict) else info)
            if tipo != "protecao":
                carga_alostatica_global += peso
            else:
                carga_alostatica_global -= (peso * 0.5)
    
    carga_alostatica_global = max(0, carga_alostatica_global)

    mapa_raiz_para_fruto = {f_nome: {} for f_nome in frutos}
    for r_nome, r_info in raizes_data["Raizes"].items():
        r_itens = coletar_itens_raiz(r_info)
        for f_nome, f_info in frutos.items():
            f_gatilhos = set(f_info["gatilhos_comuns"])
            interseccao = len(r_itens.intersection(f_gatilhos))
            mapa_raiz_para_fruto[f_nome][r_nome] = interseccao

    for f_nome, f_info in frutos.items():
        sensibilidade = f_info["sensibilidade"]
        gatilhos = set(f_info["gatilhos_comuns"])
        
        carga_especifica_ponderada = 0.0
        gatilhos_ativos = 0
        
        for (presenca, tipo, cat, nome, info) in evidencias:
            if presenca and nome in gatilhos:
                 gatilhos_ativos += 1
                 peso_fator = abs(info.get("peso", 1) if isinstance(info, dict) else info)
                 carga_especifica_ponderada += peso_fator

        score_gatilhos = carga_especifica_ponderada * (1 + (nivel_vulnerabilidade * 0.2))
        
        influencia_raiz_total = 0.0
        max_conexao = 0
        if mapa_raiz_para_fruto[f_nome]:
             max_conexao = max(mapa_raiz_para_fruto[f_nome].values())
             
        if max_conexao > 0:
            for r_nome, r_score in risco_scores_raizes.items():
                conexao = mapa_raiz_para_fruto[f_nome].get(r_nome, 0)
                influencia_raiz_total += r_score * (conexao / max_conexao)
        
        prior = calcular_fator_idade(idade_sujeito, f_nome, tipo="Frutos")
        
        score_combinado = (score_gatilhos * 1.5) + (carga_alostatica_global * 0.1) + (influencia_raiz_total * 0.5)
        
        score_combinado *= (1 + (sensibilidade * 0.1))
        
        decay = 0.0
        if gatilhos_ativos == 0:
             decay = 4.0 
        
        threshold = 8.0 + decay 
        argumento_sigmoide = (score_combinado - threshold) / 3.0
        
        likelihood_alostatica = sigmoid(argumento_sigmoide)
        
        prob_final = (prior * 0.3) + (likelihood_alostatica * 0.7)
        
        probabilidades[f_nome] = min(max(prob_final, 0.01), 0.99)

    return normalizar_dict(probabilidades)

def simular_raiz_unica_avancado(n_present_base=15, n_absent_base=10):
    
    random.seed(os.urandom(16))
        
    NIVEL_VULNERABILIDADE = NIVEL_VULNERABILIDADE_FIXO 
    
    raizes_disponiveis = list(raizes["Raizes"].keys())
    probabilidades_selecao = calcular_probabilidades_selecao_raiz(raizes, NIVEL_VULNERABILIDADE)
    
    pesos_selecao = [probabilidades_selecao[r] for r in raizes_disponiveis]
    
    raiz_foco = random.choices(
        raizes_disponiveis, 
        weights=pesos_selecao, 
        k=1
    )[0]
    
    idade_sujeito = IDADE_SUJEITO_FIXA
    
    print("\n")
    print(f"SUJEITO: {idade_sujeito} ANOS")
    print("\n")
    
    print(f"PERSONALIDADE DO CASO: Nível de Vulnerabilidade {NIVEL_VULNERABILIDADE}")
    print("\n")
    
    print(f"RAIZ FOCO SORTEADA: {raiz_foco}")
    print("\n")

    priors_mod = dict(priors)
    print("Priors Modulados pela Idade (FIA)")
    for r in priors_mod:
        fia_r = calcular_fator_idade(idade_sujeito, r, tipo="Raizes")
        priors_mod[r] *= fia_r
        print(f" - {r}: FIA = {fia_r}") 
        
    priors_mod = normalizar_dict(priors_mod) 

    priors_cond = ajustar_prior_para_raiz_unica(
        raiz_foco,
        priors_mod 
    )

    evidencias = amostrar_evidencias_focadas(
        raiz_foco, 
        n_present=n_present_base, 
        n_absent=n_absent_base, 
        foco_ratio=0.6
    ) 

    print("Evidências Amostradas")
    for p, tipo, cat, nome, info in evidencias:
        status = "PRESENTE" if p else "AUSENTE"
        peso = info.get("peso", info) if isinstance(info, dict) else info
        print(f" - [{status}] [{tipo}] {nome} (peso clínico: {peso})")
    print("\n")

    posterior_final, risco_scores = calcular_risco_por_hipotese(
        hipoteses,
        evidencias,
        priors_cond
    )
    
    print(f"Score de Risco Final da Raiz {raiz_foco}: {risco_scores[raiz_foco]}")
    print("\n")

    probabilidade_frutos = calcular_probabilidade_frutos_alostatica(
        risco_scores, 
        raizes, 
        frutos_data, 
        idade_sujeito, 
        evidencias, 
        NIVEL_VULNERABILIDADE
    )
    
    maior_f = max(probabilidade_frutos, key=lambda k: probabilidade_frutos[k])

    print("Comorbidades finais prováveis (Funil de Carga Alostática Ponderada)")
    
    for f, p in sorted(probabilidade_frutos.items(), key=lambda x: -x[1]):
        desc = frutos_data["Frutos"][f]["descricao"]
        sens = frutos_data["Frutos"][f]["sensibilidade"]
        fia_f = calcular_fator_idade(idade_sujeito, f, tipo="Frutos")
        print(f" - {f} (Sens: {sens} | FIA: {fia_f:.2f}): {p:.4f}") 
        
    print(f"\nDistúrbio com Maior Probabilidade: {maior_f} ({probabilidade_frutos[maior_f]:.4f})\n")

    return {
        "raiz_escolhida": raiz_foco,
        "probabilidade_frutos": probabilidade_frutos,
        "maior_fruto": maior_f,
        "risco_scores": risco_scores, 
        "priors_mod": priors_mod,     
        "idade_sujeito": idade_sujeito,
        "nivel_vulnerabilidade": NIVEL_VULNERABILIDADE
    }

if __name__ == "__main__":
    
    print("INICIANDO SIMULAÇÃO AVANÇADA")
    
    resultado = simular_raiz_unica_avancado(
        n_present_base=15, 
        n_absent_base=10
    )

    dados_csv = []
    
    sujeito_node_name = "SUJEITO"
    dados_csv.append({
        "Nó_Principal": "RAIZ", 
        "Nome_Nó": sujeito_node_name,
        "Valor": 1.0,
        "Tipo": "Sujeito",
        "Prior_Mod_Idade": None,
        "Detalhes": f"Idade: {resultado['idade_sujeito']} | Vuln: {resultado['nivel_vulnerabilidade']}"
    })

    for raiz, score in resultado["risco_scores"].items():
        prior_mod = resultado["priors_mod"].get(raiz)
        
        dados_csv.append({
            "Nó_Principal": sujeito_node_name,
            "Nome_Nó": raiz,
            "Valor": score, 
            "Tipo": "Raiz",
            "Prior_Mod_Idade": prior_mod, 
            "Detalhes": "Score de Risco"
        })

    raiz_maior_score = resultado["raiz_escolhida"] 
    
    for fruto, prob in resultado["probabilidade_frutos"].items():
        
        dados_csv.append({
            "Nó_Principal": raiz_maior_score, 
            "Nome_Nó": fruto,
            "Valor": prob, 
            "Tipo": "Fruto",
            "Prior_Mod_Idade": None,
            "Detalhes": frutos_data["Frutos"][fruto]["descricao"]
        })
    
    dados_csv.append({
        "Nó_Principal": "CAMINHO_SELECIONADO",
        "Nome_Nó": resultado["raiz_escolhida"], 
        "Valor": None,
        "Tipo": "Metadado",
        "Prior_Mod_Idade": resultado["maior_fruto"],
        "Detalhes": "Raiz Foco | Maior Fruto"
    })
    
    csv_file = "arvore.csv"
    fieldnames = ["Nó_Principal", "Nome_Nó", "Valor", "Tipo", "Prior_Mod_Idade", "Detalhes"]
    
    try:
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            writer.writerows(dados_csv)
            
        print(f"\nResultado salvo em '{csv_file}'")
        
        print("\n")
        print("NORTE PARA EXIBIR O CAMINHO SELECIONADO")
        print("\n")
        
        print(f"A Raiz Foco sorteada foi: {resultado['raiz_escolhida']}")
        print(f"O Fruto de maior probabilidade foi: {resultado['maior_fruto']}")
        
        print("\nPara exibir este caminho na visualização (visualizar_arvore.py):")
        print("1. No código de visualização, leia a linha onde 'Nó_Principal' é 'CAMINHO_SELECIONADO'.")
        print("2. Nome_Nó = Raiz Foco. Prior_Mod_Idade = Maior Fruto.")
        print("3. Ao desenhar as arestas no NetworkX, destaque:")
        print(f"    Aresta: 'SUJEITO' -> '{resultado['raiz_escolhida']}'")
        print(f"    Aresta: '{resultado['raiz_escolhida']}' -> '{resultado['maior_fruto']}'")

        print("")
        
    except IOError:
        print(f"\nErro ao escrever no arquivo '{csv_file}'")