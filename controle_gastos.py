import json

from datetime import date
from dateutil.relativedelta import relativedelta
            
try:
    with open("gastos.json", "r") as arquivo:
        gastos = json.load(arquivo)

except FileNotFoundError: 
    gastos = []
    
# FUNÇÕES

def exportar_csv(gastos):
    with open("gastos.csv", "w", encoding="utf-8") as arquivo:
        arquivo.write("nome;valor;categoria;data\n")
        
        for g in gastos:
            arquivo.write(f"{g['nome']};{g['valor']:.2f};{g['categoria']};{g.get('data', 'sem data')}\n")
            
def salvar_dados(gastos):
    with open("gastos.json", "w") as arquivo:
        json.dump(gastos, arquivo, indent=4)
        
    exportar_csv(gastos)
    
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

def calcular_total(gastos):
    return sum(g["valor"] for g in gastos)  

def total_por_categoria(gastos):
    totais = {}
    
    for g in gastos:
        cat = g["categoria"]
        totais[cat] = totais.get(cat,0) + g["valor"]
        
    return totais

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

def ranking_categorias(gastos):
    ranking = {}
    
    for g in gastos:
        cat = g["categoria"]
        ranking[cat] = ranking.get(cat, 0) + g["valor"]
        
    # ordenar do maior para o menor 
    ranking_ordenado = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    
    return ranking_ordenado
           
# PROGRAMA PRINCIPAL  
    
while True:
    print("\n1 - Adicionar gasto")
    print("2 - Ver gastos")
    print("3 - Ver total")
    print("4 - Total por categoria")
    print("5 - Maiores gastos")
    print("6 - Editar gasto")
    print("7 - Remover gasto")
    print("8 - Sair")
    print("9- Gastos do mês atual")
    print("10 - Média por categoria")
    print("11 - Ranking de categorias")
    

    opcao = input("\nEscolha: ")

    if opcao =="1":
        adicionar_gasto(gastos)

    elif opcao =="2":
       listar_gastos(gastos)
       
    elif opcao =="3":
        print(f"Total gasto: R$ {calcular_total(gastos):.2f}")

    elif opcao =="4":
        totais = total_por_categoria(gastos)
        
        print("\nTotal por categoria:")
        for cat, total in totais.items():
            print(f"{cat}: R$ {total:.2f}")

    elif opcao =="5":
        print("\nMaiores gastos:")

        gastos_ordenados = sorted(gastos, key=lambda g: g["valor"], reverse=True)

        for g in gastos_ordenados[:5]:
            print(f"{g['nome']} - R$ {g['valor']:.2f} - {g['categoria']}")
          
    elif opcao =="6":
        editar_gasto(gastos)

    elif opcao =="7":
       remover_gasto(gastos)
        
    elif opcao =="8":
        print("Saindo...")
        break
    
    elif opcao =="9":
        print("\nGastos do mês atual:")
        
        gastos_mes = gastos_do_mes_atual(gastos)
        
        if not gastos_mes:
            print("Nenhum gasto neste mês.")
        else:
            for g in gastos_mes:
                print(f"{g['nome']} - R$ {g['valor']:.2f} - {g['categoria']} - {g['data']}")
                
    elif opcao =="10":
        medias = media_por_categoria(gastos)
        
        print("\nMédia por categoria:")
        
        for cat, media in medias.items():
            print(f"{cat}: R$ {media:.2f}")
            
    elif opcao =="11":
        print("\nRanking de categorias:")
        
        ranking = ranking_categorias(gastos)
        
        if not ranking:
            print("Nenhum gasto cadastrado.")
        else: 
            for i, (cat,total) in enumerate(ranking, start=1):
                print(f"{i}º {cat} - R$ {total:.2f}")