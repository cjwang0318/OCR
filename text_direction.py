# -*- coding: utf-8 -*-
import os
import base64
import numpy as np
import cv2
from opencc import OpenCC
from PIL import Image
from OCR.method import image_converter
import operator

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"
from paddleocr import PaddleOCR, draw_ocr

cls_model = "./OCR_Model/ch_ppocr_mobile_v2.0_cls_infer"
# cls_model = "./OCR_Model/ch_ppocr_mobile_v2.0_cls_slim_infer"

ch_PP_OCRv4_server_det = "./OCR_Model/ch_PP-OCRv4_det_server_infer"


def getBBX(ocrModel, img_input_path, num_of_image_for_check):
    result = ocrModel.ocr(img_input_path, cls=False, rec=False, det=True)
    path = "./img_data/direction_check"
    fileList = []
    if not os.path.isdir(path):
        os.mkdir(path)
    img = cv2.imread(img_input_path)
    count = 0
    for i, line in reversed(list(enumerate(result))):
        if count < num_of_image_for_check:
            # print(line[0]) #左上頂點
            # print(line[2]) #右下頂點
            imgCrop = img[int(line[0][1]):int(line[2][1]), int(line[0][0]):int(line[2][0])]
            fileName = f'{path}/direction_check_{i}.jpg'
            cv2.imwrite(fileName, imgCrop)
            fileList.append(fileName)
        else:
            break
        count += 1
    return fileList


def getDirection(ocrModel, img_input_path):
    result = ocrModel.ocr(img_input_path, cls=True, rec=False, det=False)

    for line in result:
        print(f"Direction={line[0]}")
        print(f"Confidence={line[1]}")
        directionType = line[0]
        confidence = line[1]
    return directionType, confidence


def direction_detection(ocrModel, img_path, fileList):
    img = cv2.imread(img_path)  # original img file
    dir_dict={ '0,180': 0.0, '180,180': 0.0, '180,0': 0.0, '0,0': 0.0}
    for fileName in fileList:
        img_check = cv2.imread(fileName)
        direction = ""
        weight = 0
        ckeckName=fileName
        for i in range(2):
            if i > 0:
                output_ROTATE_90_CLOCKWISE = cv2.rotate(img_check, cv2.ROTATE_90_CLOCKWISE)
                cv2.imwrite('./temp.jpg', output_ROTATE_90_CLOCKWISE)
                fileName = './temp.jpg'
            directionType, confidence = getDirection(ocrModel, fileName)
            if i > 0:
                direction = direction + directionType
            else:
                direction = direction + directionType + ","
            weight = weight + confidence
        weight = weight / 2
        print(f"{ckeckName} direction:{direction} and weight:{weight}")
        value=dir_dict[direction]
        dir_dict[direction]=value+weight
    print(dir_dict)
    direction=max(dir_dict.items(), key=operator.itemgetter(1))[0]
    print(direction)
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
    img_path = './img_data/60_real.jpg'
    num_of_image_for_check = 30
    # ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=True, det_model_dir = det_path, rec_model_dir = rec_path) #sever model
    # ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # orginal mobil model
    # ocr = PaddleOCR(use_angle_cls=True, lang='chinese_cht', use_gpu=True, rec_model_dir=cht_mobile_rec_path)  # sever model
    ocrModel = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=True, cls_model_dir=cls_model,
                         det_model_dir=ch_PP_OCRv4_server_det)  # cht sever model
    fileList = getBBX(ocrModel, img_path, num_of_image_for_check)
    ans = direction_detection(ocrModel, img_path, fileList)
    print(ans)
