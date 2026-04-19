import json

def exportar_csv(gastos):
    with open("gastos.csv", "w", encoding="utf-8") as arquivo:
        arquivo.write("nome;valor;categoria\n")
        
        for g in gastos:
            arquivo.write(f"{g['nome']};{g['valor']};{g['categoria']}\n")
try:
    with open("gastos.json", "r") as arquivo:
        gastos = json.load(arquivo)

except: 
    
    gastos = []


while True:
    print("\n1 - Adicionar gasto")
    print("2 - Ver gastos")
    print("3 - Ver total")
    print("4 - Total por categoria")
    print("5 - Maires gastos")
    print("6 - Editar gasto")
    print("7 - Remover gasto")
    print("9 - Sair")

    opcao = input("\nEscolha: ")

    if opcao =="1":
        nome = input("Nome do gasto: ")

        while True:
            try: 
                valor = float(input("Valor: ").replace(",","."))
                break
            except:
                print("Digite um número válido!")

        categoria = input("Categoria (comida, transporte, lazer...): ")


        gastos.append({
            "nome": nome, 
            "valor": valor,
            "categoria": categoria
            })
        with open("gastos.json", "w") as arquivo:
            json.dump(gastos, arquivo, indent=4)
        print("Gasto Adicionado!")

    elif opcao =="2":
        print ("\n Seus gastos: ")
        for i, g in enumerate(gastos):
            print(f"{i} - {g['nome']} - R$ {g['valor']} - {g['categoria']}")

    elif opcao =="3":
        total= sum(g["valor"] for g in gastos)
        print("total gasto:", total)

    elif opcao =="4":
        totais = {}
        for g in gastos:
            cat = g["categoria"]
            valor = g["valor"]

            if cat in totais:
                totais[cat] += valor
            else:
                totais[cat] = valor

        print("\n Total por categoria:")
        for cat, total in totais.items():
            print(f"{cat}: R$ {total}")

    elif opcao =="5":
        print("\n Maiores gastos:")

        gastos_ordenados = sorted(gastos, key=lambda g: g["valor"], reverse=True)

        for g in gastos_ordenados[:5]:
            print(f"{g['nome']} - R$ {g['valor']} - {g['categoria']}")

    elif opcao =="9":
        print("Saindo...")
        break

    elif opcao =="7":
        print("\n Escolha o índice para remover:")
        
        for i, g in enumerate(gastos):
            print(f"{i} - {g['nome']} - R$ {g['valor']}")

        try: 
            indice = int(input("Número: "))
            removido = gastos.pop(indice)
            
            print(f"Removido: {removido['nome']}")
            
            #salva no JSON
            with open("gastos.json", "w") as arquivo:
                json.dump(gastos,arquivo, indent=4)
            
            #atualiza CSV
            exportar_csv(gastos)

        except (ValueError, IndexError): 
            print("Índice inválido!")
            
    elif opcao =="6":
        print("\nEscolha o índice para alterar:")
        
        for i, g in enumerate(gastos):
            print(f"{i} - {g['nome']} - R$ {g['valor']} - {g['categoria']}")
            
        try:
            indice = int(input("Número: "))
            gasto = gastos[indice]
                
            novo_nome = input(f"Novo nome ({gasto['nome']}): ") or gasto["nome"]
            
            try:
                novo_valor_input = input(f"Novo valor ({gasto['valor']}): ")
                novo_valor = float(novo_valor_input) if novo_valor_input else gasto["valor"]
                
            except:
                novo_valor = gasto["valor"]
        
            nova_categoria = input(f"Nova categoria ({gasto['categoria']}): ") or gasto["categoria"]

            gastos[indice] = {
                "nome" : novo_nome,
                "valor": novo_valor,
                "categoria": nova_categoria
            }        

            #salva
            with open("gastos.json", "w") as arquivo:
                json.dump(gastos, arquivo, indent=4)
                print("Gasto atualizado!")
                
            #atualiza CSV
            exportar_csv(gastos)
            
        except:
            print("Erro ao editar!")