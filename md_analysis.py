import cv2
import imutils

class MD_analysis:
    """"A class using opencv for motion analysis"""

    def __init__(self, md):
        """Initialize opencv and rstp attributes"""
        self.settings = md.settings
        self.md_time = md.md_time
        self.rstp_url = 'rstp://{}:{}@{}:554/{}'.format(
                        self.settings.rstp.username,
                        self.settings.rstp.password,
                        self.settings.rstp.ipadress,
                        self.settings.rstp.stream
                        )

    def motion_analysis(self):
        """Using opencv for motion_analysis"""
        if self.md_time.time_range():
            self.cap = self._open_stream()
            if self.cap == False:
                return False
            
            self.last_img = self._read_stream(self.cap)
            while(1):
                self.img = self._read_stream(self.cap)

    def _open_stream(self):
        """Open the rstp stream"""
        self.failure_count_hour = 0
        while(self.failure_count_hour < 5):
            self.failure_count_minute = 0
            while(self.failure_count_minute < 5):
                cap = cv2.VideoCapture(self.rstp_url)
                if cap.isOpened() != True:
                    self.failure_count_minute += 1
                    self.md_time.sleep_time()
                    continue
                return cap
            self.failure_count_hour += 1
            self.md_time.sleep_time(60)
            
        return False

    def _read_stream(self, cap):
        """Read the stream and do some processes for the images"""
        while(1):
            self.ret, self.img = cap.read()
            if self.ret != True:
                continue

            self.clip_img = self.img[55:1080, 0:1920]
            self.half_img = cv2.resize(self.clip_img, None, 0.5, 0.5)
            self.gray_img = cv2.cvtColor(self.half_img, cv2.COLOR_RGB2GRAY)
            self.gb_img = cv2.GaussianBlur(self.gray_img, (21,21), 0)