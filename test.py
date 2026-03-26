import sys
import os

# Добавляем папку libs в путь ДО импорта библиотек
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'libs'))

import cv2 as cv
import mediapipe as mp
import time
import powerpoint_logic as pow_log

video = cv.VideoCapture(0)
video.set(cv.CAP_PROP_FRAME_WIDTH, 640)
video.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

prev_x = None
prev_time = 0
last_swipe_time = 0

SWIPE_THRESHOLD = 80
TIME_THRESHOLD = 0.5
COOLDOWN = 1  # защита от повторов

while True:
	good,image  = video.read()
	if not good:
		break
	
	hand_detect = False	
	image_rgb = cv.cvtColor(image,cv.COLOR_BGR2RGB)
	results = hands.process(image_rgb)

	if(results.multi_hand_landmarks):
		for hand_lms in results.multi_hand_landmarks:
			hand_detected = True
			mp_drawing.draw_landmarks(image, hand_lms, mp_hands.HAND_CONNECTIONS)

			h, w, _ = image.shape
			for id, point in enumerate(hand_lms.landmark):
				cx, cy = int(point.x * w), int(point.y * h)
				if id == 8:
					cv.circle(image, (cx, cy), 10, (0, 255, 0), cv.FILLED)
					current_time = time.time()
					if prev_x is not None:
						dx = cx - prev_x
						dt = current_time - prev_time

						if dt < TIME_THRESHOLD:
							if dx > SWIPE_THRESHOLD:
								if current_time - last_swipe_time > COOLDOWN:
									cv.putText(image, 'SWIPE RIGHT', (50, 50),cv.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
									if pow_log.check_powerpoint():
										pow_log.next_slide()
										last_swipe_time = current_time
							#elif dx < -SWIPE_THRESHOLD:
								#if current_time - last_swipe_time > COOLDOWN:
									#cv.putText(image,'SWIPE LEFT',(50,50),cv.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
									#if pow_log.check_powerpoint():
										#import pyautogui as pyu
										#pyu.press('left')
										#last_swipe_time = current_time
					prev_x = cx
					prev_time = current_time
	cv.imshow("main",image)
	if cv.waitKey(1) & 0xFF == ord('q'):
		break

video.release()
cv.destroyAllWindows()