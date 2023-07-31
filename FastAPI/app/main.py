from fastapi import FastAPI
from gensim.models import Word2Vec
from pydantic import BaseModel
import logging
import json
from typing import List
from databases import Database
import os
## 만들 함수 

app = FastAPI()
loaded_word2vec_model = Word2Vec.load('song2vec.model')

@app.get("/")
async def root():
    return {"message": "Hello World"}


class InputData(BaseModel):
    input_data: List[str]
# 1. DB 접근 (DTO) 
# 데이터베이스 연결 URL 설정

with open("secrets.json", 'r') as f:
    secrets = json.load(f)
DATABASE_URL = secrets["DATABASE_URL"]

# 기본 데이터베이스 객체 생성
database = Database(DATABASE_URL)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    
@app.get("/test_db_connection")
async def test_db_connection():
    # 데이터가 있는지 확인하려면 실제 테이블 이름으로 교체하세요.
    query = 'SELECT master."곡번호_TJ",master.ky_song_num_id,master.title,master.artist FROM master WHERE master_number = 21'
    
    try:
        result = await database.fetch_one(query)
        
        if result is not None:
            return {"status": "success", "data": result}
        else:
            return {"status": "success", "data": "No rows found"}
    except Exception as e:
        return {"status": "error", "details": str(e)}

# 2. post 요청 유저아이디 확인
# 3. 모델에 넣고 리스트 추출 -> sing_list
# 4. DB에서 조회하기
# 5. entry 포인트

@app.post("/process")
async def process_data(input_data:  InputData):
    logging.info(f"Received data: {input_data}")
    print(f"Received data: {input_data.input_data}")
    filtered_input_data = [word for word in input_data.input_data if word in loaded_word2vec_model.wv]

    if len(filtered_input_data) == 0:
        # 여기에 모델 고도화 작업 ex) chatGPTapi,코사인유사도 뻥튀기 
        print("필터링된 데이터가 없어 모델이 실행되지 않습니다.")
    else:
        similar_songs = loaded_word2vec_model.wv.most_similar(positive=filtered_input_data, topn=10)
        result = [i[0] for i in similar_songs]
        print(result)
        
    # 결과를 수집할 빈 리스트 생성
    collected_rows = []

    for i in result:
        query = f'SELECT master."곡번호_TJ",master.ky_song_num_id,master.title,master.artist FROM master WHERE master_number = {int(i)};' 
        rows = await database.fetch_all(query=query) # 변경된 부분
        print(rows)
        
        # 결과를 collected_rows 리스트에 추가
        collected_rows.extend(rows)

    return {"result": collected_rows}



