# Riconoscimento gesti

La seguente applicazione riconosce il numero di dita presente nel video.

## utilizzo
python -d="1" -b="10, 10, 255, 255" 

dove: 
	d=numero dell'indice del device video
  	b=Regione di Interesse(Roi) ovvero la porzione del video in vui viene fatta l'analisi

## descrizione
detezione_movimento.py:
	. detezione del colore all'interno della roi
	. differenza assuluta tra pixel attuale e precedente, presi tramite il punto 1,  per vedere se ce movimento nella ROI
	. disegno dei contorni

detenzione_gesti.py:
	. creazione convex hull sui contorni trovati nel punto 3
	. Costruzione dell ROI circoloare conteggio dita
	. Conteggio delle dita
	. funzioni di disegno

il metodo di estrazione ed il conteggio della dita e stato preso da : 
https://gurus.pyimagesearch.com/wp-content/uploads/2016/02/malima_2006.pdf	
