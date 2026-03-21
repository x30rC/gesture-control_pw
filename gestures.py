#python 3-10-0.

import cv2 as cv
import mediapipe as mp
import time
import move_registration as mr
import powerpoint_logic as pow_log

video = cv.VideoCapture(0)

video.set(cv.CAP_PROP_FRAME_WIDTH,640)
video.set(cv.CAP_PROP_FRAME_HEIGHT,480)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

finger_point = [0 for i in range(21)]
finger = [0 for i in range(5)]

while True:
  good,image = video.read()
  hand_detected = False  

  camera_RGB = cv.cvtColor(image,cv.COLOR_RGB2BGR)
  results = hands.process(camera_RGB)
  print(results.multi_hand_landmarks)

  if results.multi_hand_landmarks: 
    for hand_lms in results.multi_hand_landmarks:
      hand_detected = True  # <--- рука обнаружена
      mp_drawing.draw_landmarks(image,hand_lms,mp_hands.HAND_CONNECTIONS)
      for id,point in enumerate(hand_lms.landmark):
        print(id,point)
        width,height,color = image.shape
        width,height = int(point.x * height), int(point.y * width)
        finger_point[id] = height
    good_distance = mr.distance_calc(finger_point[0],finger_point[5]) + mr.distance_calc(finger_point[0],finger_point[5])/2 
    if mr.distance_calc(finger_point[0],finger_point[8]) > good_distance:
      finger[1] = 1
    else:
      finger[1] = 0 

  if finger[1] and hand_detected:  
    for hand_lms in results.multi_hand_landmarks:
      for id,point in enumerate(hand_lms.landmark):
        width,height,color = image.shape
        width,height = int(point.x * height), int(point.y * width)
        if id == 8:
          cv.circle(image,(width,height),15,(234,178,34),cv.FILLED)
          cv.putText(image,'марк разогнул палец',(width,height-5),cv.FONT_HERSHEY_COMPLEX,1,(200,0,0),2)
          if(pow_log.check_powerpoint()):
            pow_log.next_slide()
  
  cv.imshow("main",image)

  key = cv.waitKey(30)
  if key == ord('q'):
    break
