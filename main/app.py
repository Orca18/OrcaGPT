import os
from flask import Flask, request, jsonify
import ai_chat
import ai_generate


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def hello():
    return "김동현의 챗봇 api"


### http://192.168.0.29:5000/chatbot/q?s=안녕하세요
@app.route('/chatbot/q')
def reactChatbotV1():
    sentence = request.args.get("s")
    if sentence is None or len(sentence) == 0 or sentence == '\n':
        # return jsonify({
        #     "answer": "말씀해주세요~"
        # })
        return "말씀해주세요~"

    answer = ai_chat.generate_msg(sentence)
    print("보내준 answer="+answer)
    return answer
    # return jsonify({
    #     "answer": answer
    # })

### http://192.168.0.29:5000/generate/q?s=테스트
@app.route('/generate/q')
def reactChatbotV2():
    sentence = request.args.get("s")
    length = request.args.get("l")

    print("length:"+length)
    try:
        answer = ai_generate.generate_msg(sentence, length)
        return answer
    except :
        return "s(문장) 문자,,, l(최대 길이)은 숫자만 입력해주세요"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
