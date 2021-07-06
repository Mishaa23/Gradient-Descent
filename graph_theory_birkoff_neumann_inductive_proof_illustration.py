# An illustration of the inductive part of the proof for the birkoff-von neumann theorem.
# This code demonstrate how a matrix M with all line sums equal can be decomposed into a sum of permutation matrices,
# by treating M as an adjacency matrix for a bipartite graph (with the rows and cols forming the bipartition). This graph 
# can then be found to have a perfect matching, which corresponds to a permutation matrix, which can in turn weighted and
# subtracted from M. This process can be continued until we have a full decomposition of M.

import math # Useful maths
import networkx as nx  # Graph/networks package

def pretty_print(S,row_length=120):
    ''' Displays a set of equally-sized matrices nicely.'''
    if S == [] or S[0] == []:
        return
    columns = row_length//(len(S[0][0])+2)
    rows = math.ceil(1.0*len(S)/columns)
    for row in range(rows):
        if row == rows-1:
            n_col = len(S) - columns*(rows-1)
        else:
            n_col = columns
        for i in range(len(S[0])):
            print('  '.join([''.join(str(s) for s in S[row*columns+column][i]) for column in range(n_col)]))
        print
    return

def make_bipartite_graph(M):
    '''Makes a bipartite graph G with parts A and B from matrix M with edges {i,j} when M_{ij} is nonzero.'''
    r = len(M)     # the number of rows    of M
    c = len(M[0])  # the number of columns of M
    G = nx.Graph()
    A = [i for i in range(r)] 
    B = [j for j in range(r,r+c)] 
    edges = [[i,j] for i in A for j in B if M[i][j-r] != 0]
    G.add_nodes_from(A+B)
    G.add_edges_from(edges)    
    return G

def bipartite_adjacency_matrix(G,r,c):
    '''Makes an rxc matrix M from bipartite graph G with part sizes r and c, 
       with entries M_{ij} equal to 1 when {i,j-r} is an edge of bipartite graph G, and 0 otherwise.'''
    M = [[0 for j in range(c)] for i in range(r)]
    for edge in G:
        M[edge[0]][edge[1]-r] = 1
    return M

def subtract(M, N):
    '''Subtracts the matrix N from the matrix M '''
    B = [[0,0,0,0],
      [0,0,0,0],
      [0,0,0,0],
      [0,0,0,0]]
    
    for i in range(len(M)):
        for j in range(len(M[0])):
            B[i][j] = M[i][j] - N[i][j]
    
    return B

def checkzero(M):
    '''Checks if M is the zero matrix '''
    B = [[0,0,0,0],
      [0,0,0,0],
      [0,0,0,0],
      [0,0,0,0]]
        
    k = 0
    for i in range(len(M)):
        for j in range(len(M[0])):
            if M[i][j] - B[i][j] != 0:
                k = k + 1
    
    if k > 0:
        return 1
    else:
        return 0
    
def nonnegative(M):
    '''Checks if M has negative entries '''
    k = 0
    for i in range(len(M)):
        for j in range(len(M[0])):
            if M[i][j] < 0:
                k = k + 1
    
    if k > 0:
        return 1
    else :
        return 0

    
H = [[1,3,1,0],
      [3,1,0,1],
      [0,1,1,3],
      [1,0,3,1]]

K = [[1,2,3,0],
      [0,3,2,1],
      [2,0,1,3],
      [3,1,0,2]]

L = [[4,0,1,0],
      [0,1,0,4],
      [1,0,4,0],
      [0,4,0,1]]

print('Here\'s a matrix M:\n')
M = H
n = len(M)
pretty_print([M])
print('\n')
print('We can rewrite this as:\n')
pretty_print([M])
print('=')


while checkzero(M) == 1:

    l = 0
    G = make_bipartite_graph(M)
    nx.draw(G)

    maxmatching = nx.maximal_matching(G)
    P = bipartite_adjacency_matrix(maxmatching,n,n)

    while nonnegative(subtract(M, P)) == 0:
        l = l + 1
        M = subtract(M, P)
        
    print('%s *' %l)
    pretty_print([P])
    
    if checkzero(M) == 1:   
        print('+')

    





