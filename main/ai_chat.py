from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel
import torch

# 트레이닝 해둔 모델과 대화
Q_TKN = "<usr>"
A_TKN = "<sys>"
BOS = '</s>'
EOS = '</s>'
MASK = '<unused0>'
SENT = '<unused1>'
PAD = '<pad>'

tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2", bos_token=BOS, eos_token=EOS,
                                                    unk_token='<unk>', pad_token=PAD, mask_token=MASK)

model = torch.load('C:/Users/luke0/Flask-Simple-Chat/src/app/models/10000.pt', map_location=torch.device('cpu'))

sent = "0"
def generate_msg(q):
    a = ""
    while 1:
        while 1:
            input_ids = tokenizer.encode(Q_TKN + q + SENT + sent + A_TKN + a)
            input_ids = torch.LongTensor(input_ids).unsqueeze(dim=0)
            pred = model(input_ids)
            pred = pred.logits
            gen = tokenizer.convert_ids_to_tokens(torch.argmax(pred, dim=-1).squeeze().numpy().tolist())[-1]
            if gen == EOS:
                ### 직전 생성한 문장하고, 추가된 문장하고 뭐가 다른지 확인함
                break
            a += gen.replace("▁", " ")
            # print(a)
            output_msg = "{}".format(a.strip())
            # print(output_msg)
        return output_msg




