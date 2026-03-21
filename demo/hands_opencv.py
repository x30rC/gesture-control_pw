import cv2 as cv
import mediapipe as mp

video = cv.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

while True:
	good,image = video.read()

	camera_RGB = cv.cvtColor(image,cv.COLOR_RGB2BGR)
	results = hands.process(camera_RGB)
	print(results.multi_hand_landmarks)

	if results.multi_hand_landmarks: 
		for hand_lms in results.multi_hand_landmarks:
			mp_drawing.draw_landmarks(image,hand_lms,mp_hands.HAND_CONNECTIONS)
			for id,point in enumerate(hand_lms.landmark):
				print(id,point)
				width,height,color = image.shape
				width,height = int(point.x * height), int(point.y * width)
				if id == 8:
					cv.circle(image,(width,height),15,(234,178,34),cv.FILLED)
					cv.putText(image,'указательный палец марка',(width,height-5),cv.FONT_HERSHEY_COMPLEX,1,(200,0,0),2)

	cv.imshow("main",image)

	key = cv.waitKey(30)
	if key == ord('q'):
		break