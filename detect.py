import cv2
import imutils
import requests

from md_time import MD_time
from settings import Settings
from md_analysis import MD_analysis

class MotionDetection:
    """Overall class to manage progress"""
    def __init__(self):
        """Initialize the status"""
        self.settings = Settings()
        self.md_time = MD_time(self)
        self.md_analysis = MD_analysis(self)


    def run(self):
        """Start the main progress"""
        while(1):
            if self.md_time.time_range():
                self.images_list = self.md_analysis.motion_analysis()
                self.md_send(self.images_list)
        
        

if __name__ == '__main__':
    md = MotionDetection()
    md.run()