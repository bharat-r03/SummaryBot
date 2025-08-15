from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, StreamingResponse, FileResponse
from summarize.summarize import create_chunked_summary, create_main_summary
from audio.audio import text_to_audio
import uuid
import os
import shutil
from typing import Annotated
import base64
import ollama


MODEL_DICT = {
    "Gemma 3 - 4B": "gemma3:4b",
    "Llama 3.2 - 3B": "llama3.2:3b"
}

VOICE_DICT = {
    "female": "af_heart",
    "male": "am_michael"
}


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:8080",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/generate-test")
async def generate_audio_test(files: list[UploadFile], voice: Annotated[str, Form()], summary_type: Annotated[str, Form()], model: Annotated[str, Form()]):
    sample_audio_path = "C:/Dev/SummaryBot/notebooks/audio_processing/test.wav"
    with open(sample_audio_path, "rb") as audio_file:
        summary_audio_bytes = audio_file.read()
    
    summary_audio_bytes = base64.b64encode(summary_audio_bytes).decode("utf-8")
    headers = {'Content-Disposition': 'attachment; filename="test.wav"'}
    return Response(summary_audio_bytes, headers=headers, media_type="audio/wav")


@app.post("/generate")
async def generate_audio(files: list[UploadFile], voice: Annotated[str, Form()], summary_type: Annotated[str, Form()], model: Annotated[str, Form()]):
    if not os.path.exists("tmpfiles"):
        os.mkdir("tmpfiles")

    model_name = MODEL_DICT[model]
    current_model_list = [model["model"] for model in ollama.list().models]
    if not model_name in current_model_list:
        ollama.pull(model_name)

    fpaths = []
    for file in files:
        fname = f"tmpfiles/tmp_file_{uuid.uuid4()}.pdf"
        with open(fname, "wb") as f:
            f.write(file.file.read())
        fpaths.append(fname)

    chunk_summaries = []

    for idx, fpath in enumerate(fpaths):
        print(f"Now processing file #{idx+1}!")
        file_summary = create_chunked_summary(fpath, model_name=model_name)
        chunk_summaries.append(file_summary)

    main_summary = create_main_summary(chunk_summaries, model_name=model_name, summary_type=summary_type.lower())
    summary_audio_bytes = text_to_audio(script_text=main_summary, speaker_voice=VOICE_DICT[voice.lower()])

    for fpath in fpaths:
        os.remove(fpath)
    if os.path.exists("tmpfiles"):
        shutil.rmtree("tmpfiles")

    summary_audio_bytes = base64.b64encode(summary_audio_bytes).decode("utf-8")
    headers = {'Content-Disposition': 'attachment; filename="test.wav"'}
    return Response(summary_audio_bytes, headers=headers, media_type="audio/wav")