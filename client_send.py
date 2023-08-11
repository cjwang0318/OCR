# conda install requests
import requests
import time
import base64
import cv2
import numpy as np


def Json_converImgtoBase64(img_file_path):
    img = cv2.imread(img_file_path)
    string = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    return string


def Json_converBase64toImg(img_b64encode, img_file_path, isShow):
    jpg_original = base64.b64decode(img_b64encode)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    cv2.imwrite(img_file_path, img)
    if isShow:
        cv2.imshow("img", img)
        cv2.waitKey()


img_path = './img_data/1.jpg'
img_b64code = Json_converImgtoBase64(img_path)

# print(img_b64code)
sendMessage_json = {
    "image": img_b64code
}

start = time.time()
# sent json to server
# res = requests.post('http://192.168.0.3:5000/getResult', json=sendMessage_json)
res = requests.post('http://192.168.50.29:6000/getResult', json=sendMessage_json)
img_output_path = "./result_img.jpg"
if res.ok:
    outputs = res.json()
    img_ocr_result_b64code = outputs['ocr_img_b64code']
    Json_converBase64toImg(img_ocr_result_b64code, img_output_path, False)
    print(outputs['ocr_txt'])
    print(outputs['date_txt'])

else:
    print("Abnormal return, please have check")
end = time.time()
print('time: ', end - start)
