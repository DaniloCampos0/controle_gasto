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
    print("4 - Sair")

    opcao = input("Escolha: ")

    if opcao =="1":
        nome = input("Nome do gasto: ")
        valor= float(input("Valor: "))
        gastos.append({"nome": nome, "valor":valor})
        with open("gastos.json", "w") as arquivo:
            json.dump(gastos, arquivo, indent=4)
        print("Gasto Adicionado!")

    elif opcao =="2":
        print ("\n Seus gastos: ")
        for g in gastos:
            print(f"{g['nome']} - R$ {g['valor']}")

    elif opcao =="3":
        total= sum(g["valor"] for g in gastos)
        print("total gasto:", total)

    elif opcao =="4":
        print("Saindo...")
        break

    else:
        print("Opção inválida.")