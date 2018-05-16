import imutils
import numpy as np
import argparse
import cv2
import colorsys

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=False, help="path al video")
args = vars(ap.parse_args())

def nothing(x):
    pass

#finestra nella quale verranno agganciati gli slider
cv2.namedWindow("window_0")

#definisco i range del colore hsv che voglio modifcare
#manualemtne tramite gli slider
cv2.createTrackbar("low_H", "window_0", 0, 178, nothing)
cv2.createTrackbar("high_H", "window_0", 20, 178, nothing)
cv2.createTrackbar("low_S", "window_0", 10, 255, nothing)
cv2.createTrackbar("high_S", "window_0", 150, 255, nothing)
cv2.createTrackbar("low_V", "window_0", 60, 255, nothing)
cv2.createTrackbar("high_V", "window_0", 255, 255, nothing)


#acquisisco lo stream video
if not args.get("video", False):
    camera = cv2.VideoCapture(0)
else:
    camera = cv2.VideoCapture(args["video"])

camera.set(3, 1280)
camera.set(4, 720)

#main loop
while True:
    #grabb del video
    (grabbed, frame) = camera.read()
    
    #check sull'acquisizione video,  altrimenti esco
    if args.get("video") and not grabbed:
        break;

    #range per hue ovvero il colore
    low_h  = cv2.getTrackbarPos('low_H', 'window_0');
    high_h = cv2.getTrackbarPos('high_H', 'window_0');
    #range per la saturazione
    low_s = cv2.getTrackbarPos('low_S', 'window_0');
    high_s = cv2.getTrackbarPos('high_S', 'window_0');
    #range per il value ovvero luminosita
    low_v = cv2.getTrackbarPos('low_V', 'window_0');
    high_v = cv2.getTrackbarPos('high_V', 'window_0');

    #valori dinamici degli slider
    lower = np.array([low_h, low_s, low_v])
    upper = np.array([high_h, high_s, high_v])

    #creo il gradiente tra il valore di minimo e massimo per visualizzare un immagine del colore scelto
    s_gradient = np.ones((400, 1), dtype=np.uint8)*np.linspace(lower[1], upper[1], 400, dtype=np.uint8)
    v_gradient = np.rot90(np.ones((400, 1), dtype=np.uint8)*np.linspace(lower[1], upper[1], 400, dtype=np.uint8))
    h_array = np.arange(lower[0], upper[0]+1)
    
    #array per memorizzare l immagine creata
    rgb_color = np.ones((400, 400, 3), dtype=np.uint8)
    #genero l'immagine iterando nei valori
    for hue in h_array:
        h = hue*np.ones((400, 400), dtype=np.uint8)
        hsv_color = cv2.merge((h, s_gradient, v_gradient))
        rgb_color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2BGR)

    #resize del frame, e conversione di questo nel color model HSV
    #determino se l intensita dei pixel e nel range definito in lower e upper
    frame    = imutils.resize(frame, width=400)
    convert  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(convert, lower, upper)
    #cv2.imshow("convertHSV", convert)
    #cv2.imshow("mask", mask)
    
    #applico una serie di operazioni morfologiche, erosione e dilatazione
    #alla window_0mask utilizzando un kernel ellitiico
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)
    #cv2.imshow("filtri", mask)

    #applico un filtro di gauss per rimuove un po di noise
    #infine applico la mascherma sull immagine originale
    mask = cv2.GaussianBlur(mask, (3, 3), 0)
    overlap = cv2.bitwise_and(frame, frame, mask = mask)
    
    #faccio il resize delle immagine per poterle visualizzarla in modo
    #concatenato in un unica finestra
    frame = cv2.resize(frame, (300, 300))
    overlap = cv2.resize(overlap, (300, 300))
    rgb_color = cv2.resize(rgb_color, (300, 300))    
    #l immagine finale
    cv2.imshow("window_0", np.hstack([frame, overlap, rgb_color]))

    #funzione di uscita
    if cv2.waitKey(1) & 0xFF == ord("q"): 
        break

camera.release()
cv2.destroyAllWindows()

