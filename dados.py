import json


def carregar_dados():
    try:
        with open("gastos.json", "r") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return[]

def exportar_csv(gastos):
    with open("gastos.csv", "w", encoding="utf-8") as arquivo:
        arquivo.write("nome;valor;categoria;data\n")
        
        for g in gastos:
            arquivo.write(f"{g['nome']};{g['valor']:.2f};{g['categoria']};{g.get('data', 'sem data')}\n")
            
def salvar_dados(gastos):
    with open("gastos.json", "w") as arquivo:
        json.dump(gastos, arquivo, indent=4)
        
    exportar_csv(gastos)