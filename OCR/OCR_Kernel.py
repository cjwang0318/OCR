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


def convert_s2tw(str):
    cc = OpenCC('s2tw')  # convert from Simplified Chinese to Traditional Chinese
    converted = cc.convert(str)
    return converted


def getResult(ocrModel, img_b64code):
    img_input_path = "./ocr_input_img.jpg"
    img_output_path = "./ocr_result_img.jpg"
    image_converter.Json_converBase64toImg(img_b64code, img_input_path, False)
    result = ocrModel.ocr(img_input_path, cls=True)
    ocrText = []
    for line in result:
        line = convert_s2tw(line[1][0])
        ocrText.append(line)
        print(line)
    # 显示结果
    image = Image.open(img_input_path).convert('RGB')
    boxes = [line[0] for line in result]
    # txts = [line[1][0] for line in result]
    # scores = [line[1][1] for line in result]
    im_show = draw_ocr(image, boxes, font_path='../img_data/ppocr_img/fonts/simfang.ttf')
    im_show = Image.fromarray(im_show)
    im_show.save(img_output_path)
    ocr_img_b64code = image_converter.Json_converImgtoBase64(img_output_path)
    # 建立為傳json結果
    ans = {"ocr_img_b64code": ocr_img_b64code}
    ans["ocr_txt"] = ocrText
    return ans


if __name__ == '__main__':
    img_path = '../img_data/ppocr_img/imgs/11.jpg'
    # ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=True, det_model_dir = det_path, rec_model_dir = rec_path) #sever model
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # orginal mobil model
    # ocr = PaddleOCR(use_angle_cls=True, lang='chinese_cht', use_gpu=True, rec_model_dir=cht_mobile_rec_path)  # sever model
    ans = getResult(ocr, image_converter.Json_converImgtoBase64(img_path))
    print(ans)
