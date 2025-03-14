import sys
from witchie_solver_v2 import WitchieSolverV2

def print_level(level_map, level_offset):
    """
    Imprime o mapa do nível de forma legível.
    
    Args:
        level_map (list): Lista de strings representando o mapa do nível
        level_offset (int): Largura do nível (número de colunas)
    """
    print("\nMapa do nível:")
    for i in range(0, len(level_map), level_offset):
        print(" ".join(level_map[i:i+level_offset]))
    print()

def print_solution(path):
    """
    Imprime a solução de forma legível.
    
    Args:
        path (list): Lista de direções para resolver o nível
    """
    if not path:
        print("Nenhuma solução encontrada.")
        return
    
    print("\nSolução:")
    for i, direction in enumerate(path):
        print(f"{i+1}. {direction}")
    print()

def define_level():
    """
    Permite ao usuário definir um nível manualmente.
    
    Returns:
        tuple: (level_map, level_offset)
    """
    print("Defina o nível do jogo:")
    print("Símbolos disponíveis:")
    print("⬛️ - Parede")
    print("📦 - Caixa")
    print("🙋🏿 - Personagem")
    print("⬜️ - Grama")
    print("🔯 - Spot")
    print("🗄️ - Crate")
    print("🕳️ - Buraco")
    print("🟫 - Vazio")
    
    try:
        rows = int(input("\nNúmero de linhas: "))
        cols = int(input("Número de colunas: "))
        
        level_map = []
        
        print("\nDigite o mapa linha por linha, usando os símbolos acima separados por espaço:")
        for i in range(rows):
            line = input(f"Linha {i+1}: ").split()
            if len(line) != cols:
                print(f"Erro: A linha deve ter {cols} elementos.")
                return define_level()
            level_map.extend(line)
        
        return level_map, cols
    except ValueError:
        print("Erro: Por favor, insira números válidos.")
        return define_level()

def load_predefined_level(level_number):
    """
    Carrega um nível predefinido.
    
    Args:
        level_number (int): Número do nível a ser carregado
        
    Returns:
        tuple: (level_map, level_offset)
    """
    if level_number == 1:
        # Nível 1 do jogo
        level_map = [
                    
                    # ⬛️ = wall, 📦 = box,  🙋🏿 = person,  ⬜️ = grass,   🔯 = plate.
                    
                    #nivel médio
                    "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️",
                    "⬛️", "⬜️", "⬜️", "🔯", "⬛️", "🔯", "⬜️", "⬛️",
                    "⬛️", "📦", "⬜️", "📦", "⬜️", "📦", "⬜️", "⬛️",
                    "⬛️", "🔯", "🙋🏿", "⬜️", "⬜️", "⬜️", "📦", "⬛️",
                    "⬛️", "⬛️", "⬛️", "⬜️", "⬛️", "⬜️", "🔯", "⬛️",
                    "⬛️", "⬜️", "⬜️", "⬜️", "⬜️", "⬜️", "⬛️", "⬛️",
                    "⬛️", "📦", "⬜️", "📦", "⬜️", "⬜️", "🔯", "⬛️",
                    "⬛️", "🔯", "⬛️", "⬛️", "📦", "📦", "🔯", "⬛️",
                    "⬛️", "⬛️", "⬛️", "⬛️", "🔯", "⬛️", "⬛️", "⬛️",
                    "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "🟫", "🟫"
                    
                ]
        level_offset = 8
    elif level_number == 2:
        # Nível 2 do jogo
        level_map = [
                    
                    
                    "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️",
                    "⬛️", "🔯", "⬜️", "⬜️", "⬜️", "⬜️", "⬜️", "🔯", "⬛️",
                    "⬛️", "⬜️", "⬜️", "⬜️", "⬜️", "⬜️", "⬜️", "⬜️", "⬛️",
                    "⬛️", "⬜️", "⬜️", "⬜️", "⬜️", "⬜️", "⬜️", "⬜️", "⬛️",
                    "⬛️", "⬜️", "⬜️", "⬜️", "📦", "⬜️", "⬜️", "⬜️", "⬛️",
                    "⬛️", "⬛️", "⬜️", "📦", "🙋🏿", "📦", "⬜️", "⬛️", "⬛️",
                    "⬛️", "⬜️", "⬜️", "⬜️", "⬛️", "⬜️", "⬜️", "⬜️", "⬛️",
                    "⬛️", "⬜️", "⬜️", "⬜️", "⬜️", "⬜️", "⬜️", "⬜️", "⬛️",
                    "⬛️", "⬜️", "⬜️", "⬜️", "⬜️", "⬜️", "⬜️", "⬜️", "⬛️",
                    "⬛️", "⬜️", "⬜️", "⬜️", "⬜️", "⬜️", "⬜️", "🔯", "⬛️",
                    "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️",
                    
                ]
        level_offset = 9
    elif level_number == 3:
        # Nível 3 do jogo
        level_map = [
            "🟫", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "🟫",
            "⬛️", "⬛️", "⬜️", "📦", "⬜️", "🔯", "⬛️", "⬛️",
            "⬛️", "⬜️", "⬜️", "⬛️", "⬛️", "⬛️", "🔯", "⬛️",
            "⬛️", "⬜️", "⬛️", "⬛️", "🟫", "⬛️", "⬜️", "⬛️",
            "⬛️", "⬜️", "⬛️", "🟫", "🟫", "⬛️", "⬜️", "⬛️",
            "⬛️", "⬜️", "⬛️", "⬛️", "⬛️", "⬛️", "⬜️", "⬛️",
            "⬛️", "⬜️", "⬜️", "⬜️", "📦", "⬜️", "⬜️", "⬛️",
            "⬛️", "🔯", "⬜️", "⬜️", "📦", "⬜️", "⬜️", "⬛️",
            "⬛️", "⬛️", "🔯", "⬜️", "📦", "🙋🏿", "⬜️", "⬛️",
            "🟫", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️"
        ]
        level_offset = 8
    else:
        print(f"Erro: Nível {level_number} não encontrado.")
        return None, None
    
    return level_map, level_offset

def main():
    print("=== Witchie Solver V2 ===")
    print("Este programa encontra o número mínimo de movimentos para completar um nível do jogo Witchie.")
    print("Esta versão implementa corretamente a mecânica de movimento do jogo, onde o personagem anda até colidir com algo.")
    
    while True:
        print("\nOpções:")
        print("1. Carregar nível predefinido")
        print("2. Definir nível manualmente")
        print("3. Sair")
        
        choice = input("\nEscolha uma opção: ")
        
        if choice == "1":
            level_number = int(input("Digite o número do nível (1-3): "))
            level_map, level_offset = load_predefined_level(level_number)
            if level_map is None:
                continue
        elif choice == "2":
            level_map, level_offset = define_level()
        elif choice == "3":
            print("Saindo...")
            sys.exit(0)
        else:
            print("Opção inválida. Tente novamente.")
            continue
        
        print_level(level_map, level_offset)
        
        solver = WitchieSolverV2(level_map, level_offset)
        
        print("Escolha o algoritmo:")
        print("1. A* (mais eficiente para níveis complexos)")
        print("2. BFS (mais simples, pode ser mais rápido para níveis pequenos)")
        
        algo_choice = input("\nEscolha uma opção: ")
        
        if algo_choice == "1":
            print("\nResolvendo usando A*...")
            moves_count, path = solver.solve_a_star()
        elif algo_choice == "2":
            print("\nResolvendo usando BFS...")
            moves_count, path = solver.solve_bfs()
        else:
            print("Opção inválida. Usando A* por padrão...")
            moves_count, path = solver.solve_a_star()
        
        if moves_count is not None:
            print(f"\nNúmero mínimo de movimentos: {moves_count}")
            print_solution(path)
        else:
            print("\nNão foi possível encontrar uma solução.")

if __name__ == "__main__":
    main() 