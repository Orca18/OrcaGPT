from typing import Optional
import torch
import transformers
from transformers import AutoModelWithLMHead, PreTrainedTokenizerFast
from fastai.text.all import *
import fastai
import re

import datetime as dt

now = dt.datetime.now()
nowDate = now.strftime('%m%d_%H%M')

tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
                                                    bos_token='</s>', eos_token='</s>', unk_token='<unk>',
                                                    pad_token='<pad>', mask_token='<mask>')
model = AutoModelWithLMHead.from_pretrained("skt/kogpt2-base-v2")

with open('nopebot_800min.txt', "r", encoding="utf-8") as f:
    lines = f.read()
lines = " ".join(lines.split())


class TransformersTokenizer(Transform):
    def __init__(self, tokenizer): self.tokenizer = tokenizer

    def encodes(self, x):
        toks = self.tokenizer.tokenize(x)
        return tensor(self.tokenizer.convert_tokens_to_ids(toks))

    def decodes(self, x): return TitledStr(self.tokenizer.decode(x.cpu().numpy()))


train = lines[:int(len(lines) * 0.9)]
test = lines[int(len(lines) * 0.9):]
splits = [[0], [1]]

# init dataloader 1
tls = TfmdLists([train, test], TransformersTokenizer(tokenizer), splits=splits, dl_type=LMDataLoader)
batch, seq_len = 32, 128
dls = tls.dataloaders(bs=batch, seq_len=seq_len)


# gpt2 ouput is tuple, we need just one val # 데이터 학습 시키기 약 30분
class DropOutput(Callback):
    def after_pred(self): self.learn.pred = self.pred[0]


learn = Learner(dls, model, loss_func=CrossEntropyLossFlat(), cbs=[DropOutput], metrics=Perplexity()).to_fp16()
lr = learn.lr_find()

learn.fine_tune(4)

# '폴더명/' 안에, '학습한 시간' + '_타입.pt' 로 저장
now = dt.datetime.now()
nowDate = now.strftime('%m%d_%H%M')
torch.save(model.state_dict(), './models/' + str(nowDate) + '_dict.pt')
torch.save(model, 'models/' + str(nowDate) + '_model.pt')
