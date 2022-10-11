import os
import sys
import urllib.request
import json
from pprint import pprint

### 과정: 임포트 - 클라이언트 정보 - 번역할 문장 - 번역 def - 번역 테스트 - 번역 돌리기 (한줄씩)

# 바탕화면에 저장된 메모장에서 client id, pw 가져오기
# labels에 id, pw가 리스트 형태로 저장
file_path = 'papago_client.txt'
labels = open(file_path).read().splitlines()

client_id = labels[0]  # 개발자센터에서 발급받은 Client ID 값
client_secret = labels[1]  # 개발자센터에서 발급받은 Client Secret 값

file_path = 'nopebot_800min_edit.txt' # 번역할 문장
labels = open(file_path).read().splitlines() # 한줄한줄 나눔


def ToEn(koText):
    encText = urllib.parse.quote(koText)
    data = "source=ko&target=en&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    transed = ''
    if (rescode == 200):
        response_body = response.read()
        result = response_body.decode('utf-8')
        d = json.loads(result)
        transed = d['message']['result']['translatedText']

    else:
        transed = 'fail'
        print(transed)
        # print("Error Code:" + rescode)

    return transed

test = ToEn('안녕하세요')
print(test)

now_line = 0  # 읽고 있는 문장 라인 번호 (전체 번호)
in_line = 0  # while in_line < n 번씩 끊어 읽을 때... (내부 끊어서 보는 번호)

while now_line < len(labels):  # 리스트 수 만큼 읽음
    in_line = 0  # 내부 라인 초기화
    # a => 더하는 모드 / w => 생편집
    f = open("toEN_translated.txt", 'a')  # 다시 열어주기
print("==================================================")
while in_line < 5:
    if (len(labels) > now_line):  # 0-1. 파일 라인 내
        a = labels[now_line]  # now_line번째 줄 문장
        print(a)
        if (a != ""):  # 1-1. 공백이 아니면 번역한다
            en = ToEn(a)
            if (en == "fail"):  # 2-1. 실패면 저장 안한다.
                print("fail")
                print("in_line/now_line" + str(in_line) + "/" + str(now_line))
            else:  # 2-2. 번역 성공하면, 입력한다.
                f.write(en + '\n')
    else:  # 1-2. 공백이면 공백 출력
        print("공백")

    print('line_num = ' + str(in_line))
    print('cycle = ' + str(now_line))

else:  # 0-2. 파일 라인 도달
    print('추가 안함')

# 계속 추가해주기
in_line = in_line + 1
now_line = now_line + 1
# in_line < n 번 해줬으면, 닫아주기
f.close()

