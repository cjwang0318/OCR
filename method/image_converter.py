# coding: utf-8
import base64
import numpy as np
import cv2
img_file = open(r'C:\cjwang\PycharmProjects\PaddleOCR\img_data\DKSH_img\sample\111.jpg','rb')   # 二進位制開啟圖片檔案
img_b64encode = base64.b64encode(img_file.read())  # base64編碼
img_file.close()  # 檔案關閉
img_b64decode = base64.b64decode(img_b64encode)  # base64解碼
img_array = np.frombuffer(img_b64decode,np.uint8) # 轉換np序列
img=cv2.imdecode(img_array,cv2.COLOR_BGR2RGB)  # 轉換Opencv格式
cv2.imwrite("C:\cjwang\PycharmProjects\PaddleOCR\img_data\DKSH_img\sample\copy.jpg",img)
cv2.imshow("img",img)
cv2.waitKey()