import numpy as np

#creo un immagine di grandezza 20x20 pixel
img = np.zeros((20, 20), dtype=np.int)

#disegno due righe nell'immagine appena creata
for i in range(0, 15):
    img[i+1][7] = 1
for i in range(11, 19):
    img[12][i] = 1

#creo la matrice nella quale verranno memorizzati i valori
M = np.zeros((28, 91), dtype=np.int)

#passo ogni pixel dell'immagine e se il pixel e' 1 incremento il rispettivo
#valore nella matrice M
for x in range(20):
    for y in range(20):
        if(img[x][y]==1):
            for roh in range(28):
                for theta in range(0, 91):
                    if roh == (y*np.cos(theta*np.pi/180) + x*np.sin(theta*np.pi/180)):
                        M[roh][theta] += 1

#disegno il risultato e la matrice
print(M[7][0])
print(M[12][90])
