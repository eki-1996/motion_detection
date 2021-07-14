import cv2
from datetime import datetime, timedelta
import time
import imutils
import requests

# def diffImg(t0, t1, t2):
#     d1 = cv2.absdiff(t2, t1)
#     d2 = cv2.absdiff(t1, t0)
#     return cv2.bitwise_and(d1, d2)

def handleChange(frame):
    #dirname = 'images'
    dt = datetime.now()
    output_path =( "/home/pi/Documents/images/image_" + str(dt.year) + "_"
        + str(dt.month) + "_" + str(dt.day) + "_" + str(dt.hour) + "_"
         + str(dt.minute) + "_" + str(dt.second) + ".jpg")
    #cv2.imshow('image',frame)
    re_value = cv2.imwrite(output_path, frame)
    #cv2.destroyAllWindows()
    return output_path

def sent_line(images_path):
    payload = {'message': 'Motion detected in your home'}
    #images = {'imageFile': open('C:/Users/17168/Desktop/images/d (38).JPG', 'rb')}
    headers = {'Authorization': 'Bearer ' + 'NZ6iMTUaLiyFh3UU7YHJlBWPfReUIaJRZBu4aZ7y9el'}
    response = requests.post('https://notify-api.line.me/api/notify', data=payload, headers=headers)
    number = 0
    for image_path in images_path:
        number += 1
        payload = {'message': str(number) + 'th picture'}
        images = {'imageFile': open(image_path, 'rb')}
        headers = {'Authorization': 'Bearer ' + 'NZ6iMTUaLiyFh3UU7YHJlBWPfReUIaJRZBu4aZ7y9el'}
        response = requests.post('https://notify-api.line.me/api/notify', data=payload, headers=headers, files=images)
        print(response)


if __name__ == '__main__':

    #cap = cv2.VideoCapture('rtsp://ekicamera:qwe0123987@192.168.11.2:554/stream1')

    while(True):
        dt = datetime.now()
        print(dt)
        if dt > dt.replace(hour=7, minute=20) and dt < dt.replace(hour=17, minute=22):


            cap = cv2.VideoCapture('rtsp://ekicamera:qwe0123987@192.168.11.9:554/stream2')

            if cap.isOpened() != True:
                cap.open('rtsp://ekicamera:qwe0123987@192.168.11.9:554/stream2')
                if cap.isOpened() != True:
                    continue
            #img_minus = cap.read()[1]
            ret, img = cap.read()
            print(img.shape)
            print(ret)
            if ret != True:
                continue
            crop_img = img[68:1081, 0:1920]
            #img = imutils.resize(img, width=500)
            ret, img_plus = cap.read()
            print(ret)
            if ret != True:
                continue
            crop_img_plus = img_plus[68:1081, 0:1920]
            #img_plus = imutils.resize(img_plus, width=500)

            #t_minus = cv2.cvtColor(img_minus, cv2.COLOR_RGB2BGR)
            #t_minus = cv2.GaussianBlur(t_minus, (21,21), 0)
            t = cv2.cvtColor(crop_img, cv2.COLOR_RGB2GRAY)
            t = cv2.GaussianBlur(t, (21,21), 0)
            t_plus = cv2.cvtColor(crop_img_plus, cv2.COLOR_RGB2GRAY)
            t_plus = cv2.GaussianBlur(t_plus, (21,21), 0)
            
            count = 0
            count_1 = 0
            mark = 0
            images_path = []
            second = 0
            dt_last = dt
            second = timedelta(seconds=1)
            minute = timedelta(minutes=4)
            
            while(True):
                dt = datetime.now()
                if dt > dt.replace(hour=17, minute=22):
                    break

                if count_1 != 0:
                    if dt >= dt_last + minute and mark == 1:
                        break
                    ret, img = cap.read()
                    print(ret)
                    if ret != True:
                        break
                    crop_img = img[68:1081, 0:1920]
                    t = t_plus
                    t_plus = cv2.cvtColor(crop_img, cv2.COLOR_RGB2GRAY)
                    t_plus = cv2.GaussianBlur(t_plus, (21,21), 0)


                if count_1 == 0 or dt >= dt_last + second:
                    # t = t_plus
                    # t_plus = cv2.cvtColor(crop_img, cv2.COLOR_RGB2GRAY)
                    # t_plus = cv2.GaussianBlur(t_plus, (21,21), 0)
                    count_1 = 1

                    dif = cv2.absdiff(t, t_plus)
                    thresh = cv2.threshold(dif, 25, 225, cv2.THRESH_BINARY)[1]
                    
                    thresh = cv2.dilate(thresh, None, iterations=2)
                    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    cnts = imutils.grab_contours(cnts)

                    mark = 0
                    areamax = 0
                    min_x, min_y, max_x, max_y = 4000, 2000, 0, 0

                    for c in cnts:
                        (x, y, w, h) = cv2.boundingRect(c)
                        if x < min_x:
                            min_x = x
                        if y < min_y:
                            min_y = y
                        if x + w > max_x:
                            max_x = x + w
                        if y + h > max_y:
                            max_y = y + h
                        contour_area = cv2.contourArea(c)
                        if contour_area  < 1000 or w < 50 or h < 50:
                            continue

                        if contour_area > areamax:
                            areamax = contour_area

                        mark = 1
                        

                    if mark != 1:
                        continue

                    cv2.rectangle(img, (min_x, min_y+68), (max_x, max_y+68), (0, 255, 0), 1)

                    dt_last = dt
                    output_path = handleChange(img)
                    images_path.append(output_path)
                    count += 1

                    #cv2.imshow("img", img)
                    #cv2.imshow("Thresh", thresh)
                    #CV2.imshow("dif", dif)
                    key = cv2.waitKey(1) & 0xFF

                    if count > 4:
                        break

                    if key == ord("q"):
                        break
                
            if len(images_path) > 2:
                sent_line(images_path)
                images_path.clear()
            #print(areamax)
            #cv2.destroyAllWindows()
            cap.release()
            time.sleep(10)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        print('wait for working period!')
        time.sleep(60)
