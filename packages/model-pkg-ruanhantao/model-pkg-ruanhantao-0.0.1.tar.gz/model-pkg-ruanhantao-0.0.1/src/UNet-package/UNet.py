import torch 
import torch.nn as nn 
import torch.nn.functional as F

class double_conv2d_bn(nn.Module):
    def __init__(self,in_channels,out_channels,kernel_size=3,strides=1,padding='same'):
        super(double_conv2d_bn,self).__init__()
        self.conv1 = nn.Conv2d(in_channels,out_channels,
                               kernel_size=kernel_size,
                              stride = strides,padding=padding,bias=True)
        self.conv2 = nn.Conv2d(out_channels,out_channels,
                              kernel_size = kernel_size,
                              stride = strides,padding=padding,bias=True)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.bn2 = nn.BatchNorm2d(out_channels)
    
    def forward(self,x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = F.relu(self.bn2(self.conv2(out)))
        return out


class deconv2d_bn(nn.Module):
    def __init__(self,in_channels,out_channels,kernel_size=2,strides=2):
        super(deconv2d_bn,self).__init__()
        self.conv1 = nn.ConvTranspose2d(in_channels,out_channels,
                                        kernel_size = kernel_size,
                                       stride = strides,bias=True)
        self.bn1 = nn.BatchNorm2d(out_channels)
        
    def forward(self,x):
        out = F.relu(self.bn1(self.conv1(x)))
        return out

class Unet(nn.Module):
    '''
    input_channels 图片的channel，模型最终输出的channel同input_channel
    block 表示需要几次下采样/上采样
    n 表示基础的filter数量，每次采样都是原来的2倍或者0.5倍
    '''
    def __init__(self,input_channels,blocks,n):
        super(Unet,self).__init__()
        self.input_channels = input_channels
        self.blocks = blocks 
        self.n = n      
        self.sigmoid = nn.Sigmoid()
        
    def forward(self,x):
        skip_lst = []
        # 下采样
        for i in range(self.blocks):
            if i == 0:
                conv = double_conv2d_bn(self.input_channels,self.n)(x)
                pool = F.max_pool2d(conv,2)
                skip_lst.append(conv)
            else:
                conv = double_conv2d_bn(pow(2,i-1)*self.n,pow(2,i)*self.n)(pool)
                pool = F.max_pool2d(conv,2)
                skip_lst.append(conv)

        # 中间层 
        conv = double_conv2d_bn(pow(2,self.blocks-1)*self.n,pow(2,self.blocks)*self.n)(pool)

        # 上采样
        # skip_lst = skip_lst.reverse()
        items = list(range(self.blocks))
        items.reverse()
        for i in items:
            convt = deconv2d_bn(pow(2,i+1)*self.n,pow(2,i)*self.n)(conv)
            concat = torch.cat([convt,skip_lst[i]],dim=1)
            conv = double_conv2d_bn(pow(2,i+1)*self.n,pow(2,i)*self.n)(concat)


        outp = nn.Conv2d(self.n,self.input_channels,kernel_size=3,
                                     stride=1,padding='same',bias=True)(conv)
        outp = self.sigmoid(outp)

        return outp

