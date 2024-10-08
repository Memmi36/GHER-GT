import torch
import torch.nn as nn   
from torch.autograd import Variable
from torch import Tensor
import math
import torch.nn.functional as F

def feed_forward(dim_input: int = 128, dim_feedforward: int = 512) -> nn.Module:
    return nn.Sequential(
        nn.Linear(dim_input, dim_feedforward,dtype=torch.float),
        nn.Mish(),
        nn.Linear(dim_feedforward, dim_input,dtype=torch.float),
    )
    
class Residual(nn.Module):
    def __init__(self, sublayer: nn.Module, dimension: int, stride: int = 1, dropout: float = 0.1):
        super().__init__()
        self.sublayer = sublayer
        self.norm = nn.LayerNorm(dimension, dtype=torch.float)
        self.dropout = nn.Dropout(dropout)
        self.stride = stride

    def forward(self, *tensors: Tensor) -> Tensor:
        # Assume that the "query" tensor is given first, so we can compute the
        # residual.  This matches the signature of 'MultiHeadAttention'.
        x = self.dropout(self.sublayer(*tensors))
        
        # Adjust the residual connection based on the stride
        if self.stride > 1:
            residual = tensors[0][:, ::self.stride, :, :]
        else:
            residual = tensors[0]
        
        x = residual + x
        x = self.norm(x)
        return x

class AttentionHead(nn.Module):
    def __init__(self, dim_in: int, dim_v: int, dim_k: int, strides :int =1,kernel_size: int = 1 ):
        super().__init__()
        self.strides = strides
        self.d_k=dim_k
        self.d_v=dim_v
        self.q_conv=nn.Conv2d(
                dim_in,
                dim_k,
                kernel_size=(kernel_size, 1),
                padding=(int((kernel_size - 1) / 2), 0),
                stride=(1, self.strides),dtype=torch.float)
        self.k_conv=nn.Conv2d(
                dim_in,
                dim_k,
                kernel_size=(kernel_size, 1),
                padding=(int((kernel_size - 1) / 2), 0),
                stride=(1, self.strides),dtype=torch.float)
        self.v_conv=nn.Conv2d(
                dim_in,
                dim_v,
                kernel_size=(kernel_size, 1),
                padding=(int((kernel_size - 1) / 2), 0),
                stride=(1, self.strides),dtype=torch.float)

    def attention(self,Q,K,V):
        sqrt_dk=torch.sqrt(torch.tensor(self.d_k))
        attention_weights = F.softmax((Q @ K.transpose(-2,-1))/sqrt_dk, dim=-1)
        attention_vectors=attention_weights @ V


        return attention_vectors            
    def forward(self, x: Tensor) -> Tensor:
        batch_size = x.size(0)
        seq_length = x.size(1)
        graph_size=x.size(2)
        x=x.permute(0,3,2,1)
        # x=x.transpose(1,2)
        #Q, K, V=torch.split(self.qkv_conv(x), [self.d_k , self.d_k, self.d_v],
        #                            dim=1)
        Q=self.q_conv(x).permute(0,3,2,1)
        K=self.k_conv(x).permute(0,3,2,1)
        V=self.v_conv(x).permute(0,3,2,1)


        x=self.attention(Q,K,V).transpose(1,2).contiguous().view(batch_size,seq_length//self.strides,graph_size, self.d_k)
        return x

class MultiHeadAttention(nn.Module):
    def __init__(self, num_heads: int, dim_in: int,dim_k,dim_q,dim_v, stride):
        super().__init__()
        self.stride = stride
        self.heads = nn.ModuleList(
            [AttentionHead(dim_in, dim_v, dim_k,self.stride) for _ in range(num_heads)]
        )
        self.linear = nn.Linear(num_heads * dim_k, dim_in,dtype=torch.float)

    def forward(self, x) -> Tensor:
        outs=[]
        for h in self.heads:
            outs.append(h(x))
        outs=torch.cat(outs, dim=-1)
        outs=self.linear(
            outs
        )

        return outs

class GraphtransformerLayer(nn.Module):
    def __init__(
        self,
        dim_model,
        num_heads,
        dim_feedforward,
        dropout: float ,
        stride: int = 1,
    ):
        super().__init__()
        self.stride = stride
        dim_v=dim_q = dim_k = max(dim_model // num_heads, 1)
        self.attention = Residual(
            MultiHeadAttention(num_heads, dim_model,16,16,16, self.stride),
            dimension=dim_model,
            stride=self.stride,
            dropout=dropout,
        )
        self.feed_forward = Residual(
            feed_forward(dim_model, dim_feedforward),
            dimension=dim_model,
            dropout=dropout,
        )
        self.norm = nn.LayerNorm(dim_model,dtype=torch.float)
    def forward(self, src: Tensor) -> Tensor:

        src = self.attention(self.norm(src))

        return self.feed_forward(src)

class PositionalEncoder(nn.Module):
    def __init__(self, d_model, max_seq_len = 64):
        super().__init__()
        self.d_model = d_model
        
        # create constant 'pe' matrix with values dependant on z
        # pos and i
        pe = torch.zeros(max_seq_len,22 , d_model)
        for pos in range(max_seq_len):
          for node_id in range(0,22) :
            for i in range(0, d_model, 2):
                pe[pos, node_id, i] = \
                math.sin(pos / (10000 ** ((2 * i)/d_model)))
                pe[pos, node_id, i + 1] = \
                math.cos(pos / (10000 ** ((2 * (i + 1))/d_model)))
                
        pe = pe.unsqueeze(0)
        #self.learnable_pe=nn.Linear(d_model, d_model,dtype=torch.float)
        self.norm=nn.LayerNorm(d_model,dtype=torch.float)
        self.register_buffer('pe', pe)

    
    def forward(self, x):
        # make embeddings relatively larger
        # x = x * math.sqrt(self.d_model)
        #add constant to embedding
        seq_len = x.size(1)
        device = x.device  # Get the device of the input tensor
        x = x.to(device)
        pe = self.pe[:, :seq_len, :, :].to(device)  # Move positional encoding to the same device
        x = self.norm(x + Variable(pe, requires_grad=False))
        
        return x

class GraphTransformer(nn.Module):
    def __init__(
        self,
        stride,
        num_layers,
        dim_model,
        num_heads,
        dim_feedforward,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.stride = stride
        self.layers = nn.ModuleList(
            [
            GraphtransformerLayer(dim_model, num_heads, dim_feedforward, dropout, self.stride)      
            for _ in range(num_layers)
            ]
        )
        self.positional_encoder=PositionalEncoder(dim_model)
    def forward(self, x: Tensor) -> Tensor:
        N,C,T,V=x.shape
        x=x.permute(0,2,3,1)      
        x += self.positional_encoder(x)
        for layer in self.layers:
            x = layer(x)

        return x