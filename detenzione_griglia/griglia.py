import numpy as np
import argparse
import imutils
import cv2

#import la classe per la ROI da mouse
#from  click_and_crop import click_and_crop, get_state, get_point

#argomenti da riga di comando
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dev", required=True, help="indice del device video")
ap.add_argument("-v", "--video", required=False, help="se vuoi un vido metti il path")
args = vars(ap.parse_args())

#se non ce il video grabba la camera
if not args.get("video", False):
    camera = cv2.VideoCapture(int(args["dev"]))
    #altirmenti prendi il video
else:
    camera = cv2.VideoCapture(args["video"])

#dichiaro la variabile refPt per momeorizzare i punti della Roi, e la varibile cropping per fare il check sullo stato del mouse
refPt = []
cropping = False
def click_and_crop(event, x, y, flags, param):
    #setto come globali le variabili prima dichiarate
    global refPt, cropping

    #if il mouse_button_left e' stato cliccato salvo le cordinate e metto
    #lo stato di cropping a True
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    #se lo stato moue_button_left e' stato rilasciato memorizzo gli ultimi
    #due valori e metto lo stato di cropping su False
    if event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping = False

        cv2.rectangle(frame, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("frame", frame)

#funzione per parametrizzare in automatico il filtro di canny(edge detection)
def auto_canny(image, sigma=0.33):
    #computo l'intesita media dei pixel
    v = np.median(image)

    #setto in automatico i valori low e up del filtro
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(max(255, (1.0 + sigma) * v))

    #applico il filtro 
    edge = cv2.Canny(image, lower, upper)

    #ritorno l'immagine
    return edge

#dichiaro la windows sulla quale agira la call_back dei mouse event
cv2.namedWindow("frame")
#dichiaro la call_back definita nel file importato
cv2.setMouseCallback("frame", click_and_crop)

while True:
    #prendo il frame corrente
    (grabbed, frame) = camera.read()
    #se sto utilizzando il video faccio il check su EOS
    if args.get("video") and not grabbed:
            break
    
    #faccio una copia dei frame
    clone = frame.copy()
    
    if len(refPt) == 2:
        #genero la Roi in base all'input del mouse
        roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        #roi = clone[10:120, 20:120]
        #disegno la roi
        cv2.imshow("ROI", roi)

        #converto l'immagine in scala di grigi
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        #creo l'immagine binaria tramite il filtro di canny
        edges = auto_canny(gray)
        #convluzione con gaussina bluer
        edges = cv2.GaussianBlur(edges, (5, 5), 0)

        #mostro l'immagine dei contorni presi
        cv2.imshow("thres",  edges)

        #Hoghu line probabilistico. computazionalmente migliore
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100,minLineLength=20, maxLineGap=10)

        #faccio il check se sono presenti valori nella matrice 
        if lines is not None:
            for line in lines:
                (x1, y1, x2, y2) = line[0]
                #i valori della roi x e y
                a = refPt[0][1]
                c = refPt[0][0]
                #disegno le linee riportandole sul frame
                cv2.line(frame, (x1+a , y1+c), (x2+a , y2+c), (0, 255, 0), 2)

    #mostro  l immagine
    cv2.imshow("frame", frame)
    
    #i tasti premuti
    key = cv2.waitKey(1) & 0xFF
    
    # if the r fai il reset del cropping
    if key == ord("r"):
        frame = clone.copy()

    # if the q esci
    if key == ord("q"):
        break;

#pulisci tutto
camera.release()
cv2.destroyAllWindows()

