import cv2 as cv

def do_drawer(image:cv,width:int,height:int) -> None:
	cv.circle(image,(width,height),15,(234,178,34),cv.FILLED)
	cv.putText(image,'палец разогнут',(width,height-5),cv.FONT_HERSHEY_COMPLEX,1,(200,0,0),2)