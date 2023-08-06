
import torch
from ..models.unet import UNet
import pathlib
import PIL
import PIL.Image
from ..data import loader
from . import utils
from PIL import Image, ImageOps

import matplotlib.pyplot as plt


from torchvision.transforms import transforms as VT
from torchvision.transforms import functional as VF

import cv2 as cv
import numpy as np


class SegmentationPredictor(object):
    def __init__(self, weight_path=None, device='cpu', in_chan=3, start_feat=32):
        self.device = device
        self.in_chan = in_chan
        self.start_feat = start_feat
        self._load_model()
        
        self.weight = weight_path
        if self.weight != None:
            self._load_state_dict(weight_path)
            
    def _load_state_dict(self, state_dict_path):
        state_dict = torch.load(state_dict_path)
        self.model.load_state_dict(state_dict)
        self.model = self.model.to(self.device)
        
    def _load_model(self):
        self.model = UNet(in_chan=self.in_chan, n_classes=1, start_feat=self.start_feat, device=self.device)
    
    def _clean_output(self, output): 
        output = output.squeeze()    
        if self.device =="cpu":
            output = output.cpu()
        # output = output.detach()
        return output
    
    def canvas_mask(self, image, mask):
        np_mask = np.array(mask)
        np_image = np.array(image)
        contours, _ = cv.findContours(np_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        (x, y, w, h) = cv.boundingRect(max(contours, key = cv.contourArea))

        mw,mh = mask.size
        canvas = np.zeros((mh,mw), dtype=np.uint8)
        canvas[y:y+h, x:x+w] = 255
        
        croped_area = np_image[y:y+h, x:x+w].copy()
        croped_area = PIL.Image.fromarray(croped_area)
        croped_area = croped_area.convert('RGB')
#         plt.imshow(np_image);plt.show()
#         print('print np_image')
        
        return canvas, croped_area
        
    def predict(self, image, mask_color="#ffffff"):
        self.model.eval()
        if type(image) == str:
            im_path = pathlib.Path(image)
            image = PIL.Image.open(str(im_path))
            image = PIL.ImageOps.exif_transpose(image)
            
        
        w, h = image.size
        image_tmft = utils.valid_tmft(image)
        image_tmft = image_tmft.unsqueeze(dim=0)
        
        with torch.no_grad():
            output = self.model(image_tmft)
            output = torch.sigmoid(output)
        
        output = self._clean_output(output)
        print(output.shape)
        output = VF.to_pil_image(output)
        mask = VF.resize(output, size=(h,w))

        combined = Image.new("RGBA", (w, h), mask_color)
        combined.paste(image, mask=mask)
        
        return image, mask, combined
    
    
    def predict_canvas(self, image, mask_color="#ffffff"):
        self.model.eval()
        
        if type(image) == str:
            im_path = pathlib.Path(image)
            image = PIL.Image.open(str(im_path))
            image = PIL.ImageOps.exif_transpose(image)
        
        w, h = image.size
        image_tmft = utils.valid_tmft(image)
        image_tmft = image_tmft.unsqueeze(dim=0)
        if self.device!="cpu":
            image_tmft = image_tmft.to(self.device)
            
        with torch.no_grad():
            output = self.model(image_tmft)
            output = torch.sigmoid(output)
        
        output = self._clean_output(output)
#         print(output.shape)
        output = output.squeeze()
        output = VF.to_pil_image(output)
        mask = VF.resize(output, size=(h,w))
        
        bbox_mask, croped_area = self.canvas_mask(image, mask)
        bbox_mask = PIL.Image.fromarray(bbox_mask)
        
#         plt.imshow(croped_area)
#         print('print croped_area => predict_canvas')
        
        combined = Image.new("RGBA", (w, h), mask_color)
        combined.paste(image, mask=mask)
        
        combined_bbox = Image.new("RGBA", (w, h), mask_color)
        combined_bbox.paste(image, mask=bbox_mask)
        
        
        return image, bbox_mask, mask, croped_area
        
        