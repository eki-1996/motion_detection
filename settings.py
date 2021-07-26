class Settings:
    """A class to store all settings for Motion Detection"""

    def __init__(self):
        """Initialize the program's settings"""

        #Path for save the picture on your device
        self.output_path = 'C:/Users/17168/Desktop/images/'

        #Your line notify token
        self.line_notify_token = 'NZ6iMTUaLiyFh3UU7YHJlBWPfReUIaJRZBu4aZ7y9el'

        #The time range your want this progrom works
        self.time_range = {'start_time': {'hour': 7, 'minute': 20},
                           'end_time': {'hour': 23, 'minute': 22}}

        #Username, password, ipadress of your ip camera and the stream
        self.rtsp = {'username': 'ekicamera', 
                     'password': 'qwe0123987',
                     'ipadress': '192.168.11.9',
                     'stream': 'stream1'}

        #minimun area for a motion
        self.area_min = 500
        
        #Time limitaion of first valid motion detected
        self.time_limit = {'minute': 4}

        #Time intervel between images
        self.time_intervel = {'milliseconds': 100}

        #The max and min number of pictures that will be send to your line
        self.picture_num =  {'max': 5, 'min': 3}