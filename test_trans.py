from googletrans import Translator

# 구글 번역기 객체 생성
translator = Translator()

# 번역할 텍스트
txt = '''이미 일어나 버린 일에 대해 뒤늦게 이유를 늘어놓아 봐야 사실은 아무것도 변하지 않는다. 그런데 사람들은 왜 동기다, 경위다, 이유다 하는 것을 요구하는 것일까.'''

# 텍스트 번역
res = translator.translate(txt, src='ko', dest='ko')

# 결과 출력
print(f"Original: {txt}")
print(f"Translated: {res.text}")