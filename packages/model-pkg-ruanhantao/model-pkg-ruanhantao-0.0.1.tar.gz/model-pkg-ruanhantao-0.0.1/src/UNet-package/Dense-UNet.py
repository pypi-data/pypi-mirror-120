'''
使用DenseBlock+Transition结构 
其中DenseBlock是包含很多层的模块，每个层的特征图大小相同，层与层之间采用密集连接方式。密集连接有利于特征重用，补偿分辨率损失。
而Transition模块用来连接两个相邻的DenseBlock，并且通过Pooling使特征图进行降维

Dense-UNet 论文里面也是用了4次的下采样和上采样。由于UNet在下采样过程中会导致分辨率下降，深层结构会防止丢失更多信息。
用DenseBlock替换了UNet中的ConvBlock，用Transition替换了UNet中的Pooling
'''
import torch
from torch.functional import block_diag
import torch.nn as nn
from torch.nn.modules import activation
from torch.nn.modules.dropout import Dropout 

class Dense_layer(nn.Module):
    '''
    densenet中说 dense block中每层输出的feature map也就是growth rate
    为了避免网络变得很宽，作者都是采用较小的k，比如32这样，作者的实验也表明小的k可以有更好的效果
    这里的1*1卷积主要是为了让网络变窄，降低计算量。1*1卷积的channel是growth rate*4
    '''
    def __init__(self,input_channels,output_channels=32,p=0.2):
        super(Dense_layer,self).__init__()
        self.bn1 = nn.BatchNorm2d(input_channels)   
        self.conv1 = nn.Conv2d(input_channels,output_channels*4,kernel_size=1,padding='same')  
        self.bn2 = nn.BatchNorm2d(output_channels*4)
        self.conv2 = nn.Conv2d(output_channels*4,output_channels,kernel_size=3,padding='same')
        self.activation = nn.ReLU(inplace=True)
        self.drop = nn.Dropout(p)
        pass
    def forward(self,x):
        x = self.bn1(x)
        x = self.conv1(x)
        x = self.activation(x)
        x = self.bn2(x)
        x = self.conv2(x)
        x = self.activation(x)
        x = self.drop(x)
        return x 

class DenseBlock(nn.Module):
    # 每一个DenseBlock由4个Dense_layer构成
    def __init__(self,input_channels,output_channels):
        super(DenseBlock,self).__init__()
        self.dense_layer1 = Dense_layer(input_channels,output_channels)
        self.dense_layer2 = Dense_layer(input_channels+output_channels,output_channels)
        self.dense_layer3 = Dense_layer(input_channels+2*output_channels,output_channels)
        self.dense_layer4 = Dense_layer(input_channels+3*output_channels,output_channels)
        

    def forward(self,x):
        x1 = self.dense_layer1(x)
        x2 = self.dense_layer2(torch.cat([x,x1],dim=1))
        x3 = self.dense_layer3(torch.cat([x,x1,x2],dim=1))
        x4 = self.dense_layer4(torch.cat([x,x1,x2,x3],dim=1))
        x5 = torch.cat([x,x1,x2,x3,x4],dim=1)
        return x5


class Transition(nn.Module):
    '''
    transition layer有个参数reduction（范围是0到1），表示将这些输出缩小到原来的多少倍，默认是0.5，这样传给下一个Dense Block的时候channel数量就会减少一半
    '''
    def __init__(self,input_channels,reduction=0.5):
        super(Transition,self).__init__()
        self.bn = nn.BatchNorm2d(input_channels)
        self.conv = nn.Conv2d(input_channels,int(input_channels*reduction),kernel_size=1,padding='same')
        self.maxpool = nn.MaxPool2d(kernel_size=2,stride=2) 

    def forward(self,x):
        x = self.bn(x)
        x = self.conv(x)
        x = self.maxpool(x)
        return x 
    



class DenseUNet(nn.Module):
    def __init__(self,input_channels,blocks,growth_rate,reduction=0.5):
        super(DenseUNet,self).__init__()
        self.input_channels = input_channels
        self.blocks = blocks
        self.growth_rate = growth_rate
        self.reduction = reduction
        
    def forward(self,x):
        lst = []
        input_dim_lst = []
        # 上采样
        input_dim = self.input_channels
        for i in range(self.blocks):
            dense_out = DenseBlock(input_dim,self.growth_rate)(x) # input_channels -> input_channels + 4 *  growth_rate
            lst.append(dense_out)
            input_dim = input_dim + 4*self.growth_rate
            input_dim_lst.append(input_dim)
            x = Transition(input_dim,self.reduction)(dense_out)
            input_dim = int(input_dim * self.reduction)
        # 中间层
        # out = DenseBlock(input_dim,self.growth_rate)(x)
        # 下采样
        for i in range(self.blocks):
            dense_out = DenseBlock(input_dim,self.growth_rate)(x)
            up_out = nn.ConvTranspose2d(input_dim + 4 * self.growth_rate ,input_dim_lst[self.blocks-i-1],kernel_size = 2, stride = 2, bias=True)(dense_out)
            x = torch.cat([up_out,lst[self.blocks-i-1]],dim=1)
            input_dim = 2 * input_dim_lst[self.blocks-i-1]
            #  = nn.ConvTranspose2d(in_channels,out_channels,kernel_size = 2, stride = 2, bias=True)
        out = DenseBlock(input_dim,self.growth_rate)(x)
        out = DenseBlock(input_dim + 4*self.growth_rate ,self.growth_rate)(out)
        out = nn.Conv2d( input_dim + 8 * self.growth_rate, self.input_channels, kernel_size=3, padding='same')(out)
        out = nn.ReLU(inplace=True)(out)
        return out 


if __name__=='__main__':
    model = DenseUNet(1,4,32)
    x = torch.rand([2,1,512,512])
    # print(x)
    out = model(x)
    print(out.shape)