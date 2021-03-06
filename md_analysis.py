import cv2
import imutils

class MD_analysis:
    """"A class using opencv for motion analysis"""

    def __init__(self, md):
        """Initialize opencv and rtsp attributes"""
        self.settings = md.settings
        self.md_time = md.md_time
        self.rtsp_url = "rtsp://{}:{}@{}:554/{}".format(
                        self.settings.rtsp['username'],
                        self.settings.rtsp['password'],
                        self.settings.rtsp['ipadress'],
                        self.settings.rtsp['stream']
                        )
        self.images_list = []

    def motion_analysis(self):
        """Using opencv for motion_analysis"""
        self._reset_att()
        self.ret, self.cap = self._open_stream()
        if self.ret == False:
            return (False, self.images_list)
        
        self.last_gb_img = self._read_stream()
        self.dt_intervel_start = self.md_time.get_time()
        while(1):
            if self.md_time.time_range() == False:
                self.cap.release()
                return (False, self.images_list)
            self.gb_img = self._read_stream()
            self.dt_intervel_end = self.md_time.get_time()
            #if the time between dt_interval_start and dt_interval_end longer than time_intervel, it process images, or just read images and ingore the images.
            if(self.dt_intervel_start + self.md_time.time_intervel <= self.dt_intervel_end): 
                self.dt_intervel_start = self.dt_intervel_end
                self.ret, self.dt, self.ret_img = self._process_dif()
                if self.ret == True:
                    self.dif_cnt += 1
                    self.last_dt = self.dt
                    self._save_img()
                
                if self.dif_cnt > 0:
                    #if time out the time_limit and number of picture is bigger than minimal limit, return the function with the path of saved pcitures.
                    if self.dt >= self.last_dt + self.md_time.time_limit:
                        if self.dif_cnt < self.settings.picture_num['min']:
                            self._reset_att
                            self.cap.release()
                            return (False, self.images_list)
                        else: break

                    #if picture's number over the maximal limit, return the function with the path of saved pcitures.
                    if self.dif_cnt >= self.settings.picture_num['max']:
                        break 

                self.last_gb_img = self.gb_img
        self.cap.release()
        return (True, self.images_list)

    def _reset_att(self):
        """Reset the attributes"""
        self.dif_cnt = 0
        self.images_list.clear()

    def _open_stream(self):
        """Open the rstp stream"""
        self.failure_count_hour = 0
        #if open failed, retry after one minute for five times and continue five hours. you can change the attributes as you like.
        while(self.failure_count_hour < 5):
            self.failure_count_minute = 0
            while(self.failure_count_minute < 5):
                cap = cv2.VideoCapture(self.rtsp_url)
                if cap.isOpened() != True:
                    self.failure_count_minute += 1
                    self.md_time.sleep_time()
                    continue
                return (True, cap)
            self.failure_count_hour += 1
            self.md_time.sleep_time(60)
            
        return (False, cap)

    def _read_stream(self):
        """Read the stream and do some processes for the images"""
        while(1):
            self.ret, self.img = self.cap.read()
            if self.ret != True:
                continue

            self.clip_img = self.img[55:1080, 0:1920] #since my ip camera embedded time on the upper images, i need to cut it out.
            self.half_img = cv2.resize(self.clip_img, dsize=None, fx=0.5, fy=0.5) #change the images' size to reduce the load of your cpu.
            self.gray_img = cv2.cvtColor(self.half_img, cv2.COLOR_RGB2GRAY) #change the images to white-blank images.
            self.gb_img = cv2.GaussianBlur(self.gray_img, (21,21), 0) #blurring images to reduce noisy.
            break

        return self.gb_img

    def _process_dif(self):
        """Process the diffrence of tow images"""
        self.dif = cv2.absdiff(self.last_gb_img, self.gb_img) #get the difference of two images.
        self.thresh = cv2.threshold(self.dif, 25, 225, 
                      cv2.THRESH_BINARY)[1] #threshold images and just get the thresholded images.
        self.thresh = cv2.dilate(self.thresh, None, iterations=2) #make the differece wider.
        self.cnts = cv2.findContours(self.thresh.copy(), 
                    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #retrieves only the extreme outer contours by using two point(to get a straight line)
        self.cnts = imutils.grab_contours(self.cnts) #remove the small dot and retrive the largest contours.

        self.min_x, self.min_y, self.max_x, self.max_y = 4000, 2000, 0, 0
        self.valid_cnt = 0

        for self.c in self.cnts:
            (self.x, self.y, self.w, self.h) = cv2.boundingRect(self.c) #using rectangle to contain the contour
            if self.x < self.min_x:
                self.min_x = self.x
            if self.y < self.min_y:
                self.min_y = self.y
            if self.x + self.w > self.max_x:
                self.max_x = self.x + self.w
            if self.y + self.h > self.max_y:
                self.max_y = self.y + self.h
            self.contour_area = cv2.contourArea(self.c)
            if self.contour_area  < self.settings.area_min: #ignore the small contours.
                continue
            self.valid_cnt += 1

        self.dt = self.md_time.get_time()

        if self.valid_cnt == 0:
            return (False, self.dt, self.img)
        cv2.rectangle(self.img, (self.min_x * 2, self.min_y * 2+55), 
                     (self.max_x * 2, self.max_y * 2+55), (0, 255, 0), 1) #draw the smallest rectangle to contains all the contours.
        return (True, self.dt, self.img)

    def _save_img(self):
        """Save the motional image"""
        self.output_path = '{}image_{}_{}_{}_{}_{}_{}.jpg'.format(
            self.settings.output_path, self.dt.year, self.dt.month, self.dt.day, 
            self.dt.hour, self.dt.minute, self.dt.second
        )
        cv2.imwrite(self.output_path, self.ret_img)
        self.images_list.append(self.output_path)
