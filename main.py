from dados import carregar_dados
from funcoes import *

gastos = carregar_dados()

# PROGRAMA PRINCIPAL  
    
while True:
    print("\n1 - Adicionar gasto")
    print("2 - Ver gastos")
    print("3 - Ver total")
    print("4 - Total por categoria")
    print("5 - Maiores gastos")
    print("6 - Editar gasto")
    print("7 - Remover gasto")
    print("8 - Ranking de categorias")
    print("9- Gastos do mês atual")
    print("10 - Média por categoria")
    print("11 - Sair")
    print("12 - Ver gastos por mês")
    print("13 - Ver total por mês")
    print("14 - Ver gastos futuros")
    
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
        print("\nRanking de categorias:")
        
        ranking = ranking_categorias(gastos)
        
        if not ranking:
            print("Nenhum gasto cadastrado.")
        else: 
            for i, (cat,total) in enumerate(ranking, start=1):
                print(f"{i}º {cat} - R$ {total:.2f}")
    
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
        print("Saindo...")
        break

    elif opcao =="12":
        filtrar_por_mes(gastos)
        
    elif opcao =="13":
        totais = total_por_mes(gastos)
        
        print("\nTotais por mês:")
        for mes, total in sorted(totais.items()):
            print(f"{mes}: R$ {total:.2f}")
            
    elif opcao =="14":
        gastos_futuros(gastos)
            
    