from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from summarize.summarize import create_chunked_summary, create_main_summary
from audio.audio import text_to_audio
import uuid
import os
import shutil
from typing import Annotated
import base64


MODEL_NAME = "gemma3:4b"
SPEAKER_VOICE = "af_heart"

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/generate-test")
async def generate_audio_test(files: list[UploadFile], voice: Annotated[str, Form()], type: Annotated[str, Form()]):
    sample_audio_path = "C:/Dev/SummaryBot/notebooks/audio_processing/test.wav"
    with open(sample_audio_path, "rb") as audio_file:
        file = audio_file.read()
    
    return base64.b64encode(file)

@app.post("/generate")
async def generate_audio(files: list[UploadFile], voice: Annotated[str, Form()], type: Annotated[str, Form()]):
    if not os.path.exists("tmpfiles"):
        os.mkdir("tmpfiles")

    fpaths = []
    for file in files:
        fname = f"tmpfiles/tmp_file_{uuid.uuid4()}.pdf"
        with open(fname, "wb") as f:
            f.write(file.file.read())
        fpaths.append(fname)

    chunk_summaries = []

    for idx, fpath in enumerate(fpaths):
        print(f"Now processing file #{idx+1}!")
        file_summary = create_chunked_summary(fpath, model_name=MODEL_NAME)
        chunk_summaries.append(file_summary)

    main_summary = create_main_summary(chunk_summaries, model_name=MODEL_NAME)
    summary_audio_bytes = text_to_audio(script_text=main_summary, speaker_voice=SPEAKER_VOICE)

    for fpath in fpaths:
        os.remove(fpath)
    if os.path.exists("tmpfiles"):
        shutil.rmtree("tmpfiles")

    headers = {'Content-Disposition': 'attachment; filename="test.wav"'}
    return Response(summary_audio_bytes, headers=headers, media_type="audio/wav")