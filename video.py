import cv2, detect_pitch
from detect_pitch import detection

class video_Input:
	def __init__(self, input_video_name):
		self.input_video_name = input_video_name
		self.vid = cv2.VideoCapture(self.input_video_name)

	def read_video(self):
		count = 1
		while(True):
			self.ret, self.frame = self.vid.read()
			if self.ret:
				self.obj_2 = detection(self.frame)
				print("Frame : ", count)
				count += 1
				self.finframe = self.obj_2.center()
				cv2.imshow('frame', self.finframe)
				# cv2.imwrite(f"./frames_103/frame_{count}.jpg", self.finframe)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break
			else:
				cv2.destroyAllWindows()
				break
		self.vid.release()

obj_1 = video_Input("sample.mp4")
obj_1.read_video()
