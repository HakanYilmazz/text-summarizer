from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()  # load HF_API_KEY

app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL = "facebook/bart-large-cnn"

class SummarizeRequest(BaseModel):
    text: str
    use_key: bool

@app.post("/summarize")
def summarize(req: SummarizeRequest):
    if not req.use_key:
        return {"summary": "API key disabled. Switch ON to generate."}

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{HF_MODEL}",
        headers={"Authorization": f"Bearer {HF_API_KEY}"},
        json={"inputs": req.text}
    )

    data = response.json()
    summary_text = data[0].get("summary_text", "") if isinstance(data, list) else "No summary available"
    return {"summary": summary_text}