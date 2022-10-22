import cv2
import numpy as np
import TrackingModule as tm
import time
import autopy


######################
wCam, hCam = 640, 480
######################

# test webcam
cap = cv2.VideoCapture(0)

# atur lebar dan panjang webcam display
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
detector = tm.deteksiTangan(maxHands=1)

while True:
    # 1. Deteksi hand landmark
    success, img = cap.read()
    img = detector.trackingTangan(img)
    lmList, bbox = detector.trackingPosisi(img)
    
    # 2. Deteksi ujung jari telunjuk dan  jari tengah
    # 3. Cek jika jari diatas/diangkat
    # 4. Hanya jari tengah yang bisa menggerakkan cursor (moving mode)
    # 5. Konversi koordinat dari layar PC/laptop untuk mendapatkan posisi cursor
    # 6. Smoothen Values -> untuk memperhalus gerakan cursor mouse
    # 7. Menggerakkan mouse
    # 8. Jika jari telunjuk dan tengah diatas/diangkat masuk ke mode clicking (clicking mode)
    # 9. Hitung jarak antar jari
    # 10. Klik mouse jika jarak jari dekat

    # 11. Frame Rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)), (20,50),cv2.FONT_HERSHEY_PLAIN,3,
                (255,0,0),3)
    # 12. Display
    cv2.imshow("Virtual Mouse", img)
    cv2.waitKey(1)





