from typing import Tuple
from numpy.lib.arraypad import pad
import pandas as pd
import numpy as np

from iqradre.segment.prod import SegmentationPredictor
from iqradre.detect.pred import BoxesPredictor
from iqradre.detect.ops import boxes as boxes_ops

from iqradre.recog.prod import TextPredictor, TesseractPredictor

import transformers
from transformers import BertTokenizer
from iqradre.extract.prod.prod import Extractor
from iqradre.extract.prod import utils as text_utils
from iqradre.extract.config import label as label_cfg


import matplotlib.pyplot as plt
# from iqradre.detect.ops import box_ops
# from iqradre.extract.ops import boxes_ops

from deskew import determine_skew
from skimage.transform import rotate
import imutils
import cv2 as cv
from . import utils
import torch
import pathlib
import PIL
import time

from . import functional as PF


class IDCardPredictor(object):
    def __init__(self, config, device='cpu', use_tesseract=False):
        self.config = config
        self.device = device
        self.use_tesseract = use_tesseract
        
        self._init_model()
    
    def _init_model(self):
        print(f'INFO: Load all model, please wait...')
        self.segmentor = None
        if self.config.get('segmentor', False):
            self.segmentor = SegmentationPredictor(weight_path=self.config['segmentor'], device=self.device,
                                                  start_feat=self.config.get('segmentor_start_feat', 32))
        self.boxes_detector = BoxesPredictor(weight_path=self.config['detector'], device=self.device)
        
        if self.use_tesseract:
            self.text_recognitor = TesseractPredictor()
        else:
            self.text_recognitor = TextPredictor(weight_path=self.config['recognitor'], device=self.device)
        
        self.tokenizer = BertTokenizer.from_pretrained(self.config["tokenizer"])
        self.info_extractor = Extractor(tokenizer=self.tokenizer, weight=self.config['extractor'], device='cpu')
        print(f'INFO: All model has been loaded!')
        
    def _clean_boxes_result(self, boxes_result, min_size_percent=2):
        polys, boxes, images_patch, img, score_text, score_link, ret_score_text = boxes_result
        
        #find max
        sizes = [im.shape[1] for im in images_patch]
        max_index, max_value = max(enumerate(sizes), key=lambda x: x[1])

        #create percent by max size
        percent_size = [int(size/max_value * 100) for size in sizes]

        #exclude with minimum_size
        remove_indices = [i for i, psize in enumerate(percent_size) if psize<=min_size_percent]
        # images_patch = np.delete(images_patch, remove_indices).tolist()
        new_boxes = []
        new_images_patch = []
        for i in range(len(images_patch)):
            if not i in remove_indices:
                new_boxes.append(boxes[i])
                new_images_patch.append(images_patch[i])
        new_boxes = np.array(new_boxes)
        boxes_result = polys, new_boxes, new_images_patch, img, score_text, score_link, ret_score_text
        
        return boxes_result
    
    def _resize_normalize(self, image:np.ndarray, dsize=(750, 1000), pad_color=0):
        try:
            outimg = utils.resize_pad(image, size=dsize, pad_color=pad_color)
        except:
            h,w = image.shape[:2]
#             print(f'resize exception ori size:({h},{w})')
            ratio = h/w
            if ratio<1.3:
                nh = int(h * 1.3)
                dim = (nh, w)
                outimg = cv.resize(image, dim, interpolation=cv.INTER_LINEAR)
                size = outimg.shape[:2]
#                 print(f'resize Exception new size: {size}')
        
        return outimg
    
    
    def _crop_from_scanner(self, image, g1=220, g2=50, pfac=0.1):
        if type(image) == str:
            im_path = pathlib.Path(image)
            image = PIL.Image.open(str(im_path))
            image = np.array(image)
            
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray, (1,1), 2000)
        flag, thresh = cv.threshold(blur, g1, g2, cv.THRESH_BINARY_INV) 
        # canny = cv.Canny(thresh, g1, g2)
        
        contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv.contourArea, reverse=True)[:10] 
        
        boxes = []
        for card in contours:
            peri = cv.arcLength(card, True)
            box = cv.boundingRect(card)
            boxes.append(box)
            
        box = boxes[0]
        box = utils.xywh2xymm(box)
        box = utils.pad(box, factor=pfac)
        (xmin,ymin,xmax,ymax) = box
        x,y,w,h = utils.xymm2xywh(box)
        # box np.array(box)
        # box = utils.box_coordinate_to_xyminmax(box)
        # image = cv.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
        crop = image[ymin:ymax, xmin:xmax]
        crop = PIL.Image.fromarray(crop)
        
        return crop,  box
    
    def _draw_bbox_image(self, image, raw_data):
        img = image.copy()
        for key, values in raw_data.items():
            for val in values:
                word, box, label = val
                color = label_cfg.label_colors[label]
                box = boxes_ops.xymm2coord(box, to_int=True)
                box = np.array(box)
                img = cv.polylines(img, [box], True, color, 2)
        return img
    
    def _segment_predictor(self, impath):
        if self.config.get('segmentor', False):
            image, bbox_mask, mask, combined = self.segmentor.predict_canvas(impath, mask_color="#ffffff")
            
            # import matplotlib.pyplot as plt
            # plt.imshow(combined)
#             print('segment_predictor size ==>',combined.size)
            
            combined = combined.convert("RGB")
            result = np.array(combined).astype(np.uint8)
            return result, bbox_mask, mask
        else:
            return impath, None, None
    
    def _segment_predict(self, impath):
        unet_stime = time.time()
        img_segment, img_bbox, img_mask = self._segment_predictor(impath)
        unet_etime = time.time()
        unet_time = unet_etime - unet_stime
        return img_segment, img_bbox, img_mask, unet_time
        
    def _detect_boxes(self, impath, text_threshold=0.7, link_threshold=0.3, low_text=0.5, min_size_percent=5):
        result = self.boxes_detector.predict_word_boxes(impath, 
                                                        text_threshold=text_threshold, 
                                                        link_threshold=link_threshold, 
                                                        low_text=low_text)
        polys, boxes, images_patch, img, score_text, score_link, ret_score_text = result
        return result
    
    def _craft_predict(self, img_norm, text_threshold=0.7, link_threshold=0.3, low_text=0.3, min_size_percent=3):
        craft_stime = time.time()
        boxes_result = self._detect_boxes(img_norm, 
                                          text_threshold=text_threshold,
                                          link_threshold=link_threshold,
                                          low_text=low_text)
        boxes_result = self._clean_boxes_result(boxes_result, min_size_percent=min_size_percent)
        polys, boxes, images_patch, image, score_text, score_link, ret_score_text = boxes_result
        boxes_list = boxes_ops.batch_coord2xymm(boxes, to_int=True).tolist() 
        craft_etime = time.time()
        craft_time = craft_etime - craft_stime
        
        return boxes_list, boxes, images_patch, image, score_text, score_link, craft_time
        
    def _auto_deskew(self, impath, resize=False):
        result = self._detect_boxes(impath)
        polys, boxes, images_patch, img, score_text, score_link, ret_score_text = result
        
        angle = determine_skew(score_text+score_link)
        rotated_img = rotate(img, angle, resize=True, cval=1)
        
        rotated_img = (rotated_img * 255).astype(np.uint8)
        
        if resize:
            shape = rotated_img.shape[:2]
            max_index = shape.index(max(shape))
            if max_index == 1:
                rotated_img = imutils.resize(rotated_img, width=1000)
            else:
                rotated_img = imutils.resize(rotated_img, height=1000)
        
        return rotated_img, angle
    
    def _deskew_normalize(self, img_segment, resize: bool = True, dsize: tuple = (1500,2000)):
        normdesk_stime = time.time()
        img_rot, angle = self._auto_deskew(img_segment, resize=resize)
        img_norm = self._resize_normalize(img_rot, dsize=dsize)
        normdesk_etime = time.time()
        
        normdesk_time = normdesk_etime - normdesk_stime
        return img_rot, img_norm, normdesk_time, angle
    
    def _recognize_predict(self, images_patch):
        crnn_stime = time.time()
        text_list =  self.text_recognitor.predict(images_patch)
        crnn_etime = time.time()
        crnn_time = crnn_etime - crnn_stime
        return text_list, crnn_time
    
    def _extractor_predict(self, text_list, boxes):
        layoutlm_stime = time.time()
        annoset = text_utils.build_annoset(text_list, boxes)
        annoset = sorted(annoset, key = lambda i: (i['bbox'][1], i['bbox'][0]))
        data, clean, raw = self.info_extractor.predict(annoset)  
        dframe = pd.DataFrame(clean)
        layoutlm_etime = time.time()
        layoutlm_time = layoutlm_etime - layoutlm_stime
        
        return data, dframe, annoset, raw, layoutlm_time
    
    
    def predict(self, image, mode='mobile', resize: bool = True, dsize: Tuple[int, int] = (1500,2000),
                text_threshold: float = 0.7, link_threshold: float = 0.3, low_text: float = 0.3, 
                min_size_percent: int = 3, scanline: bool = True, draw_bbox_image: bool = False,
                return_images: bool = False, return_patches: bool = False):
        
        if mode!='mobile':
            image, box = self._crop_from_scanner(image)
        
        # UNET Network
        img_segment, img_bbox, img_mask, unet_time = self._segment_predict(image)
        
        #Deskew
        img_rot, img_norm, normdesk_time, angle = self._deskew_normalize(img_segment, resize=resize, dsize=dsize)
        
        # CRAFT network
        result_craft = self._craft_predict(img_norm, text_threshold=text_threshold, 
                                           link_threshold=link_threshold, low_text=low_text,
                                           min_size_percent=min_size_percent)
        boxes_list, boxes, images_patch, image, score_text, score_link, craft_time = result_craft

        # CRNN Network
        text_list, crnn_time = self._recognize_predict(images_patch)
        
        # Layoutlm Network
        data, dframe, annoset, raw, layoutlm_time = self._extractor_predict(text_list, boxes)
        
        
        if scanline:
            nama_sorted = PF.prediction_scanline_sorted(boxes_list, text_list, data, key="nama", key_stop="tempat")
            alamat_sorted = PF.prediction_scanline_sorted(boxes_list, text_list, data, key="alamat", key_stop="rt/rw")
            data['nama'] = nama_sorted
            data['alamat'] = alamat_sorted

        
        output = {
            'data': data,
            'dframe':dframe,
            'annoset': annoset,
            'images': {},
            'patches': {},
            'times': {}
        }
        
        
        if return_images:
            output["images"] = {
                'original': utils.npimage_to_pilimage(image),
                'drawbox': None,
                'segmented': utils.npimage_to_pilimage(img_segment),
                'segmented_mask': utils.npimage_to_pilimage(utils.npimage_to_viridis(np.array(img_mask))),
                'segmented_bbox': utils.npimage_to_pilimage(utils.npimage_to_viridis(np.array(img_bbox))),
                'rotated': utils.npimage_to_pilimage(img_rot),
                'score_text': utils.score_to_pilimage(score_text),
                'score_link': utils.score_to_pilimage(score_link),
                'score_combine': utils.score_combine_to_pilimage(score_text+score_link),
            }
            
            
        if draw_bbox_image and return_images:
            labels = dframe['labels'].tolist()
            drawbox = self._draw_bbox_image(img_norm, raw)
            output['images']['drawbox'] = utils.npimage_to_pilimage(drawbox)
            
        
        if return_patches:
            output["patches"] = {
                'boxes': boxes_list,
                'texts': text_list,
                'images': images_patch,
           } 
           
           
        output['times'] = {
            'unet': f'{(unet_time):.4f} s',
            'deskew': f'{(normdesk_time):.4f} s',
            'craft': f'{(craft_time):.4f} s',
            'crnn': f'{(crnn_time):.4f} s',
            'layoutlm': f'{(layoutlm_time):.4f} s',
        }
        
        return output
        
        
   