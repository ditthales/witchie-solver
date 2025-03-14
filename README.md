# Witchie Solver V2

Este é um solucionador para o jogo Witchie, capaz de encontrar o número mínimo de movimentos necessários para completar uma fase e fornecer o caminho para a solução.

## Sobre o Jogo

Witchie é um jogo de quebra-cabeça inspirado em Sokoban, mas com uma mecânica de movimento diferente. No Sokoban tradicional, o jogador se move uma casa por vez. No Witchie, o jogador continua andando em uma direção até colidir com algo (parede, caixa, etc.).

O jogo apresenta os seguintes elementos:

- ⬛️ - Parede (intransponível)
- 📦 - Caixa (pode ser empurrada)
- 🙋🏿 - Personagem (controlado pelo jogador)
- ⬜️ - Grama (espaço vazio onde o jogador pode andar)
- 🔯 - Spot (local onde as caixas devem ser colocadas)
- 🗄️ - Crate (outro tipo de objeto que pode ser empurrado)
- 🕳️ - Buraco (faz o jogador reiniciar o nível se cair nele)
- 🟫 - Vazio (espaço fora do mapa)

O objetivo do jogo é empurrar todas as caixas para os spots marcados no mapa, usando o menor número possível de movimentos.

## Mecânica de Movimento

A principal diferença desta versão do solucionador é a implementação correta da mecânica de movimento do jogo:

1. Quando o jogador se move em uma direção, ele continua andando até colidir com algo (parede, caixa, spot, crate).
2. Se o jogador colide com uma caixa e há espaço vazio ou um spot atrás dela, a caixa é empurrada.
3. Se o jogador colide com um crate e há espaço vazio atrás dele, o crate é empurrado.
4. Se o jogador encontra um buraco, o nível é reiniciado (no solucionador, consideramos isso como um movimento inválido).

Esta mecânica de movimento é implementada através da função `define_movement()` que utiliza recursão para simular o movimento contínuo do jogador até encontrar uma colisão.

## Algoritmos Implementados

O solucionador utiliza dois algoritmos de busca:

1. **A* (A-Star)**: Um algoritmo de busca informada que utiliza uma heurística para encontrar o caminho mais curto. É mais eficiente para níveis complexos.

2. **BFS (Breadth-First Search)**: Um algoritmo de busca em largura que explora todos os nós vizinhos antes de avançar para os próximos níveis. É mais simples e pode ser mais rápido para níveis pequenos.

## Componentes do Projeto

O projeto é composto por três arquivos principais:

1. **witchie_solver_v2.py**: Implementa os algoritmos de solução (A* e BFS) para encontrar o caminho mais curto, com a mecânica de movimento correta.

2. **witchie_solver_interface_v2.py**: Fornece uma interface de linha de comando para definir níveis e encontrar soluções.

3. **witchie_solver_visualizer_v2.py**: Permite visualizar a solução passo a passo, mostrando como o algoritmo resolve o nível.

## Como Usar

### Requisitos

- Python 3.6 ou superior

### Execução

#### Solucionador Básico

Execute o arquivo `witchie_solver_v2.py` para resolver o nível de exemplo:

```bash
python3 witchie_solver_v2.py
```

#### Interface Interativa

Execute o arquivo `witchie_solver_interface_v2.py` para uma interface interativa:

```bash
python3 witchie_solver_interface_v2.py
```

Siga as instruções na interface para:
- Carregar um nível predefinido (1-3)
- Definir um nível manualmente
- Escolher o algoritmo de solução (A* ou BFS)

#### Visualizador de Soluções

Execute o arquivo `witchie_solver_visualizer_v2.py` para visualizar a solução passo a passo:

```bash
python3 witchie_solver_visualizer_v2.py
```

O visualizador permite:
- Ver a solução passo a passo (modo manual)
- Reproduzir a solução automaticamente com um intervalo de tempo definido
- Observar como o algoritmo move o personagem e as caixas para resolver o nível

### Exemplo de Saída do Visualizador

```
=== Witchie Solver Visualizer V2 ===
Este programa visualiza a solução de um nível do jogo Witchie passo a passo.
Esta versão implementa corretamente a mecânica de movimento do jogo, onde o personagem anda até colidir com algo.

Opções:
1. Carregar nível predefinido
2. Sair

Escolha uma opção: 1
Digite o número do nível (1-3): 1

Mapa do nível:
⬛️ ⬛️ ⬛️ ⬛️ ⬛️ ⬛️ 🟫
⬛️ 🙋🏿 ⬛️ ⬜️ ⬜️ ⬛️ 🟫
⬛️ ⬜️ ⬛️ 📦 ⬜️ ⬛️ 🟫
⬛️ ⬜️ ⬛️ 🔯 ⬜️ ⬛️ 🟫
⬛️ 📦 ⬛️ ⬛️ ⬜️ ⬛️ 🟫
⬛️ ⬜️ ⬜️ ⬛️ ⬜️ ⬛️ ⬛️
⬛️ 🔯 ⬜️ ⬜️ 📦 🔯 ⬛️
⬛️ ⬛️ ⬛️ ⬛️ ⬛️ ⬛️ ⬛️

Escolha o algoritmo:
1. A* (mais eficiente para níveis complexos)
2. BFS (mais simples, pode ser mais rápido para níveis pequenos)

Escolha uma opção: 1

Resolvendo usando A*...
Solução encontrada em 0.05 segundos
Nós explorados: 42

Número mínimo de movimentos: 4

Opções de visualização:
1. Passo a passo (manual)
2. Automático

Escolha uma opção: 1

Solução com 4 movimentos:

Estado atual do nível:
⬛️ ⬛️ ⬛️ ⬛️ ⬛️ ⬛️ 🟫
⬛️ 🙋🏿 ⬛️ ⬜️ ⬜️ ⬛️ 🟫
⬛️ ⬜️ ⬛️ 📦 ⬜️ ⬛️ 🟫
⬛️ ⬜️ ⬛️ 🔯 ⬜️ ⬛️ 🟫
⬛️ 📦 ⬛️ ⬛️ ⬜️ ⬛️ 🟫
⬛️ ⬜️ ⬜️ ⬛️ ⬜️ ⬛️ ⬛️
⬛️ 🔯 ⬜️ ⬜️ 📦 🔯 ⬛️
⬛️ ⬛️ ⬛️ ⬛️ ⬛️ ⬛️ ⬛️

Passo 1/4: down

Estado atual do nível:
⬛️ ⬛️ ⬛️ ⬛️ ⬛️ ⬛️ 🟫
⬛️ ⬜️ ⬛️ ⬜️ ⬜️ ⬛️ 🟫
⬛️ ⬜️ ⬛️ 📦 ⬜️ ⬛️ 🟫
⬛️ 🙋🏿 ⬛️ 🔯 ⬜️ ⬛️ 🟫
⬛️ 📦 ⬛️ ⬛️ ⬜️ ⬛️ 🟫
⬛️ ⬜️ ⬜️ ⬛️ ⬜️ ⬛️ ⬛️
⬛️ 🔯 ⬜️ ⬜️ 📦 🔯 ⬛️
⬛️ ⬛️ ⬛️ ⬛️ ⬛️ ⬛️ ⬛️

Pressione Enter para o próximo passo...
```

## Definindo Níveis Manualmente

Ao escolher a opção de definir um nível manualmente, você precisará:

1. Informar o número de linhas e colunas do mapa
2. Digitar cada linha do mapa, usando os símbolos correspondentes separados por espaço

Exemplo:
```
Defina o nível do jogo:
Símbolos disponíveis:
⬛️ - Parede
📦 - Caixa
🙋🏿 - Personagem
⬜️ - Grama
🔯 - Spot
🗄️ - Crate
🕳️ - Buraco
🟫 - Vazio

Número de linhas: 3
Número de colunas: 3

Digite o mapa linha por linha, usando os símbolos acima separados por espaço:
Linha 1: ⬛️ ⬛️ ⬛️
Linha 2: ⬛️ 🙋🏿 ⬛️
Linha 3: ⬛️ 📦 🔯
```

## Diferenças em Relação à Versão 1

A principal diferença entre esta versão e a versão 1 do solucionador é a implementação correta da mecânica de movimento do jogo:

- **Versão 1**: O jogador se move uma casa por vez, como no Sokoban tradicional.
- **Versão 2**: O jogador continua andando em uma direção até colidir com algo, como no jogo Witchie original.

Isso resulta em um número significativamente menor de movimentos para completar um nível, pois cada movimento representa uma direção escolhida pelo jogador, não um passo individual.

## Limitações

- O solucionador tem um limite de tempo de 5 minutos para encontrar uma solução. Se não conseguir encontrar uma solução nesse tempo, ele informará que não foi possível resolver o nível.
- Níveis muito complexos podem exigir muita memória e tempo de processamento.
- A detecção de deadlocks (situações onde o nível se torna impossível de resolver) é básica e pode não identificar todos os casos.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias para o solucionador. 