import time 
import pyautogui as pyu
import pygetwindow as gw

def check_powerpoint() -> bool:
	try:
		powerpoint_window = gw.getWindowsWithTitle('PowerPoint')
		slide_show_window = gw.getWindowsWithTitle('Слайд-шоу')
		presentation = gw.getWindowsWithTitle('Презентация')
		if len(powerpoint_window) or len(slide_show_window) or len(presentation):
			return True
		return False
	except:
		return False

def next_slide():
	time.sleep(3)
	pyu.press('right')
	print('slide switched!')