import requests

class MD_line:
    """Process line notify"""
    def __init__(self, md):
        """Initialize line attributes"""
        self.settings = md.settings
        self.headers = {'Authorization': 'Bearer {}'.format(
            self.settings.line_notify_token)}
    
    def send_line(self, images_list):
        """Send a message and the images to your line notify"""
        self.payload = {'message': 'Motion detected in your home'}
        self.response = requests.post(
            'https://notify-api.line.me/api/notify', 
            data=self.payload, headers=self.headers)
        self.number = 0
        for image in images_list:
            self.number += 1
            self.payload = {'message': '{}th picture'.format(self.number)}
            self.images = {'imageFile': open(image, 'rb')}
            response = requests.post(
                'https://notify-api.line.me/api/notify', 
                data=self.payload, headers=self.headers, files=self.images)