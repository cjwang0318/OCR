# -*- coding: utf-8 -*-
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"
from paddleocr import PaddleOCR, draw_ocr
from opencc import OpenCC

# img_path = './ppocr_img/imgs/11.jpg'
# img_path = './DKSH_img\sample/546150.jpg'
# img_path = './DKSH_img\sample/546151.jpg'
# img_path = './DKSH_img\sample/546159.jpg'
# img_path = './DKSH_img\sample/546161.jpg'
# img_path = './post_img/Image_20201019203901_adjust.jpg'
# img_path = './測試影像/2_cut.jpg'
#img_path = './test.jpg'
#img_path = './img_data/family_img/1_46,60,88,96.jpg'
#img_path = './img_data/handwriting/49.jpg'
#img_path = './img_data/包裝日期/1.png'
img_path = './img_data/合通/其他憑證-1.tif'


PPOCRv2_det_path = "./OCR_Model/ch_PP-OCRv2_det/ch_PP-OCRv2_det_infer"
ch_PP_OCRv3_det = "./OCR_Model/ch_PP_OCRv3_det/ch_PP_OCRv3_det_infer"
ch_PP_OCRv4_server_det = "./OCR_Model/ch_PP-OCRv4_det_server_infer"
mobile_det_path = "./OCR_Model/ch_ppocr_mobile_v2.0_det/ch_ppocr_mobile_v2.0_det_infer"
server_det_path = "./OCR_Model/ch_ppocr_server_v2.0_det/ch_ppocr_server_v2.0_det_infer"
en_ppocr_mobile_v2_table_det="./OCR_Model/en_ppocr_mobile_v2.0_table_det/en_ppocr_mobile_v2.0_table_det_infer"

ch_PP_OCRv4_server_rec = "./OCR_Model/ch_PP-OCRv4_rec_server_infer"
server_rec_path = "./OCR_Model/ch_ppocr_server_v2.0_rec/ch_ppocr_server_v2.0_rec_infer"
cht_rec_path = "./OCR_Model/chinese_cht_mobile_v2.0_rec/chinese_cht_mobile_v2.0_rec_infer"

# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
#ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=True, det_model_dir = server_det_path, rec_model_dir = server_rec_path) #sever model
#ocr = PaddleOCR(use_angle_cls=True, lang="ch")  #orginal mobil model
#ocr = PaddleOCR(use_angle_cls=True, lang='chinese_cht', use_gpu=True, det_model_dir = en_ppocr_mobile_v2_table_det,rec_model_dir=cht_rec_path)  # cht sever model
ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=True, det_model_dir = ch_PP_OCRv4_server_det, rec_model_dir = ch_PP_OCRv4_server_rec) #sever model
result = ocr.ocr(img_path, cls=True)
for line in result:
    print(line)

def convert_s2tw(str):
    cc = OpenCC('s2tw')  # convert from Simplified Chinese to Traditional Chinese
    converted = cc.convert(str)
    return converted
# 显示结果
from PIL import Image
image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
#txts = [line[1][0] for line in result] #檢體顯示
txts = [convert_s2tw(line[1][0]) for line in result] #繁體顯示
scores = [line[1][1] for line in result]
im_show = draw_ocr(image, boxes, txts, scores, font_path='./img_data/ppocr_img/fonts/simfang.ttf')
im_show = Image.fromarray(im_show)
im_show.save('其他憑證-1.jpg')
