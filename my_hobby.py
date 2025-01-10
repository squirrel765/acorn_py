import re
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from googletrans import Translator

# 웹 페이지를 가져오는 함수
def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    else:
        print("웹 페이지를 가져오는 데 실패했습니다.")
        return None

# 웹 페이지에서 텍스트를 추출하는 함수
def extract_text(soup):
    paragraphs = soup.find_all('p')  # 모든 <p> 태그 추출
    text = ' '.join([para.get_text() for para in paragraphs])
    return text

# 텍스트 정리 함수
def clean_text(text):
    # 알파벳, 숫자, 공백, 기본 구두점만 남기고 나머지 문자 제거
    text = re.sub(r'[^\w\s.,!?\'"-]', '', text)
    # 여러 개의 공백을 하나로 줄여줌
    text = ' '.join(text.split())
    return text

# 텍스트에서 해시태그 추출 함수
def extract_hashtags(text):
    hashtags = [word for word in text.split() if word.startswith("#")]
    return hashtags

# 텍스트 요약 함수
def summarize_text(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    # 텍스트 정리 후 요약
    cleaned_text = clean_text(text)
    
    # 텍스트를 1000자씩 나눠서 요약
    chunk_size = 1000
    text_chunks = [cleaned_text[i:i+chunk_size] for i in range(0, len(cleaned_text), chunk_size)]
    summary = ""
    
    for chunk in text_chunks:
        part_summary = summarizer(chunk, max_length=150, min_length=50, do_sample=False)
        summary += part_summary[0]['summary_text'] + " "
    
    return summary.strip()

# 메인 함수
def main(url):
    # 1. 웹 크롤링
    soup = fetch_page(url)
    if soup:
        # 2. 텍스트 추출
        text = extract_text(soup)
        
        # 3. 텍스트 요약
        summary = summarize_text(text)
        
        # 4. 해시태그 추출
        hashtags = extract_hashtags(text)
        
        # 5. 요약된 텍스트 출력
        print("원본 텍스트:", text[:1000])  # 처음 1000자 출력
        print("요약:", summary)
        print("발견된 해시태그:", hashtags)

        # 결과를 파일로 저장
        with open("output.txt", "w", encoding="utf-8") as file:
            file.write(f"원본 텍스트: {text}\n")
            file.write(f"요약: {summary}\n")
            file.write(f"발견된 해시태그: {', '.join(hashtags)}\n")
            
        # 6. 영어로 요약된 텍스트 번역
        # 구글 번역기 객체 생성
        translator = Translator()

        # 영어 요약 텍스트 번역 (영어 -> 한국어)
        res = translator.translate(summary, src='en', dest='ko')

        # 번역된 결과 출력
        print(f"원본 요약 (영어): {summary}")
        print(f"번역된 요약 (한국어): {res.text}")

# 예시 URL
url = 'https://edition.cnn.com/2024/12/03/asia/south-korea-martial-law-explainer-intl-hnk/index.html?iid=cnn_buildContentRecirc_end_recirc' # 원하는 웹사이트 URL 입력

if __name__ == '__main__':
    main(url)
