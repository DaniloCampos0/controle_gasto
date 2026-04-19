import json

try:
    with open("gastos.json", "r") as arquivo:
        gastos = json.load(arquivo)

except: 
    
    gastos = []


while True:
    print("\n 1 - Adicionar gasto")
    print("2 - Ver gastos")
    print("3 - Ver total")
    print("4 - Total por categoria")
    print("5 - Maires gastos")
    print("6 - Sair")

    opcao = input("Escolha: ")

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
        for g in gastos:
            print(f"{g['nome']} - R$ {g['valor']} - {g['categoria']}")

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

    elif opcao =="6":
        print("Saindo...")
        break

    else:
        print("Opção inválida.")