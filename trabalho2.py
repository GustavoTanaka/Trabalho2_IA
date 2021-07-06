import time
from random import randint
from sklearn.neighbors import kneighbors_graph
from scipy import sparse
from math import dist

# Will mexeu aqui
import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt

def undirect_graph(grafo):
    for i in range(len(grafo)-1):
        for j in range(i+1, len(grafo)):
            if grafo[i][j] or grafo[j][i] :
                grafo[j][i] = grafo[i][j] = 1
    return grafo

def get_next_in_row(matrix, row, flag):
    index_start = matrix.indptr[row]
    index_end = matrix.indptr[row+1]

    index = index_start + flag
    if index >= index_end: # não ha mais elementos na linha
        return -1
        
    return matrix.indices[index]

def __get_path(pai, final):
    caminho = [final]
    vertice = final
    while vertice in pai:
        caminho.insert(0, pai[vertice])
        vertice = pai[vertice]
    
    return caminho

# Funcao recursiva estoura pilha para nVertices muito grande
# def __depthSearch(grafo, atual, final, caminho):
#     if not caminho or atual not in caminho: # if vertice atual not in caminho salvo
#         caminho.append(atual)
#         if atual == final: 
#             return caminho
        
#         i = 0
#         proxVertice = get_next_in_row(grafo, atual, i)
#         i += 1
#         # itera sobre todos os elementos da linha
#         while proxVertice >= 0:
#             result = __depthSearch(grafo, proxVertice, final, caminho) # chama funcao recursiva
#             if result:
#                 return result
#             proxVertice = get_next_in_row(grafo, atual, i)
#             i += 1

def depthSearch(grafo, inicial, final):
    # return __depthSearch(grafo, inicial, final, [])

    pilha = [inicial]
    visitados = [inicial]
    pai = {}

    while pilha:
        vertice = pilha.pop()
        if vertice == final:
            return __get_path(pai, final)
        
        i = 0
        proxVertice = get_next_in_row(grafo, vertice, i)
        i += 1
        # itera sobre todos os elementos da linha
        while proxVertice >= 0:
            if proxVertice not in visitados:
                pilha.append(proxVertice)
                visitados.append(proxVertice)
                pai[proxVertice] = vertice # salva o no pai pelo qual foi acessado
            proxVertice = get_next_in_row(grafo, vertice, i)
            i += 1

def breadthSearch(grafo, inicial, final):
    visitados = [inicial]
    fila = [inicial]
    pai = {}

    while fila:
        vertice = fila.pop(0)
        if vertice == final:
            return __get_path(pai, final)
        
        i = 0
        proxVertice = get_next_in_row(grafo, vertice, i)
        i += 1
        # itera sobre todos os elementos da linha
        while proxVertice >= 0:
            if proxVertice not in visitados:
                fila.append(proxVertice)
                visitados.append(proxVertice)
                pai[proxVertice] = vertice # salva o no pai pelo qual foi acessado
            proxVertice = get_next_in_row(grafo, vertice, i)
            i += 1
        
def __distance_to_final(vertices, final):
    distancia = []
    for x,y in vertices:
        distancia.append(dist((x,y), vertices[final]))

    return distancia

def bestFirst(vertices, grafo, inicial, final):
    h = __distance_to_final(vertices, final) # calcula a distancia euclidiana dos pontos ate o final
    visitados = [inicial]
    fila = [inicial]
    pai = {}

    while fila:
        vertice = fila.pop(0)
        if vertice == final:
            return __get_path(pai, final)
        
        i = 0
        proxVertice = get_next_in_row(grafo, vertice, i)
        i += 1
        # itera sobre todos os elementos da linha
        while proxVertice >= 0:
            if proxVertice not in visitados:
                pos = 0
                # insere o elemento ordenado a partif do f = h
                while pos < len(fila) and h[proxVertice] > h[fila[pos]]:
                    pos += 1
                fila.insert(pos, proxVertice)
                visitados.append(proxVertice)
                pai[proxVertice] = vertice # salva o no pai pelo qual foi acessado
            proxVertice = get_next_in_row(grafo, vertice, i)
            i += 1

def __get_pos_to_insert(fila, elem):
    start = 0
    end = len(fila) - 1
    pivot = (int) ((start + end) / 2)
    elemF = elem['g'] + elem['h']

    while start <= end:
        pivotF = fila[pivot]['g'] + fila[pivot]['h']
        if elemF < pivotF:
            end = pivot - 1
        elif elemF > pivotF:
            start = pivot + 1
        else:
            return pivot
        pivot = (int) ((start + end) / 2)

    return start

def aStar(vertices, grafo, inicial, final):
    h = __distance_to_final(vertices, final) # calcula a distancia euclidiana dos pontos ate o final
    fila = [{
        'vertice': inicial,
        'g': 0,
        'h': h[inicial],
        'caminho': [inicial]
    }]
    visitados = []

    while fila:
        atual = fila.pop(0)
        visitados.append(atual['vertice'])
        if atual['vertice'] == final:
            return atual['caminho']
        
        i = 0
        proxVertice = get_next_in_row(grafo, atual['vertice'], i)
        i += 1
        # itera sobre todos os elementos da linha
        while proxVertice >= 0:
            if proxVertice not in visitados:
                vDict = {
                    'vertice': proxVertice,
                    'g': atual['g'] + dist(vertices[ atual['vertice'] ], vertices[proxVertice]),
                    'h': h[proxVertice],
                    'caminho': atual['caminho'] + [proxVertice]
                }
                # insere o elemento ordenado a partif do f = g + h
                pos = __get_pos_to_insert(fila, vDict)
                fila.insert(pos, vDict)
            proxVertice = get_next_in_row(grafo, atual['vertice'], i)
            i += 1


def main():
    nVertices = int(input('Numero de vertices: '))
    K = int(input('Valor do K: '))

    vertices = []
    for i in range(nVertices):
        vertices.append((randint(1, nVertices), randint(1, nVertices)))
    # remove vertices duplicados
    while True:
        vertices = list(dict.fromkeys(vertices))
        if len(vertices) == nVertices:
            break
        while len(vertices) < nVertices:
            vertices.append((randint(1,nVertices), randint(1,nVertices)))
    
    # Impressao do grafo
    G = nx.Graph()
    G.add_edges_from(vertices)
    net = Network(notebook=True)
    net.from_nx(G)
    net.show("grafo.html")

    grafo_knn = kneighbors_graph(vertices, K).toarray() # forma o grafo direcionado a partir do algoritmo KNN
    grafo_knn = undirect_graph(grafo_knn) # transforma em um grafo nao direcionado
    grafo_knn = sparse.csr_matrix(grafo_knn) # salva o grafo como matriz esparsa

    # seleciona vertices iniciais 
    vInicial = randint(0, nVertices-1)
    vFinal = randint(0, nVertices-1)
    while vInicial == vFinal:
        vFinal = randint(0, nVertices-1)

    print('Vertice Inicial: ', vertices[vInicial])
    print('Vertice Final: ', vertices[vFinal])

    # Busca em Profundidade
    tInicio = time.time()
    result = depthSearch(grafo_knn, vInicial, vFinal)
    tFim = time.time()
    if result is not None:
        print('\nBusca em Profundidade:')
        print('Caminho:')
        for i in result:
            print('\t', vertices[i])
        print('Tempo: ', tFim - tInicio)
    else: # encerra o programa caso nao haja solucao
        print('Não há solução para a situação proposta')
        return

    # Busca em Largura
    print('\nBusca em Largura:')
    tInicio = time.time()
    result = breadthSearch(grafo_knn, vInicial, vFinal)
    tFim = time.time()
    print('Caminho:')
    for i in result:
        print('\t', vertices[i])
    print('Tempo: ', tFim - tInicio)

    # Greedy Best-First
    print('\nBest-First:')
    tInicio = time.time()
    result = bestFirst(vertices, grafo_knn, vInicial, vFinal)
    tFim = time.time()
    print('Caminho:')
    for i in result:
        print('\t', vertices[i])
    print('Tempo: ', tFim - tInicio)

    # A-Estrela (A*)
    print('\nA-Estrela:')
    tInicio = time.time()
    result = aStar(vertices, grafo_knn, vInicial, vFinal)
    tFim = time.time()
    print('Caminho:')
    for i in result:
        print('\t', vertices[i])
    print('Tempo: ', tFim - tInicio)

if __name__ == '__main__':
    main()

# TO DO
    # VISUALIZAR OS CAMINHOS OBTIDOS
    # ATUALIZAR README COM AS LIBS QUE PRECISAM SER INSTALADAS
