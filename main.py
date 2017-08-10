# Importando as bibliotecas random e math do python
from random import randint
import math

# Importando as bibliotecas numpy e matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Classe para modelar uma bactéria
class Bacteria:
    # Construtor da classe, onde a bactéria ocupa posições X e Y no espaço
    # e fazendo parte de um ambiente de procriação de bactérias
    def __init__(self, px, py, environment):
        self.px = px
        self.py = py
        self.environment = environment

    # Método para a bactéria gerar uma nova bactéria no mesmo ambiente
    #  que ela está
    def replicate(self):
        # Cria uma nova bactéria com posição aleatória próxima da bactéria pai
        self.environment.append(
            Bacteria(self.px + randint(-1, 1) * randint(30, 60),
                     self.py + randint(-1, 1) * randint(30, 60),
                     self.environment))


# end Bacteria Class

# Número inicial de bactérias
initial_number_bacteria = 3

# Taxa de crescimento de bactérias, podendo ser um número arbitrário
# no caso eu calculei esse número na mão a partir da solução analítica da EDO
#  para que se eu começasse com apenas 1 bactéria, em 10 segundos eu teria
# uma população de 1024 bactérias
rate_of_population_increase = 0.69314718056

# Tempo inicial
initial_time = 0

# Tempo final
final_time = 10

# Número de pontos em que o intervalo de tempo será dividido pra gerar um dt
slices_number = 1000

# Feito o cálculo do dt a partir do intervalo de tempo e do número de divisões
delta_time = (final_time - initial_time) / slices_number

# Gerando uma lista com todas as divisões de tempo, será usada na animação da
# matplotlib
delta_times = np.linspace(initial_time, final_time, slices_number)

# Gerando uma lista com todos os números inteiros presentes no intervalo de
# tempo, será usado no eixo X do gráfico do crescimento populacional
delta_times_floor = [math.floor(dt) for dt in delta_times]

# Variável pra armazenar a população atual de bactérias
population_count = initial_number_bacteria

# Tamanho do canvas que representa a cultura de bactérias
canvas_size = 1024, 768

# Criando a janela onde serã́o exibidas as animações do matplotlib
fig = plt.figure(figsize=(15, 5))

# Criando a primeira plotagem, que será utilizada pra representar a cultura
# de bactérias no matplotlib
ax_environment = fig.add_subplot(121)

# Dando um nome para a plotagem e tirando as escalas dos eixos X e Y que não
# serão utilizadas
ax_environment.set_xlabel('Cultura de bactérias')
ax_environment.set_xticklabels([])
ax_environment.set_yticklabels([])

# Criando listas onde serão armazenadas as posições X e Y de todas as bactérias,
# pra serem passadas para a plotagem
bacterias_px, bacterias_py = [], []

# Instanciando o objeto de linha no gráfico, será usado para desenhar as
# bactérias
bacteria_playground, = plt.plot([], [], 'go', animated=True)

# Instanciando um nova plotagem, que será utilizada como o gráfico de
# crescimento populacional das bactérias com o passar do tempo
ax_graphic = fig.add_subplot(122)

# Nomeando os eixos do gráfico de número de bactérias por tempo
ax_graphic.set_xlabel('Tempo')
ax_graphic.set_ylabel('Número de bactérias')

# Colocando as escalas dos eixos X e Y
ax_graphic.set_xticks([x for x in range(final_time)])
ax_graphic.set_yticks(
    [initial_number_bacteria * 2 ** x for x in range(final_time + 1)])

# Listas onde serão armazenadas as posições a serem plotadas no gráfico, tanto
# da solução analítica quanto da solução aproximada
graphic_px_approximation, graphic_py_approximation = [], []
graphic_px_real, graphic_py_real = [], []

# Instanciando os objetos de linha, o primeiro na cor padrão que é azul para os
# resultados da solução aproximada e o segundo na cor vermelha para os
# resultados da solução analítica
graphic_line_approximation, = plt.plot([], [], animated=True)
graphic_line_real, = plt.plot([], [], 'r', animated=True)

# Criando a lista que será utilizada como o ambiente de reprodução das bactérias
environment = []

# Populando o ambienta com o número inicial de bacterias, se for apenas uma
# ficará no meio do ambiente, se forem várias ficarão espalhadas
if initial_number_bacteria == 1:
    environment.append(Bacteria(canvas_size[0] / 2.0, canvas_size[1] / 2.0,
                                environment))
else:
    for _ in range(initial_number_bacteria):
        environment.append(
            Bacteria(randint(0, canvas_size[0]), randint(0, canvas_size[1]),
                     environment))


# Função modelando a evolução da cultura de bactérias
def environment_evolution():
    # Declarando as variáveis globais que estão sendo utilizadas
    global environment, bacterias_px, bacterias_py, population_count

    # Limpando as listas de posições das bactérias a serem plotadas
    bacterias_px, bacterias_py = [], []

    population_count += rate_of_population_increase * population_count \
                                                    * delta_time

    # O crescimento da população vai crescendo de maneira fracionárias de acordo
    # com as divisões no tempo, porém novas bactérias só podem ser criadas
    # quando o número da população for um novo número inteiro, tendo em vista
    # que a quantidade real de bactérias não pode ser um número fracionário
    while len(environment) < int(math.floor(population_count)):
        environment[randint(0, len(environment) - 1)].replicate()

    # Adicionando as posições das bactérias nas listas de posições a serem
    # plotadas na cultura de bactérias
    for bacteria in environment:
        bacterias_px.append(bacteria.px)
        bacterias_py.append(bacteria.py)


# Função de inicialização da animação da cultura de bactérias
def init_environment():
    # Definindo os limites do tamanho da animação
    ax_environment.set_xlim(0, canvas_size[0])
    ax_environment.set_ylim(0, canvas_size[1])

    # Adicionando as posições das bactérias iniciais nas listas de posições
    for bacteria in environment:
        bacterias_px.append(bacteria.px)
        bacterias_py.append(bacteria.py)

    # Plotando as bactérias iniciais na cultura
    bacteria_playground.set_data(bacterias_px, bacterias_py)

    # Retornando o objeto de linha, coisa do matplotlib
    return bacteria_playground,


# Função de callback que atualiza a cultura de bactérias com o passar do tempo
def update_environment(dt):
    # Chamando a função de evolução da cultura com o passar do tempo
    environment_evolution()

    # Plotando as bactérias na cultura
    bacteria_playground.set_data(bacterias_px, bacterias_py)

    # Retornando o objeto de linha, coisa do matplotlib
    return bacteria_playground,


# Função de inicialização da animação do gráfico de população de bactérias por
# tempo
def init_graphic():
    # Definindo os limites dos eixos X e Y do gráfico
    ax_graphic.set_xlim(0, final_time)
    ax_graphic.set_ylim(0, initial_number_bacteria * 2 ** final_time)

    # Plotando o número inicial de bactérias da linha de solução aproximada do
    # gráfico no tempo inicial
    graphic_px_approximation.append(0)
    graphic_py_approximation.append(initial_number_bacteria)
    graphic_line_approximation.set_data(graphic_px_approximation,
                                        graphic_py_approximation)

    # Plotando o número inicial de bactérias da linha de solução analítica do
    # gráfico no tempo inicial
    graphic_px_real.append(0)
    graphic_py_real.append(initial_number_bacteria)
    graphic_line_real.set_data(graphic_px_real,
                               graphic_py_real)

    # Retornando os objetos de linha, coisa do matplotlib
    return graphic_line_approximation, graphic_line_real


# Função para atualização da animação do gráfico de população de bactérias por
# tempo
def update_graphic(dt):
    # Resultado atual da solução aproximada
    current_approximation_result = len(environment)

    # Resultado atual da solução analítica
    current_real_result = initial_number_bacteria * math.e ** (
        rate_of_population_increase * dt)

    # Imprimindo o erro absoluto
    absolute_error = abs(current_real_result - current_approximation_result)
    print("Erro absoluto = %f" % absolute_error)

    # Imprimindo o erro relativo
    print("Erro relativo = %f\n" % (absolute_error / float(
        abs(current_approximation_result))))

    # Adicionando o dt atual na lista de pontos X da linha da solução aproximada
    graphic_px_approximation.append(dt)

    # Adicionando a quantidade atual de bactérias na lista de pontos Y da linha
    # da solução aproximada
    graphic_py_approximation.append(current_approximation_result)

    # Adicionando o dt atual na lista de pontos X da linha da solução analítica
    graphic_px_real.append(dt)

    # Adicionando a quantidade atual de bactérias na lista de pontos Y da linha
    # da solução analítica de acordo com a equação analítica obtida a partir da
    # EDO de crescimento populacional
    graphic_py_real.append(current_real_result)

    # Plotando os pontos no gráfico da linha de solução aproximada
    graphic_line_approximation.set_data(graphic_px_approximation,
                                        graphic_py_approximation)

    # Plotando os pontos no gráfico da linha de solução analítica
    graphic_line_real.set_data(graphic_px_real,
                               graphic_py_real)

    # Retornando os objetos de linha, coisa do matplotlib
    return graphic_line_approximation, graphic_line_real


# Criando a animação para a cultura de bactérias
environment_animation = animation.FuncAnimation(fig, update_environment,
                                                frames=delta_times,
                                                init_func=init_environment,
                                                blit=True,
                                                repeat=False)

# Criando a animação para o gráfico
graphic_animation = animation.FuncAnimation(fig, update_graphic,
                                            frames=delta_times,
                                            init_func=init_graphic,
                                            blit=True,
                                            repeat=False)

# Exibindo a janela da matplotlib
plt.show()
