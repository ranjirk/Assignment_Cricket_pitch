import cv2
import numpy as np


class detection:
	def __init__(self, frame):
		self.frame = frame
		self.frame_height, self.frame_width, _ = self.frame.shape
		self.frame_center = int(self.frame_width/2), int(self.frame_height/2)
		self.kernel = np.ones((5, 5), np.uint8)

	def center(self):
		self.ret = self.find_pitch()
		return self.ret

	def find_pitch(self):
		self.image = self.frame.copy()
		self.blur = cv2.GaussianBlur(self.image.copy(), (5,5), 0)
		self.back = self.color_enhancer(self.blur)
		self.gray = cv2.cvtColor(self.back, cv2.COLOR_BGR2GRAY)
		self.dilate = cv2.dilate(self.gray, self.kernel, iterations=1)
		self.edge  = cv2.Canny(self.dilate.copy(), 10, 100)
		(self.contours,_) = cv2.findContours(self.edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
		print("length of contour", len(self.contours))
		for self.contour in self.contours:
			(self.x, self.y, self.w, self.h) = cv2.boundingRect(self.contour)
			if self.bound_conditions([self.x, self.y, self.w, self.h]):
				print("			Found ", self.x, self.y, self.w, self.h, "     ", self.frame_center)
				cv2.rectangle(self.image, (self.x, self.y), (self.x+self.w,self.y+self.h), (0,255,0), 10)
		return self.image


	def color_enhancer(self, img):
		self.img = img
		self.hsv = cv2.cvtColor(self.blur, cv2.COLOR_BGR2HSV)
		self.green_mask = cv2.inRange(self.hsv, (26,10,30), (97,100,255))
		self.hsv[:,:,1] = self.green_mask
		self.green = cv2.cvtColor(self.hsv, cv2.COLOR_HSV2BGR)
		return self.green

	def bound_conditions(self, cor):
		self.x, self.y, self.w, self.h = cor
		self.box_in_centerW = True if ((self.x) < (self.frame_center[0]) < (self.x + self.w)) else False 
		self.box_in_centerH = True if ((self.y) < (self.frame_center[1]) < (self.y + self.h)) else False
		self.maxHeight 	= True if ( (self.h) < (self.frame_height-100) ) else False
		self.maxWidth 	= True if ( (self.w) < (self.frame_width - int(self.frame_width/10) ) ) else False
		self.minHeight	= True if (self.w>200) else False
		self.minWidth	= True if (self.h>400) else False
		return True if (self.box_in_centerW and self.box_in_centerH and\
						 self.minHeight and self.minWidth and self.maxWidth and self.maxHeight) else False



