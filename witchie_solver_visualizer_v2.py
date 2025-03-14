import time
import os
import platform
from witchie_solver_v2 import WitchieSolverV2

class WitchieSolverVisualizerV2:
    def __init__(self, level_map, level_offset, path=None):
        """
        Inicializa o visualizador com o mapa do nível, o offset e o caminho da solução.
        
        Args:
            level_map (list): Lista de strings representando o mapa do nível
            level_offset (int): Largura do nível (número de colunas)
            path (list): Lista de direções para resolver o nível
        """
        self.level_map = level_map.copy()
        self.level_offset = level_offset
        self.path = path
        self.solver = WitchieSolverV2(level_map, level_offset)
        self.player_position = self.solver.start_position
        
    def clear_screen(self):
        """
        Limpa a tela do terminal.
        """
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")
    
    def print_level(self, state):
        """
        Imprime o mapa do nível de forma legível.
        
        Args:
            state (list): Estado atual do mapa
        """
        print("\nEstado atual do nível:")
        for i in range(0, len(state), self.level_offset):
            print(" ".join(state[i:i+self.level_offset]))
        print()
    
    def visualize_solution(self, delay=0.5, auto_play=False):
        """
        Visualiza a solução passo a passo.
        
        Args:
            delay (float): Tempo de espera entre cada passo (em segundos)
            auto_play (bool): Se True, a solução é reproduzida automaticamente
        """
        if not self.path:
            print("Nenhuma solução para visualizar.")
            return
        
        state = self.level_map.copy()
        position = self.player_position
        
        self.clear_screen()
        print(f"Solução com {len(self.path)} movimentos:")
        self.print_level(state)
        
        for i, direction in enumerate(self.path):
            print(f"Passo {i+1}/{len(self.path)}: {direction}")
            
            # Determina o offset com base na direção
            if direction == "up":
                offset = -self.level_offset
            elif direction == "down":
                offset = self.level_offset
            elif direction == "left":
                offset = -1
            elif direction == "right":
                offset = 1
            
            # Aplica o movimento usando a lógica do jogo
            new_state, new_position = self.solver.define_movement(state, position, offset)
            state = new_state
            position = new_position
            
            self.print_level(state)
            
            if self.solver.is_level_completed(state):
                print("Nível completado!")
                break
            
            if auto_play:
                time.sleep(delay)
            else:
                input("Pressione Enter para o próximo passo...")
            
            self.clear_screen()
            print(f"Solução com {len(self.path)} movimentos:")
            
        print("Visualização concluída!")

def main():
    from witchie_solver_interface_v2 import load_predefined_level, print_level
    
    print("=== Witchie Solver Visualizer V2 ===")
    print("Este programa visualiza a solução de um nível do jogo Witchie passo a passo.")
    print("Esta versão implementa corretamente a mecânica de movimento do jogo, onde o personagem anda até colidir com algo.")
    
    while True:
        print("\nOpções:")
        print("1. Carregar nível predefinido")
        print("2. Sair")
        
        choice = input("\nEscolha uma opção: ")
        
        if choice == "1":
            level_number = int(input("Digite o número do nível (1-3): "))
            level_map, level_offset = load_predefined_level(level_number)
            if level_map is None:
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
                
                visualizer = WitchieSolverVisualizerV2(level_map, level_offset, path)
                
                print("\nOpções de visualização:")
                print("1. Passo a passo (manual)")
                print("2. Automático")
                
                vis_choice = input("\nEscolha uma opção: ")
                
                if vis_choice == "1":
                    visualizer.visualize_solution(auto_play=False)
                elif vis_choice == "2":
                    delay = float(input("Digite o tempo de espera entre os passos (em segundos): "))
                    visualizer.visualize_solution(delay=delay, auto_play=True)
                else:
                    print("Opção inválida. Usando visualização manual por padrão...")
                    visualizer.visualize_solution(auto_play=False)
            else:
                print("\nNão foi possível encontrar uma solução.")
        elif choice == "2":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main() 