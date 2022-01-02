# coding: utf-8
import base64
import numpy as np
import cv2


def converImgtoBase64(img_file_path):
    img_file = open(img_file_path, 'rb')  # 二進位制開啟圖片檔案
    img_b64encode = base64.b64encode(img_file.read())  # base64編碼
    img_file.close()  # 檔案關閉
    return img_b64encode


def Json_converImgtoBase64(img_file_path):
    img = cv2.imread(img_file_path)
    string = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    return string


def converBase64toImg(img_b64encode, img_file_path, isShow):
    img_b64decode = base64.b64decode(img_b64encode)  # base64解碼
    img_array = np.frombuffer(img_b64decode, np.uint8)  # 轉換np序列
    img = cv2.imdecode(img_array, cv2.COLOR_BGR2RGB)  # 轉換Opencv格式
    cv2.imwrite(img_file_path, img)
    if isShow:
        cv2.imshow("img", img)
        cv2.waitKey()


def Json_converBase64toImg(img_b64encode, img_file_path, isShow):
    jpg_original = base64.b64decode(img_b64encode)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    cv2.imwrite(img_file_path, img)
    if isShow:
        cv2.imshow("img", img)
        cv2.waitKey()


if __name__ == '__main__':
    img_file = open(r'C:\cjwang\PycharmProjects\PaddleOCR\img_data\DKSH_img\sample\111.jpg', 'rb')  # 二進位制開啟圖片檔案
    img_b64encode = base64.b64encode(img_file.read())  # base64編碼
    img_file.close()  # 檔案關閉
    img_b64decode = base64.b64decode(img_b64encode)  # base64解碼
    img_array = np.frombuffer(img_b64decode, np.uint8)  # 轉換np序列
    img = cv2.imdecode(img_array, cv2.COLOR_BGR2RGB)  # 轉換Opencv格式
    cv2.imwrite("C:\cjwang\PycharmProjects\PaddleOCR\img_data\DKSH_img\sample\copy.jpg", img)
    cv2.imshow("img", img)
    cv2.waitKey()
