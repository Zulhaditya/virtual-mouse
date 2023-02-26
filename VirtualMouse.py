import cv2
import numpy as np
import TrackingModule as tm
import time
import mouse
import pyautogui

######## VARIABEL #######
wCam, hCam = 640, 480
frameR = 100
smoothening = 4.5
pTime = 0
plocX,plocY  = 0,0
clocX,clockY = 0,0
click = 0
#########################

# test webcam
cap = cv2.VideoCapture(0)

# atur lebar dan panjang webcam display
cap.set(3,wCam)
cap.set(4,hCam)

detector = tm.deteksiTangan(maxHands=1)
wScr, hScr = pyautogui.size()
# print(wScr, hScr) -> 1280x720 

def waktu_eksekusi():
	et = time.time()
	elapsed_time = et - st
	print('Waktu eksekusi:', elapsed_time, 'detik')

while True:
		# waktu mulai
		st = time.time()
		# 1. Deteksi hand landmark
		success, img = cap.read()
		img = detector.trackingTangan(img)
		lmList, bbox = detector.trackingPosisi(img)
		
		# 2. Deteksi ujung jari telunjuk dan  jari tengah
		if len(lmList) != 0:
				# list koordinat jari telunjuk
				x1,y1 = lmList[8][1:]
				# list koordinat jari tengah
				x2,y2 = lmList[12][1:]

				# 3. Cek jika jari diatas/diangkat
				fingers = detector.jariAtas()
				cv2.rectangle(img,(frameR,frameR),(wCam-frameR, hCam-frameR),
														(255,0,255),2)

				# 4. Hanya jari telunjuk yang bisa menggerakkan cursor (moving mode)
				if fingers[0] == 0 and fingers[1] == 1:

						# 5. Konversi koordinat dari layar PC/laptop untuk mendapatkan posisi cursor
						x3 = np.interp(x1, (frameR, wCam-frameR), (0,wScr))
						y3 = np.interp(y1, (frameR, hCam-frameR), (0,hScr))

						# 6. Smoothen Values -> untuk memperhalus gerakan cursor mouse
						clocX = plocX + (x3-plocX) / smoothening
						clocY = plocY + (y3-plocY) / smoothening

						# 7. Menggerakkan mouse
						mouse.move(wScr - clocX, clocY)
						cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
						plocX,plocY = clocX,clocY
						waktu_eksekusi()

				# mode klik kiri
				if fingers[1] == 1 and fingers[2] == 1:
						length,img, lineInfo = detector.trackingJarak(8,12,img)
						if length < 40:
								cv2.circle(img,(lineInfo[4],lineInfo[5]),15,(0,255,0),cv2.FILLED)
								click += 1
								if click % 5 == 0:
										mouse.click()
										waktu_eksekusi()

				# mode klik kanan
				if fingers[4] == 1:
						click += 1
						if click % 5 == 0:
							# print(click)						
							mouse.right_click()
							waktu_eksekusi()
				
				# mode scroll
				if fingers[0] == 1 and fingers[1] == 1:
						length,img, lineInfo = detector.trackingJarak(4,8,img)
						if length > 120:
								mouse.wheel(0.3)
								waktu_eksekusi()
						else:
								mouse.wheel(-0.3)
								waktu_eksekusi()
				
				# jari tengah
				if fingers[2] == 1:
					waktu_eksekusi()
				
				# ibu jari
				if fingers[0] == 1:
					waktu_eksekusi()
				
		# 11. Frame Rate
		cTime = time.time()
		fps = 1/(cTime-pTime)
		pTime = cTime
		cv2.putText(img, 'FPS:', (20,50), cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),2)
		cv2.putText(img,str(int(fps)), (90,50),cv2.FONT_HERSHEY_PLAIN,2,
								(0,255,0),2)
		# 12. Display
		cv2.imshow("Virtual Mouse", img)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break