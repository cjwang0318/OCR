# -*- coding: utf-8 -*-
import os
import base64
import numpy as np
import cv2
from opencc import OpenCC
from PIL import Image

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"
from paddleocr import PaddleOCR, draw_ocr


def convert_s2tw(str):
    cc = OpenCC('s2tw')  # convert from Simplified Chinese to Traditional Chinese
    converted = cc.convert(str)
    return converted


def converImgtoBase64(img_file_path):
    img_file = open(img_file_path, 'rb')  # 二進位制開啟圖片檔案
    img_b64encode = base64.b64encode(img_file.read())  # base64編碼
    img_file.close()  # 檔案關閉
    return img_b64encode


def converBase64toImg(img_b64encode, isShow):
    img_b64decode = base64.b64decode(img_b64encode)  # base64解碼
    img_array = np.frombuffer(img_b64decode, np.uint8)  # 轉換np序列
    img = cv2.imdecode(img_array, cv2.COLOR_BGR2RGB)  # 轉換Opencv格式
    cv2.imwrite("./ocr_input_img.jpg", img)
    if isShow:
        cv2.imshow("img", img)
        cv2.waitKey()

def getResult(ocrModel, img_b64code):
    img_input_path = "./ocr_input_img.jpg"
    img_output_path = "./ocr_result_img.jpg"
    converBase64toImg(img_b64code, False)
    result = ocr.ocr(img_input_path, cls=True)
    ocrText = []
    for line in result:
        line = convert_s2tw(line[1][0])
        ocrText.append(line)
        print(line)
    # 显示结果
    image = Image.open(img_path).convert('RGB')
    boxes = [line[0] for line in result]
    # txts = [line[1][0] for line in result]
    # scores = [line[1][1] for line in result]
    im_show = draw_ocr(image, boxes, font_path='../img_data/ppocr_img/fonts/simfang.ttf')
    im_show = Image.fromarray(im_show)
    im_show.save(img_output_path)
    ocr_img_b64code = converImgtoBase64(img_output_path)
    converBase64toImg(ocr_img_b64code, True)
    # 建立為傳json結果
    ans = {"ocr_img_b64code": ocr_img_b64code}
    ans["ocr_txt"] = ocrText
    return ans


if __name__ == '__main__':
    img_path = '../img_data/ppocr_img/imgs/11.jpg'
    # ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=True, det_model_dir = det_path, rec_model_dir = rec_path) #sever model
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # orginal mobil model
    # ocr = PaddleOCR(use_angle_cls=True, lang='chinese_cht', use_gpu=True, rec_model_dir=cht_mobile_rec_path)  # sever model
    ans = getResult(ocr, converImgtoBase64(img_path))
    print(ans)
