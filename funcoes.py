from datetime import date
from dateutil.relativedelta import relativedelta
from dados import salvar_dados

def adicionar_gasto(gastos):
    nome = input("Nome do gasto: ")

    while True:
        try: 
            valor_total = float(input("Valor: ").replace(",","."))
            break
        except ValueError:
            print("Digite um número válido!")

    categoria = input("Categoria (comida, transporte, lazer...): ")
    
    parcelas_input = input("Parcelas (1 se não for parcelado): ")
    try:
        parcelas = int(parcelas_input)
        if parcelas <= 0:
            parcelas = 1
    except ValueError:
        parcelas = 1
    
    valor_parcela = valor_total / parcelas
    
    data= date.today().strftime("%Y-%m-%d")
    
    data_base = date.today()
    
    for i in range(parcelas):
        data_parcela = (data_base + relativedelta(months=i)).strftime("%Y-%m")
        
        gastos.append({
                "nome": f"{nome} ({i+1}/{parcelas})",
                "valor": valor_parcela,
                "categoria": categoria,
                "data": data_parcela
                })
    
    salvar_dados(gastos)
    print("Gasto adicionado!")
    
def listar_gastos(gastos):
    if not gastos:
        print("\nNenhum gasto cadastrado.")
        return
    
    print("\nSeus gastos: ")
    
    for i, g in enumerate(gastos):
        print(f"{i} - {g['nome']} - R$ {g['valor']:.2f} - {g['categoria']} - {g.get('data','sem data')}")
        
def remover_gasto(gastos):
    if not gastos:
        print("Nenhum gasto para remover.")
        return
    
    listar_gastos(gastos)
    
    try: 
        indice = int(input("Número: "))
        removido = gastos.pop(indice)
        
        print(f"Removido: {removido['nome']}")
        salvar_dados(gastos)
    
    except(ValueError, IndexError):
        print("Índice inválido")
        
def calcular_total(gastos):
    return sum(g["valor"] for g in gastos) 

def editar_gasto(gastos):
    if not gastos:
        print("Nenhum gasto para editar.")
        return
    
    listar_gastos(gastos)
    
    try:
        indice = int(input("Número: "))
        gasto = gastos[indice]
            
        novo_nome = input(f"Novo nome ({gasto['nome']}): ") or gasto["nome"]
        
        try:
            novo_valor_input = input(f"Novo valor ({gasto['valor']}): ")
            novo_valor = float(novo_valor_input) if novo_valor_input else gasto["valor"]
            
        except ValueError:
            novo_valor = gasto["valor"]
    
        nova_categoria = input(f"Nova categoria ({gasto['categoria']}): ") or gasto["categoria"]
        nova_data = input(f"Nova data({gasto['data']}): ") or gasto ["data"]
        gastos[indice] = {
            "nome" : novo_nome,
            "valor": novo_valor,
            "categoria": nova_categoria,
            "data":nova_data
        }        

        #salva
        salvar_dados(gastos)
        print("Gasto atualizado!")
    
    except Exception as e:
        print("Erro ao editar!", e)

def ranking_categorias(gastos):
    ranking = {}
    
    for g in gastos:
        cat = g["categoria"]
        ranking[cat] = ranking.get(cat, 0) + g["valor"]
        
    # ordenar do maior para o menor 
    ranking_ordenado = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    
    return ranking_ordenado

def gastos_do_mes_atual(gastos):
    mes_atual = date.today().strftime("%Y-%m")
    
    filtrados = [
        g for g in gastos
        if g.get("data", "").startswith(mes_atual)
    ]
    
    return filtrados

def media_por_categoria(gastos):
    dados = {}
    
    for g in gastos:
        cat = g["categoria"]
        
        if cat not in dados:
            dados[cat] = {
                "total": 0,
                "quantidade": 0
            }
        dados[cat]["total"] += g["valor"] 
        dados[cat]["quantidade"] += 1
    
    medias = {}
        
    for cat, info in dados.items():
        medias[cat] = info["total"] / info["quantidade"]
        
    return medias 

def total_por_categoria(gastos):
    totais = {}
    
    for g in gastos:
        cat = g["categoria"]
        totais[cat] = totais.get(cat,0) + g["valor"]
        
    return totais