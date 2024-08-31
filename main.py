from openai import OpenAI
from trafilatura import fetch_url, extract
from fastapi import FastAPI, status
from pydantic import BaseModel
import os

# clase con el modelo para request
class RequestModel(BaseModel):
    url: str

app = FastAPI()
@app.get("/")
def main(url: str):
    downlad =  fetch_url(url)
    texto = extract(downlad, with_metadata=True)

    client = OpenAI(
        api_key=os.environ['SAIMON_API_KEY'],  
        base_url="https://saimon.ca/ollama/v1"
    )

    completion = client.chat.completions.create(
        model="llama3.1:latest",
        messages=[
            {"role": "system", "content": "You are a teacher reading news to 10 year old kids."},
            {"role": "user", "content": f"Necesito un resumen de las noticias de todo este texto de modo informal explicado para un niño y omitiendo temas de adultos sobre este texto: {texto}"}
        ]
    )

    return completion.choices[0].message.content