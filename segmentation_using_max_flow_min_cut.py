# An implementation of the Max-Flow-Min-Cut Theorem for the purpose of segmenting an image. The idea
# was obtained from Kleinberg and Tardos' book 'Algorithm Design'. A chosen greyscale image is converted
# into a matrix of pixels (representative of a grid of pixels), with each entry representing the integer
# value for the corresponding pixel. These values are then used to construct an appropriate flow network,
# within which a minimum cut corresponds to a foreground/background segmentation of the original image.


import numpy as np
import networkx as nx
import cv2
import matplotlib.pyplot as plt
from tensorflow.keras.applications.vgg16 import preprocess_input

'''a_i (foreground likelihood) = pixel value'''
'''b_i (background likelihood) = 255-pixel value'''
'''darker means more likely to be in foreground in this case (assumption)'''

def getimage (file):
    a = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    a = cv2.resize(a, (600, 400))
    a = preprocess_input(a)
    new = np.array(a)
    return new

def getnetwork (array):
    G = nx.DiGraph()
    r = len(array)
    c = len(array[0])
    '''source'''
    G.add_node('s')
    '''sink'''
    G.add_node('t')
    for i in range(r):
        for j in range(c):
            G.add_node((i,j))
            '''arcs involving source/sink'''
            G.add_edge('s', (i,j), capacity = array[i][j])
            G.add_edge((i,j), 't', capacity = 255-array[i][j])
    
    '''arcs representing penalties going across the grid'''
    for i in range (r):
        for j in range(c-1):
            G.add_edge((i,j), (i,j+1), capacity = abs(array[i][j] - array[i][j+1]))
            G.add_edge((i,j+1), (i,j), capacity = abs(array[i][j] - array[i][j+1]))

    '''arcs representing penalties down the grid'''
    for i in range (c):
        for j in range(r-1):
            G.add_edge((j,i), (j+1,i), capacity = abs(array[j][i] - array[j+1][i]))
            G.add_edge((j+1,i), (j,i), capacity = abs(array[j][i] - array[j+1][i]))
    return G

b = getimage('wunna.pbm')

r1 = len(b)
c1 = len(b[0])

G = getnetwork(b)

cut_value, partition = nx.minimum_cut(G, 's', 't')

background, foreground = partition

segmented_image = [[0 for j in range(c1)] for i in range(r1)]
for point in background:
    if point != 's':
        i = point[0]
        j = point[1]
        segmented_image[i][c1-1-j] = 255

plt.imshow(segmented_image)
plt.savefig("output")


