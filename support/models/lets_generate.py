import torch
from transformers import AutoModelWithLMHead, PreTrainedTokenizerFast
from fastai.text.all import *

# kogpt2 불러오기 및 데이터 훈련 전 테스트
tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
                                                    bos_token='</s>', eos_token='</s>', unk_token='<unk>',
                                                    pad_token='<pad>', mask_token='<mask>')

# model = AutoModelWithLMHead.from_pretrained("skt/kogpt2-base-v2")
model = torch.load('모델명.pt', map_location=torch.device('cpu'))

text = input("앞 문장: ")
input_ids = tokenizer.encode(text)
gen_ids = model.generate(torch.tensor([input_ids]),
                         max_length=40,
                         repetition_penalty=2.0,
                         pad_token_id=tokenizer.pad_token_id,
                         eos_token_id=tokenizer.eos_token_id,
                         bos_token_id=tokenizer.bos_token_id,
                         use_cache=True
                         )
generated = tokenizer.decode(gen_ids[0, :].tolist())
print(generated)
