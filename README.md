This repository contains code and projects for a basilar air hockey bot.

# ITA
# Sistema di rilevamento del disco e previsione della traiettoria con rimbalzi per airhockey
# Rilevamento del colore tramite maschera in color code HSV implementato in OpenCV
# Raccolta di punti e calcolo della regressione lineare con l'aiuto di math

# Impostazioni per la cam PS4 Camera:
# 3448x808 fps=60 heighCut=800 widthCut=1328; 1748x408 fps=120 heightCut=400 widthCut=800 ; 898x200 fps=240 heightCut=N.a. widthCut=N.a.
# Driver e firmware: https://github.com/Hackinside/PS4-CAMERA-DRIVERS
# !!!! Ricordare di installare il firmware ogni volta che si riavvia il pc
# Imposta "cap" relativamente alle impostazioni del tuo sistema (normalmente 0 se è l'unica cam collegata, 1 se hai una webcam integrata)
# Esegui il file python, seleziona il colore minimo e il colore massimo tramite il color picker
# Controlla nella finestra 'result' se l'intervallo di colore è corretto (il disco dovrebbe apparire chiaramente in mezzo al nero)
# Spegni il programma premendo 'q' sulla tastiera e cattura l'ultimo frame con cv2.imwrite('nomeFile.jpg', frame)

#ENG
# Puck detection and trajectory prediction system with rebounds per airhockey
# Color detection via mask in HSV color code implemented in OpenCV
# Collection of points and calculations of the linear regression done with the help of math

# Settings for PS4 Camera:
# 3448x808 fps=60 heightCut=800 widthCut=1328; 1748x408 fps=120 heightCut=400 widthCut=800 ; 898x200 fps=240 heightCut=N.a. widthCut=N.a.
# Driver and firmware: https://github.com/Hackinside/PS4-CAMERA-DRIVERS
# !!!! Remember to install the firmware every time you restart your PC
# Set "cap" relative to your system settings (normally 0 if this is the only cam connected, 1 if you have a built-in webcam)
# Run the python file, select the minimum color and maximum color via the color picker 
# Check in the 'result' window if the color range is correct (the disk should appear clearly among the black)
# Close the program by pressing 'q' on the keyboard and capture the last frame with cv2.imwrite('filename.jpg', frame)
