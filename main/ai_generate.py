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

tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
                                                           bos_token=BOS, eos_token=EOS, unk_token='<unk>',
                                                           pad_token=PAD, mask_token=MASK)


# model = torch.load('models/10000.pt', map_location=torch.device('cpu'))
model = GPT2LMHeadModel.from_pretrained('skt/kogpt2-base-v2')

# text = input('시작 문장 입력: ')

def generate_msg(text, length):
    input_ids = tokenizer.encode(text)
    gen_ids = model.generate(torch.tensor([input_ids]),
                             max_length=int(length),  # 키워드 입력 길이 제한
                             repetition_penalty=2.0,  # 단어가 반복됐을 때 새로운 단어가 생성되도록 만듬
                             pad_token_id=tokenizer.pad_token_id,
                             eos_token_id=tokenizer.eos_token_id,
                             bos_token_id=tokenizer.bos_token_id,
                             use_cache=True)
    generated = tokenizer.decode(gen_ids[0, :].tolist())
    generated = generated.replace("</s>", "")
    # . 으로 자르고 마지막 애매한 라인은 없애버리기


    a = generated.split('.')
    print(a)
    size = int(len(a)) -1

    result = ''
    for i in range(0, size):
        # print(a[i])
        result = result + a[i] + ".\n"
    return result