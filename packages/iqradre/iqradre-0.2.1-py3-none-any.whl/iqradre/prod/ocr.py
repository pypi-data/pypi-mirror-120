from enum import auto
from typing import Any, Dict, Optional, Tuple, Union
from numpy.lib.arraypad import pad
import pandas as pd
import numpy as np

from iqradre.detect.pred import BoxesPredictor
from iqradre.detect.ops import boxes as boxes_ops
from iqradre.recog.prod import TextPredictor, TesseractPredictor

from iqradre.extract.prod import utils as text_utils
from iqradre.detect.pred import functional as DPF

from . import functional as PF
from . import utils
 

import matplotlib.pyplot as plt
from deskew import determine_skew
from skimage.transform import rotate
import imutils
import cv2 as cv
import torch
import pathlib
from PIL import Image
import PIL
import time

# __all__ = ['OCRPredictor']

class OCRPredictor(object):
    def __init__(self, config: dict, device: str = 'cpu', use_tesseract: bool = False):
        self.config = config
        self.device = device
        self.use_tesseract = use_tesseract
        
        self._init_model()
    
    def _init_model(self):
        self.boxes_detector: BoxesPredictor = BoxesPredictor(weight_path=self.config['detector'], device=self.device)
        
        if self.use_tesseract:
            self.text_recognitor: TesseractPredictor = TesseractPredictor()
        else:
            self.text_recognitor: TextPredictor = TextPredictor(weight_path=self.config['recognitor'], device=self.device)
        print(f'INFO: All model has been loaded!')
        
    def _detect_word_boxes(self, impath, text_threshold=0.7, link_threshold=0.3, low_text=0.5, min_size_percent=5):
        result = self.boxes_detector.predict_word_boxes(impath, 
                                                        text_threshold=text_threshold, 
                                                        link_threshold=link_threshold, 
                                                        low_text=low_text)
        polys, boxes, images_patch, img, score_text, score_link, ret_score_text = result
        return result
    
    
    def _detect_char_boxes(self, impath, low_text=0.3, mag_ratio=1):
        result = self.boxes_detector.predict_char_boxes(impath, low_text=low_text, mag_ratio=mag_ratio)
        
        boxes, score_text, score_link, image, images_patch = result
#         boxes, score_text, score_link, image, images_patch
#         polys, boxes, images_patch, img, score_text, score_link, ret_score_text = result
        return result
    
    def _auto_deskew_word(self, impath, resize=False):
        result = self._detect_word_boxes(impath)
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
    
    
    def _auto_deskew_char(self, impath, resize=False):
        result = self._detect_char_boxes(impath)
#         polys, boxes, images_patch, img, score_text, score_link, ret_score_text = result
        boxes, score_text, score_link, image, images_patch = result
        
        angle = determine_skew(score_text+score_link)
        rotated_img = rotate(image, angle, resize=True, cval=1)
        
        rotated_img = (rotated_img * 255).astype(np.uint8)
        
        if resize:
            shape = rotated_img.shape[:2]
            max_index = shape.index(max(shape))
            if max_index == 1:
                rotated_img = imutils.resize(rotated_img, width=1000)
            else:
                rotated_img = imutils.resize(rotated_img, height=1000)
        
        return rotated_img, angle
    
    
    def _clean_word_boxes_result(self, boxes_result, min_size_percent=2):
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
    
    def _clean_char_boxes_result(self, boxes_result, min_size_percent=2)->tuple:
        boxes, score_text, score_link, image, images_patch = boxes_result
        
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
#         boxes_result = polys, new_boxes, new_images_patch, img, score_text, score_link, ret_score_text
        boxes_result = new_boxes, new_images_patch, image, score_text, score_link
        
        return boxes_result
    
    def _resize_normalize(self, image:np.ndarray, dsize=(750, 1000), pad_color=0)->np.ndarray:
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
    
    def _draw_bbox_image(self, image, raw_data):
        img = image.copy()
        for idx, data in enumerate(raw_data):
            word, box = data['text'], data['bbox']
            color = (0, 255, 255)
            box = boxes_ops.xymm2coord(box, to_int=True)
            box = np.array(box)
            img = cv.polylines(img, [box], True, color, 2)
        return img
    
    def _threshold_otsu_invert(self, image: np.ndarray):
        image_gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
        ret, thresh = cv.threshold(image_gray, 127, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        ret, thresh = cv.threshold(thresh, 0, 255, cv.THRESH_BINARY_INV)
        image = cv.merge((thresh, thresh, thresh))
        return image
    
    def _load_image(self, image: Union[str, np.ndarray, Image.Image]) -> np.ndarray:
        if type(image)==PIL.Image.Image:
            image = np.array(image).astype(np.uint8)
            
        if type(image)==str:
            image = DPF.load_image(image)
        
        return image


    def _predict_word(self, image, autodeskew: bool = False, deskew_resize: bool = True,
                      normalize: bool = False, normalize_dsize: Tuple[int, int] = (1500,2000),
                      text_threshold: float = 0.7, link_threshold: float = 0.3, 
                      low_text: float = 0.3, min_size_percent: int = 3, 
                      return_images: bool = True, draw_bbox_image: bool = False,
                      invert=False, scanline: bool = True, ) -> Dict[Any, Any]:
        
        image = self._load_image(image)
        
        if invert:
            image = self._threshold_otsu_invert(image)
            
        # auto deskew image
        if autodeskew:
            normdesk_stime = time.time()
            img_rot, angle = self._auto_deskew_word(image, resize=deskew_resize)
            normdesk_etime = time.time()
        else:
            img_rot = image
        
        # Normalize image size 
        if normalize:
            img_norm = self._resize_normalize(img_rot, dsize=normalize_dsize)
        else:
            img_norm = img_rot
        
        # CRAFT network
        craft_stime = time.time()
        boxes_result = self._detect_word_boxes(img_norm, 
                                          text_threshold=text_threshold,
                                          link_threshold=link_threshold,
                                          low_text=low_text)
        boxes_result = self._clean_word_boxes_result(boxes_result, min_size_percent=min_size_percent)
        polys, boxes, images_patch, img, score_text, score_link, ret_score_text = boxes_result
        boxes_list = boxes_ops.batch_coord2xymm(boxes, to_int=True).tolist() 
        craft_etime = time.time()
        
        # CRNN Network
        crnn_stime = time.time()
        text_list =  self.text_recognitor.predict(images_patch)
        crnn_etime = time.time()
        
        data_annoset = text_utils.build_annoset(text_list, boxes)
        data_annoset = sorted(data_annoset, key = lambda i: (i['bbox'][1], i['bbox'][0]))
        
        output =  {
            "data": data_annoset,
            "boxes": boxes_list,
            "texts": text_list,
            'times':{
                'craft': f'{(craft_etime - craft_stime):.4f} s',
                'crnn': f'{(crnn_etime - crnn_stime):.4f} s',
            }
        }
        
        if return_images:
            output["images"] =  {
                "original": utils.npimage_to_pilimage(image),
                "normalize": utils.npimage_to_pilimage(img_norm),
                "score_text": utils.score_to_pilimage(score_text),
                "score_link": utils.score_to_pilimage(score_link),
                "score_result": utils.score_combine_to_pilimage(score_text+score_link)
            }
            
        if return_images and draw_bbox_image:
            img_draw = self._draw_bbox_image(img_norm, data_annoset)
            output["images"]["drawbox"] = utils.npimage_to_pilimage(img_draw)
        
        if autodeskew:
            output['times']['deskew'] = f'{(normdesk_etime - normdesk_stime):.4f} s'
            
        return output
    
    
    def _predict_char(self, image: Union[str, np.ndarray, Image.Image], autodeskew: bool = False, deskew_resize: bool = True, 
                      normalize: bool = False, normalize_dsize: Tuple[int, int] = (1500,2000), 
                      low_text: float = 0.5, min_size_percent: int = 3,  scanline: bool = True,
                      draw_bbox_image: bool = False, return_images: bool = True, 
                      invert: bool = False) -> Dict[Any, Any]:
        
        image = self._load_image(image)
       
        if invert: 
            image = self._threshold_otsu_invert(image)
            
        #Deskew
        if autodeskew:
            normdesk_stime = time.time()
            img_rot, angle = self._auto_deskew_char(image, resize=deskew_resize)
            normdesk_etime = time.time()    
        else:
            img_rot = image
            
        if normalize:
            img_norm = self._resize_normalize(img_rot, dsize=normalize_dsize)
        else:
            img_norm = img_rot
        
        # CRAFT network
        craft_stime = time.time()
        boxes_result = self._detect_char_boxes(img_norm, low_text=low_text)
        boxes_result = self._clean_char_boxes_result(boxes_result, min_size_percent=min_size_percent)
        boxes, images_patch, image, score_text, score_link = boxes_result
#         boxes, score_text, score_link, image, images_patch = boxes_result
        boxes_list = boxes_ops.batch_coord2xymm(boxes, to_int=True).tolist() 
        craft_etime = time.time()
        
        # CRNN Network
        crnn_stime = time.time()
        text_list =  self.text_recognitor.predict(images_patch)
        crnn_etime = time.time()
        
        data_annoset = text_utils.build_annoset(text_list, boxes)
        data_annoset = sorted(data_annoset, key = lambda i: (i['bbox'][1], i['bbox'][0]))
        
        output = {
            "data": data_annoset,
            "boxes": boxes_list,
            "texts": text_list,
            'times':{
                'craft': f'{(craft_etime - craft_stime):.4f} s',
                'crnn': f'{(crnn_etime - crnn_stime):.4f} s',
            }
        }
        
        if return_images:
            output["images"] =  {
                "original": utils.npimage_to_pilimage(image),
                "normalize": utils.npimage_to_pilimage(img_norm),
                "score_text": utils.score_to_pilimage(score_text),
                "score_link": utils.score_to_pilimage(score_link),
                "score_result": utils.score_combine_to_pilimage(score_text+score_link)
            }
            
        if return_images and draw_bbox_image:
            img_draw = self._draw_bbox_image(img_norm, data_annoset)
            output["images"]["drawbox"] = utils.npimage_to_pilimage(img_draw)
        
        if autodeskew:
            output['times']['deskew'] = f'{(normdesk_etime - normdesk_stime):.4f} s'
            
        return output
        
    def predict(self, impath, word_mode: bool = True, 
                autodeskew: bool = False, deskew_resize: bool = True, 
                normalize: bool = False, normalize_dsize: Tuple[int, int] = (1500,2000),
                text_threshold: float = 0.7, link_threshold: float = 0.3, low_text: float = 0.3, 
                min_size_percent: int = 3, scanline: bool = True, draw_bbox_image: bool = True, 
                return_images: bool = True, invert: bool = False) -> Dict[Any, Any]:
        
        if word_mode:
            return self._predict_word(impath, autodeskew=autodeskew, deskew_resize=deskew_resize,
                                      normalize=normalize, normalize_dsize=normalize_dsize, 
                                      text_threshold=text_threshold, 
                                      link_threshold=link_threshold, low_text=low_text,
                                      min_size_percent=min_size_percent, scanline=scanline,
                                      draw_bbox_image=draw_bbox_image, return_images=return_images,
                                      invert=invert)
        else:
            return self._predict_char(impath, autodeskew=autodeskew, deskew_resize=deskew_resize,
                                      normalize=normalize, normalize_dsize=normalize_dsize,  
                                      low_text=low_text, min_size_percent=min_size_percent,
                                      scanline=scanline, draw_bbox_image=draw_bbox_image,
                                      return_images=return_images, invert=invert)
            