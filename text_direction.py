# -*- coding: utf-8 -*-
import os
import base64
import numpy as np
import cv2
from opencc import OpenCC
from PIL import Image
from OCR.method import image_converter

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"
from paddleocr import PaddleOCR, draw_ocr

cls_model = "./OCR_Model/ch_ppocr_mobile_v2.0_cls_slim_infer"


def getDirection(ocrModel, img_input_path):
    result = ocrModel.ocr(img_input_path, cls=True, rec=False, det=False)
    for line in result:
        # print(f"Direction={line[0]}")
        # print(f"Confidence={line[1]}")
        directionType = line[0]
        confidence = line[1]
    return directionType, confidence


def direction_detection(ocrModel, img_path):
    img = cv2.imread(img_path)
    direction = ""
    weight = 0
    for i in range(2):
        if i > 0:
            output_ROTATE_90_CLOCKWISE = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            cv2.imwrite('./temp.jpg', output_ROTATE_90_CLOCKWISE)
            img_path = './temp.jpg'
        directionType, confidence = getDirection(ocrModel, img_path)
        if i > 0:
            direction = direction + directionType
        else:
            direction = direction + directionType + ","
        weight = weight + confidence
    weight = weight / 2
    print(direction)
    print(weight)
    if direction == "0,180":
        ans = "ROTATE_0_CLOCKWISE"
        cv2.imwrite('./direction_result.jpg', img)
    elif direction == "180,180":
        ans = "ROTATE_90_COUNTERCLOCKWISE"
        output_ROTATE_90_COUNTERCLOCKWISE = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        cv2.imwrite('./direction_result.jpg', output_ROTATE_90_COUNTERCLOCKWISE)
    elif direction == "180,0":
        ans = "ROTATE_180"
        output_ROTATE_180 = cv2.rotate(img, cv2.ROTATE_180)
        cv2.imwrite('./direction_result.jpg', output_ROTATE_180)
    elif direction == "0,0":
        ans = "ROTATE_90_CLOCKWISE"
        output_ROTATE_90_CLOCKWISE = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        cv2.imwrite('./direction_result.jpg', output_ROTATE_90_CLOCKWISE)
    else:
        ans = "ROTATE_0_CLOCKWISE"
        cv2.imwrite('./direction_result.jpg', img)
    return ans


if __name__ == '__main__':
    img_path = './img_data/4.jpg'
    # ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=True, det_model_dir = det_path, rec_model_dir = rec_path) #sever model
    # ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # orginal mobil model
    # ocr = PaddleOCR(use_angle_cls=True, lang='chinese_cht', use_gpu=True, rec_model_dir=cht_mobile_rec_path)  # sever model
    ocrModel = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=True, cls_model_dir=cls_model)  # cht sever model
    ans = direction_detection(ocrModel, img_path)
    print(ans)
