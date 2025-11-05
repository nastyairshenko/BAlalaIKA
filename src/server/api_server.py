from fastapi import FastAPI
from pydantic import BaseModel
from ..tutor.virtual_tutor import VirtualTutor
from ..tutor.emotion_fusion import fuse

app, tutor = FastAPI(), VirtualTutor()

class Inp(BaseModel):
    input: str
    text_sentiment: float | None = None
    prosody_energy: float | None = None
    vlm_label: str | None = None

@app.post("/test/{client_id}/getAnswer")
async def get_answer(client_id: str, data: Inp):
    vad = fuse(data.text_sentiment, data.prosody_energy, data.vlm_label).tolist()
    reply = await tutor.reply(data.input, vad, meta={})
    return {"Reply": reply, "VAD": vad}
