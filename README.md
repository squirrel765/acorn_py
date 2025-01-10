# 도토리_파이썬 프로젝트 
![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=squirrel765&layout=compact)  
<img alt="Python" src ="https://img.shields.io/badge/Python-3776AB.svg?&style=for-the-badge&logo=Python&logoColor=white"/>

## 2025.01.09
**semu_helper, semu_helper2를 추가하였습니다.**  
semu_helper2는 부가가치 계산에 있어 표 기능을 파이썬 GUI로 세심하게 구현해보고자 하였으나, 아직 미완성 단계입니다.  
semu_helper는 기본적으로 부가가치세 신고 도우미가 편하게 직관적으로 사용할수 있게 설계되었습니다.  
  
<img width="791" alt="스크린샷 2025-01-09 오전 9 20 52" src="https://github.com/user-attachments/assets/b9c7f6fc-7a4f-4838-9892-00810102c483" />
  
## 보완할 부분 
1. 코드의 길이 줄이기
2. UI 다듬기
## 계획
1. 표 기능 수정
2. 실제 사용해보기


***
  
**test_trans 파일을 추가하였습니다.**
간단하게 번역을 돌려볼수 있는 코드입니다. 
```
# 번역할 텍스트
txt = '''이미 일어나 버린 일에 대해 뒤늦게 이유를 늘어놓아 봐야 사실은 아무것도 변하지 않는다. 그런데 사람들은 왜 동기다, 경위다, 이유다 하는 것을 요구하는 것일까.'''
# 텍스트 번역
res = translator.translate(txt, src='ko', dest='en')  # 예시는 ko(한국어)를 en(영어)로 번역합니다.

# 결과 출력
print(f"Original: {txt}")
print(f"Translated: {res.text}")
```

## 보완할 부분
1. 방대한 양을 넣으면 번역이 안되는 문제
## 계획
1. csv파일의 특정 열을 번역시 중복되는 부분을 찾아서 set()를 이용해 묶은 후 번역진행
