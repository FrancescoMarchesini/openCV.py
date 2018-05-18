import cv2

#inizializzo il vettore di punti e una variabile booleana per
#verificare se i punti sono stati allocati
refPt = []
cropping = False

def click_and_crop(event, x, y, flags, param):
    #imposto refPt e cropping come variabile globale
    global refPt, cropping

    #se il bootone sinistro del mouse viene premuto
    #memorizzo le cordinate in refPt e combia lo stato di cropping
    #in True
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    #verifico se il left mouse button e' stato rilascito, salvo
    #il valore e metto cropping su False
    if event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping = False
        print("pt={}".format(refPt))

def get_point():
        return(refPt)

def get_state():
    return(cropping)
