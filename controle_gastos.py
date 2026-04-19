import json
            
try:
    with open("gastos.json", "r") as arquivo:
        gastos = json.load(arquivo)

except FileNotFoundError: 
    gastos = []
    
# FUNÇÕES

def exportar_csv(gastos):
    with open("gastos.csv", "w", encoding="utf-8") as arquivo:
        arquivo.write("nome;valor;categoria\n")
        
        for g in gastos:
            arquivo.write(f"{g['nome']};{g['valor']:.2f};{g['categoria']}\n")
            
def salvar_dados(gastos):
    with open("gastos.json", "w") as arquivo:
        json.dump(gastos, arquivo, indent=4)
        
    exportar_csv(gastos)
    
def adicionar_gasto(gastos):
    nome = input("Nome do gasto: ")

    while True:
        try: 
            valor = float(input("Valor: ").replace(",","."))
            break
        except ValueError:
            print("Digite um número válido!")

    categoria = input("Categoria (comida, transporte, lazer...): ")

    gastos.append({
            "nome": nome, 
            "valor": valor,
            "categoria": categoria
            })
    
    salvar_dados(gastos)
    print("Gasto adicionado!")

def listar_gastos(gastos):
    if not gastos:
        print("\nNenhum gasto cadastrado.")
        return
    
    print("\nSeus gastos: ")
    
    for i, g in enumerate(gastos):
        print(f"{i} - {g['nome']} - R$ {g['valor']:.2f} - {g['categoria']}")

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

        gastos[indice] = {
            "nome" : novo_nome,
            "valor": novo_valor,
            "categoria": nova_categoria
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

    opcao = input("\nEscolha: ")

    if opcao =="1":
        adicionar_gasto(gastos)

    elif opcao =="2":
       listar_gastos(gastos)
       
    elif opcao =="3":
        print(f"Total gasto: R$, {calcular_total(gastos):.2f}")

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