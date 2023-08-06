import sys
import torch
import torch.nn as nn
from torchvision.models import resnet
from ..modules import Attention, FeatureExtractor, BiLSTM
from ..modules.spatial import SpatialTransformer

from ..ops import net

class Encoder(nn.Module):
    def __init__(self, in_feat: int = 1, out_feat=512, nf: int = 20, im_size: tuple = (32, 100), device='cpu'):
        super(Encoder, self).__init__()
        self.device = device
        self.spatial_transformer = SpatialTransformer(nf=nf, img_size=im_size, imrec_size=im_size, img_channel=in_feat)
        self.feature_extractor = FeatureExtractor(in_channels=in_feat, out_channels=out_feat)
        self.out_channels = out_feat
        
        self._init_device()
        
    def _init_device(self):
        self.spatial_transformer = self.spatial_transformer.to(self.device)
        self.feature_extractor = self.feature_extractor.to(self.device)
        
    def freeze_spatial(self):
        net.freeze(self.spatial_transformer)

    def unfreeze_spatial(self):
        net.unfreeze(self.spatial_transformer)        
        
    def freeze_feature(self):
        net.freeze(self.feature_extractor)
        
    def unfreeze_feature(self):
        net.unfreeze(self.feature_extractor)
        
    def forward(self, x):
        x = self.spatial_transformer(x)
        x = self.feature_extractor(x)
        return x


class Decoder(nn.Module):
    def __init__(self, input_size: int, num_class: int, hidden_size: int = 256, device='cpu'):
        super(Decoder, self).__init__()
        self.device = device
        self.sequence = nn.Sequential(
            BiLSTM(input_size, hidden_size, hidden_size),
            BiLSTM(hidden_size, hidden_size, hidden_size)
        )
        self.prediction = Attention(hidden_size, hidden_size, num_class, )
        
        self._init_device()
        
    def _init_device(self):
        self.sequence = self.sequence.to(self.device)
        self.prediction = self.prediction.to(self.device)
        
    def freeze_sequence(self):
        net.freeze(self.sequence)
        
    def unfreeze_sequence(self):
        net.unfreeze(self.sequence)
            
    def freeze_prediction(self):
        net.freeze(self.prediction)
        
    def unfreeze_prediction(self):
        net.unfreeze(self.prediction)    

    def forward(self, feature: torch.Tensor, text=None, max_length=25):
        contextual_feature = self.sequence(feature)
        contextual_feature = contextual_feature.contiguous()
        prediction = self.prediction(contextual_feature, text, max_length=max_length)
        return prediction


class OCRNet(nn.Module):
    def __init__(self, num_class, in_feat: int = 1, out_feat=512, hidden_size: int = 256, 
                 nfid: int = 20, im_size: tuple = (32, 100), device='cpu'):
        super(OCRNet, self).__init__()
        self.device = device
        self.encoder = Encoder(in_feat=in_feat, out_feat=out_feat, nf=nfid, im_size=im_size, device=device)
        self.decoder = Decoder(input_size=out_feat, num_class=num_class, hidden_size=hidden_size, device=device)

    def forward(self, x: torch.Tensor, text=None, max_length=25):
        features = self.encoder(x)
        prediction = self.decoder(features, text, max_length)
        return prediction
    
    def freeze_encoder(self):
        net.freeze(self.encoder)
        
    def unfreeze_encoder(self):
        net.unfreeze(self.encoder)
        
    def freeze_decoder(self):
        net.freeze(self.decoder)
        
    def unfreeze_decoder(self):
        net.unfreeze(self.decoder)
    
    def read(self, x: torch.Tensor, converter, max_length=25):
        batch_size = x.size(0)
        used_device = x.get_device()
        if used_device == -1: used_device = 'cpu'
        texts_length = torch.IntTensor([max_length] * batch_size)
        texts_zeroes = torch.LongTensor(batch_size, max_length + 1).fill_(0)
        
        with torch.no_grad():
            features = self.encoder(x)
            prediction = self.decoder(features, texts_zeroes, max_length=max_length)
            _, prediction_index = prediction.max(2)
            prediction_string = converter.decode(prediction_index, texts_length)
        
        return prediction_string, prediction_index
            


if __name__ == "__main__":
    # enc = Encoder()aqa
    test_data = torch.rand(3, 1, 224, 224)
    # out = enc(test_data)
    # print(out)

    num_class = 96
    im_size = (32, 100)
    model = OCRNet(num_class=num_class, im_size=im_size)
