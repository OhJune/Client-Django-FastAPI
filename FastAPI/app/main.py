from fastapi import FastAPI
from gensim.models import Word2Vec
from pydantic import BaseModel
import logging
import json
from typing import List
from databases import Database
import os
import openai
import re
## 만들 함수 

app = FastAPI()
logging.basicConfig(level=logging.INFO)
loaded_word2vec_model = Word2Vec.load('song2vec.model')


@app.get("/")
async def root():
    return {"message": "Hello World"}


class InputData(BaseModel):
    input_data: List[str]
# 1. DB 접근 (DTO) 
# 데이터베이스 연결 URL 설정

fast_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
secrets_path = os.path.join(fast_dir,"secrets.json")

with open(secrets_path, 'r') as f:
    secrets = json.load(f)
DATABASE_URL = secrets["DATABASE_URL"]

# gpt api
openai.organization = secrets["openai.organization"]
openai.api_key = secrets["openai.api_key"]
# 기본 데이터베이스 객체 생성
database = Database(DATABASE_URL)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    
# @app.get("/test_db_connection")
# async def test_db_connection():
#     # 데이터가 있는지 확인하려면 실제 테이블 이름으로 교체하세요.
#     query = 'SELECT song_song.tj_song_num_id,song_song.ky_song_num_id,song_song.title,song_song.artist FROM song_song WHERE master_number = 21'
    
#     try:
#         result = await database.fetch_one(query)
        
#         if result is not None:
#             return {"status": "success", "data": result}
#         else:
#             return {"status": "success", "data": "No rows found"}
#     except Exception as e:
#         return {"status": "error", "details": str(e)}

def record_to_dict(record):
    return {
        "tj_song_num_id": record["tj_song_num_id"],
        "ky_song_num_id": record["ky_song_num_id"],
        "title": record["title"],
        "artist": record["artist"]
    }
    
@app.post("/process")
async def process_data(input_data:  InputData):
    logging.info(f"Received data: {input_data}")
    print(f"Received data: {input_data.input_data}")
    print(f"Received data type: {type(input_data)}")
    
    filtered_input_data = [word for word in input_data.input_data if word in loaded_word2vec_model.wv]

    if len(filtered_input_data) == 0:
        result_list = []
        for i in input_data.input_data:
            query = f'SELECT song_song.tj_song_num_id,song_song.ky_song_num_id,song_song.title,song_song.artist FROM song_song WHERE master_number = {int(i)};' 
            rows = await database.fetch_all(query=query)
            logging.info(f"comfirm: {rows}")
            
            for row in rows:
                song_title = row["title"]
                artist = row["artist"]

                result_list.append(f"{song_title}-{artist}")
        print(result_list)
        prompt = f"내 플레이리스트는 {result_list}이고, 내 플레이리스트 기반으로 부를 노래를 노래방에 있는 노래.가수 형식 10곡 추천해줘"

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=1024,
            n=1,
            stop=None,
        )

        # print(response.choices[0].text.strip())
        song_info = response.choices[0].text.strip().split('\n')
        print(song_info)

            
        collected_rows = []
        
        for song in song_info:
            song = re.sub(r'\d+\.','', song)
            title,_=song.split('-')
            title = title.replace(" ","").strip()
            print(title)

            try:
                query = f"SELECT song_song.tj_song_num_id,song_song.ky_song_num_id,song_song.title,song_song.artist FROM song_song WHERE song_song.title = '{title}' LIMIT 1;"
                data = await database.fetch_one(query=query)

                collected_rows.append(data)
            
            except Exception as error:
                print(f"Error for title '{i}': {error}")
                continue
        
        # 여기에 모델 고도화 작업 ex) chatGPTapi,코사인유사도 뻥튀기 
        print("필터링된 데이터가 없어 chat gpt가 응답합니다.")
        return {"result": collected_rows}
    
    else:
        similar_songs = loaded_word2vec_model.wv.most_similar(positive=filtered_input_data, topn=10)
        result = [i[0] for i in similar_songs]
        print(result)
        
    # 결과를 수집할 빈 리스트 생성
    collected_rows = []

    for i in result:
        query = f'SELECT song_song.tj_song_num_id,song_song.ky_song_num_id,song_song.title,song_song.artist FROM song_song WHERE master_number = {int(i)};' 
        rows = await database.fetch_all(query=query) # 변경된 부분
        print(rows)
        
        # 결과를 collected_rows 리스트에 추가
        collected_rows.extend(rows)

    return {"result": collected_rows}



