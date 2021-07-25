import cv2
import imutils
import requests

from md_time import MD_time
from settings import Settings
from md_analysis import MD_analysis
from md_line import MD_line

class MotionDetection:
    """Overall class to manage progress"""
    def __init__(self):
        """Initialize the status"""
        self.settings = Settings()
        self.md_time = MD_time(self)
        self.md_analysis = MD_analysis(self)
        self.md_line = MD_line(self)


    def run(self):
        """Start the main progress"""
        while(1):
            if self.md_time.time_range():
                self.ret, self.images_list = self.md_analysis.motion_analysis()
                if self.ret == True:
                    self.md_line.send_line(self.images_list)
            else: self.md_time.sleep_time(1)
        
        

if __name__ == '__main__':
    md = MotionDetection()
    md.run()