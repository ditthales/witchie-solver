import heapq
import copy
from collections import deque
import time

class WitchieSolverV2:
    # Símbolos do jogo
    WALL = "⬛️"
    BOX = "📦"
    PERSON = "🙋🏿"
    GRASS = "⬜️"
    SPOT = "🔯"
    CRATE = "🗄️"
    HOLE = "🕳️"
    EMPTY = "🟫"

    def __init__(self, level_map, level_offset):
        """
        Inicializa o solucionador com o mapa do nível e o offset (largura) do nível.
        
        Args:
            level_map (list): Lista de strings representando o mapa do nível
            level_offset (int): Largura do nível (número de colunas)
        """
        self.level_map = level_map
        self.level_offset = level_offset
        self.spots_index = self.get_indexes_of(self.SPOT)
        self.start_position = self.get_indexes_of(self.PERSON)[0]
        
    def get_indexes_of(self, element):
        """
        Retorna os índices de um elemento específico no mapa.
        
        Args:
            element (str): O elemento a ser procurado
            
        Returns:
            list: Lista de índices onde o elemento foi encontrado
        """
        return [i for i, x in enumerate(self.level_map) if x == element]
    
    def is_level_completed(self, state):
        """
        Verifica se o nível está completo (todas as caixas estão nos spots).
        
        Args:
            state (list): Estado atual do mapa
            
        Returns:
            bool: True se o nível estiver completo, False caso contrário
        """
        return all(state[spot] == self.BOX for spot in self.spots_index)
    
    def define_movement(self, state, position, offset):
        """
        Implementa a lógica de movimento do jogo, onde o personagem anda até colidir com algo.
        
        Args:
            state (list): Estado atual do mapa
            position (int): Posição atual do jogador
            offset (int): Offset do movimento (depende da direção)
            
        Returns:
            tuple: (novo_estado, nova_posição)
        """
        new_state = state.copy()
        
        # Verifica se a nova posição está dentro dos limites do mapa
        if position + offset < 0 or position + offset >= len(state):
            return new_state, position
        
        # CASO 1: ENCONTROU UM BURACO
        if new_state[position + offset] == self.HOLE:
            # No jogo original, isso reinicia o nível
            # Aqui, vamos considerar como um movimento inválido
            return new_state, position
        
        # CASO 2: ANDANDO EM ESPAÇO LIVRE
        elif new_state[position + offset] == self.GRASS:
            # Troca a posição do jogador com o espaço vazio
            new_state[position] = self.GRASS
            new_state[position + offset] = self.PERSON
            new_position = position + offset
            
            # Verifica se o próximo espaço é uma colisão (parede, caixa, spot, crate)
            if (new_position + offset < 0 or new_position + offset >= len(new_state) or
                new_state[new_position + offset] == self.BOX or 
                new_state[new_position + offset] == self.WALL or 
                new_state[new_position + offset] == self.SPOT or 
                new_state[new_position + offset] == self.CRATE):
                # Colisão encontrada, para de andar
                return new_state, new_position
            else:
                # Continua andando recursivamente
                return self.define_movement(new_state, new_position, offset)
        
        # CASO 3: EMPURRANDO UM CRATE
        elif new_state[position + offset] == self.CRATE:
            # Verifica se o espaço após o crate é grama
            if (position + offset + offset >= 0 and position + offset + offset < len(new_state) and
                new_state[position + offset + offset] == self.GRASS):
                
                # Move o jogador e o crate
                new_state[position] = self.GRASS
                new_state[position + offset] = self.PERSON
                new_state[position + offset + offset] = self.CRATE
                
                return new_state, position + offset
        
        # CASO 4: EMPURRANDO UMA CAIXA
        elif new_state[position + offset] == self.BOX:
            # Verifica se a caixa não está em um spot
            if position + offset not in self.spots_index:
                # Verifica se o espaço após a caixa é grama ou spot
                if (position + offset + offset >= 0 and position + offset + offset < len(new_state) and
                    (new_state[position + offset + offset] == self.GRASS or 
                     new_state[position + offset + offset] == self.SPOT)):
                    
                    # Move o jogador e a caixa
                    new_state[position] = self.GRASS
                    new_state[position + offset] = self.PERSON
                    new_state[position + offset + offset] = self.BOX
                    
                    return new_state, position + offset
        
        # Se chegou aqui, o movimento é inválido
        return new_state, position
    
    def get_possible_moves(self, state, position):
        """
        Retorna todos os movimentos possíveis a partir de uma posição.
        
        Args:
            state (list): Estado atual do mapa
            position (int): Posição atual do jogador
            
        Returns:
            list: Lista de tuplas (nova_posição, novo_estado, direção)
        """
        moves = []
        directions = [
            (-self.level_offset, "up"),
            (self.level_offset, "down"),
            (-1, "left"),
            (1, "right")
        ]
        
        for offset, direction in directions:
            # Verifica se o movimento é válido (não sai do mapa)
            if (direction == "left" or direction == "right") and (position // self.level_offset != (position + offset) // self.level_offset):
                continue
            
            # Aplica o movimento usando a lógica do jogo
            new_state, new_position = self.define_movement(state, position, offset)
            
            # Se a posição mudou, o movimento é válido
            if new_position != position:
                moves.append((new_position, new_state, direction))
        
        return moves
    
    def get_heuristic(self, state, position):
        """
        Calcula uma heurística para o estado atual.
        A heurística é a soma das distâncias de Manhattan entre cada caixa e o spot mais próximo.
        
        Args:
            state (list): Estado atual do mapa
            position (int): Posição atual do jogador
            
        Returns:
            int: Valor da heurística
        """
        boxes = [i for i, x in enumerate(state) if x == self.BOX]
        spots = self.spots_index
        
        if len(boxes) != len(spots):
            return float('inf')
        
        # Calcula a distância de Manhattan entre cada caixa e o spot mais próximo
        total_distance = 0
        for box in boxes:
            box_row, box_col = box // self.level_offset, box % self.level_offset
            min_distance = float('inf')
            
            for spot in spots:
                # Se a caixa já está em um spot, a distância é 0
                if box == spot:
                    min_distance = 0
                    break
                    
                spot_row, spot_col = spot // self.level_offset, spot % self.level_offset
                distance = abs(box_row - spot_row) + abs(box_col - spot_col)
                min_distance = min(min_distance, distance)
            
            total_distance += min_distance
        
        # Adiciona a distância do jogador até a caixa mais próxima que não está em um spot
        player_row, player_col = position // self.level_offset, position % self.level_offset
        min_player_distance = float('inf')
        
        for box in boxes:
            if box not in spots:
                box_row, box_col = box // self.level_offset, box % self.level_offset
                distance = abs(player_row - box_row) + abs(player_col - box_col)
                min_player_distance = min(min_player_distance, distance)
        
        if min_player_distance != float('inf'):
            total_distance += min_player_distance
        
        return total_distance
    
    def is_deadlock(self, state):
        """
        Verifica se o estado atual é um deadlock (impossível de resolver).
        
        Args:
            state (list): Estado atual do mapa
            
        Returns:
            bool: True se for um deadlock, False caso contrário
        """
        # Implementação básica de detecção de deadlock
        # Verifica se alguma caixa está presa em um canto
        boxes = [i for i, x in enumerate(state) if x == self.BOX]
        
        for box in boxes:
            # Se a caixa já está em um spot, não é um deadlock
            if box in self.spots_index:
                continue
                
            row, col = box // self.level_offset, box % self.level_offset
            
            # Verifica se a caixa está em um canto
            up = (row - 1) * self.level_offset + col
            down = (row + 1) * self.level_offset + col
            left = row * self.level_offset + (col - 1)
            right = row * self.level_offset + (col + 1)
            
            # Verifica se a caixa está presa horizontalmente
            horizontal_blocked = False
            if col > 0 and col < self.level_offset - 1:
                if state[left] in [self.WALL, self.EMPTY] and state[right] in [self.WALL, self.EMPTY]:
                    horizontal_blocked = True
            
            # Verifica se a caixa está presa verticalmente
            vertical_blocked = False
            if row > 0 and row < len(state) // self.level_offset - 1:
                if state[up] in [self.WALL, self.EMPTY] and state[down] in [self.WALL, self.EMPTY]:
                    vertical_blocked = True
            
            # Se a caixa está presa tanto horizontalmente quanto verticalmente, é um deadlock
            if horizontal_blocked and vertical_blocked:
                return True
        
        return False
    
    def solve_a_star(self):
        """
        Resolve o nível usando o algoritmo A*.
        
        Returns:
            tuple: (número de movimentos, caminho)
        """
        start_time = time.time()
        
        # Estado inicial
        initial_state = self.level_map.copy()
        initial_position = self.start_position
        
        # Fila de prioridade para o A*
        open_set = []
        heapq.heappush(open_set, (0, 0, initial_position, initial_state, []))
        
        # Conjunto de estados visitados
        closed_set = set()
        
        # Contador de nós explorados
        nodes_explored = 0
        
        while open_set and time.time() - start_time < 300:  # Limite de 5 minutos
            # Obtém o estado com menor f(n) = g(n) + h(n)
            f, g, position, state, path = heapq.heappop(open_set)
            
            # Converte o estado para uma tupla para poder ser usado como chave no conjunto
            state_tuple = tuple(state)
            
            # Se o estado já foi visitado, pula
            if (position, state_tuple) in closed_set:
                continue
            
            # Adiciona o estado ao conjunto de visitados
            closed_set.add((position, state_tuple))
            
            # Incrementa o contador de nós explorados
            nodes_explored += 1
            
            # Se o nível está completo, retorna o caminho
            if self.is_level_completed(state):
                print(f"Solução encontrada em {time.time() - start_time:.2f} segundos")
                print(f"Nós explorados: {nodes_explored}")
                return len(path), path
            
            # Obtém os movimentos possíveis
            moves = self.get_possible_moves(state, position)
            
            for new_position, new_state, direction in moves:
                # Converte o novo estado para uma tupla
                new_state_tuple = tuple(new_state)
                
                # Se o novo estado já foi visitado, pula
                if (new_position, new_state_tuple) in closed_set:
                    continue
                
                # Verifica se o novo estado é um deadlock
                if self.is_deadlock(new_state):
                    continue
                
                # Calcula g(n) e h(n)
                new_g = g + 1
                new_h = self.get_heuristic(new_state, new_position)
                new_f = new_g + new_h
                
                # Adiciona o novo estado à fila de prioridade
                new_path = path + [direction]
                heapq.heappush(open_set, (new_f, new_g, new_position, new_state, new_path))
        
        print(f"Tempo limite excedido após {time.time() - start_time:.2f} segundos")
        print(f"Nós explorados: {nodes_explored}")
        return None, None
    
    def solve_bfs(self):
        """
        Resolve o nível usando o algoritmo BFS (Breadth-First Search).
        Útil para níveis menores onde o A* pode ser muito complexo.
        
        Returns:
            tuple: (número de movimentos, caminho)
        """
        start_time = time.time()
        
        # Estado inicial
        initial_state = self.level_map.copy()
        initial_position = self.start_position
        
        # Fila para o BFS
        queue = deque([(initial_position, initial_state, [])])
        
        # Conjunto de estados visitados
        visited = set()
        
        # Contador de nós explorados
        nodes_explored = 0
        
        while queue and time.time() - start_time < 300:  # Limite de 5 minutos
            position, state, path = queue.popleft()
            
            # Converte o estado para uma tupla para poder ser usado como chave no conjunto
            state_tuple = tuple(state)
            
            # Se o estado já foi visitado, pula
            if (position, state_tuple) in visited:
                continue
            
            # Adiciona o estado ao conjunto de visitados
            visited.add((position, state_tuple))
            
            # Incrementa o contador de nós explorados
            nodes_explored += 1
            
            # Se o nível está completo, retorna o caminho
            if self.is_level_completed(state):
                print(f"Solução encontrada em {time.time() - start_time:.2f} segundos")
                print(f"Nós explorados: {nodes_explored}")
                return len(path), path
            
            # Obtém os movimentos possíveis
            moves = self.get_possible_moves(state, position)
            
            for new_position, new_state, direction in moves:
                # Converte o novo estado para uma tupla
                new_state_tuple = tuple(new_state)
                
                # Se o novo estado já foi visitado, pula
                if (new_position, new_state_tuple) in visited:
                    continue
                
                # Verifica se o novo estado é um deadlock
                if self.is_deadlock(new_state):
                    continue
                
                # Adiciona o novo estado à fila
                new_path = path + [direction]
                queue.append((new_position, new_state, new_path))
        
        print(f"Tempo limite excedido após {time.time() - start_time:.2f} segundos")
        print(f"Nós explorados: {nodes_explored}")
        return None, None

# Exemplo de uso
if __name__ == "__main__":
    # Exemplo do nível 1 do jogo
    level_map = [
        "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "🟫",
        "⬛️", "🙋🏿", "⬛️", "⬜️", "⬜️", "⬛️", "🟫",
        "⬛️", "⬜️", "⬛️", "📦", "⬜️", "⬛️", "🟫",
        "⬛️", "⬜️", "⬛️", "🔯", "⬜️", "⬛️", "🟫",
        "⬛️", "📦", "⬛️", "⬛️", "⬜️", "⬛️", "🟫",
        "⬛️", "⬜️", "⬜️", "⬛️", "⬜️", "⬛️", "⬛️",
        "⬛️", "🔯", "⬜️", "⬜️", "📦", "🔯", "⬛️",
        "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️", "⬛️",
    ]
    level_offset = 7
    
    solver = WitchieSolverV2(level_map, level_offset)
    
    print("Resolvendo usando A*...")
    moves_count, path = solver.solve_a_star()
    
    if moves_count is not None:
        print(f"Número mínimo de movimentos: {moves_count}")
        print(f"Caminho: {path}")
    else:
        print("Não foi possível encontrar uma solução usando A*.")
        
        print("\nTentando com BFS...")
        moves_count, path = solver.solve_bfs()
        
        if moves_count is not None:
            print(f"Número mínimo de movimentos: {moves_count}")
            print(f"Caminho: {path}")
        else:
            print("Não foi possível encontrar uma solução usando BFS.") 