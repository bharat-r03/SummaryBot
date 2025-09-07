from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, StreamingResponse
from summarize.summarize import create_chunked_summaries, create_main_summary
from audio.audio import text_to_audio
import uuid
import os
import shutil
from typing import Annotated
import base64
import ollama
import asyncio


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


stage_dict = {"stage": ""}

async def set_stage(stage: str):
    stage_dict["stage"] = stage
    await asyncio.sleep(0.5)


async def update_stage():
    while True:
        status = stage_dict["stage"]
        yield f"event: stageUpdate\ndata: {status}\n\n"
        await asyncio.sleep(1)


@app.get("/stream")
async def stream_stage():
    return StreamingResponse(update_stage(), media_type="text/event-stream")


@app.post("/generate-test")
async def generate_audio_test(files: list[UploadFile], voice: Annotated[str, Form()], summary_type: Annotated[str, Form()], model: Annotated[str, Form()]):
    sample_audio_path = "C:/Dev/SummaryBot/notebooks/audio_processing/test.wav"
    with open(sample_audio_path, "rb") as audio_file:
        summary_audio_bytes = audio_file.read()

    summary_audio_bytes = base64.b64encode(summary_audio_bytes).decode("utf-8")
    headers = {'Content-Disposition': 'attachment; filename="test.wav"'}
    await set_stage("processing_complete")
    return Response(summary_audio_bytes, headers=headers, media_type="audio/wav")


@app.post("/generate")
async def generate_audio(files: list[UploadFile], voice: Annotated[str, Form()], summary_type: Annotated[str, Form()], model: Annotated[str, Form()]):
    if not os.path.exists("tmpfiles"):
        os.mkdir("tmpfiles")

    model_name = MODEL_DICT[model]
    current_model_list = [model["model"] for model in ollama.list().models]
    if not model_name in current_model_list:
        ollama.pull(model_name)
    await set_stage("load_model")

    fpaths = []
    for file in files:
        fname = f"tmpfiles/tmp_file_{uuid.uuid4()}.pdf"
        with open(fname, "wb") as f:
            f.write(file.file.read())
        fpaths.append(fname)
    await set_stage("process_files")
    

    chunk_summaries = []

    for idx, fpath in enumerate(fpaths):
        print(f"Now processing file #{idx+1}!")
        doc_summary_list = create_chunked_summaries(fpath, model_name=model_name)
        chunk_summaries.append(doc_summary_list)
    await set_stage("summarize_files")

    main_summary = create_main_summary(chunk_summaries, model_name=model_name, summary_type=summary_type.lower())
    await set_stage("summarize_main")

    summary_audio_bytes = text_to_audio(script_text=main_summary, speaker_voice=VOICE_DICT[voice.lower()])
    await set_stage("text_to_audio")

    for fpath in fpaths:
        os.remove(fpath)
    if os.path.exists("tmpfiles"):
        shutil.rmtree("tmpfiles")

    summary_audio_bytes = base64.b64encode(summary_audio_bytes).decode("utf-8")
    headers = {'Content-Disposition': 'attachment; filename="test.wav"'}
    await set_stage("processing_complete")
    return Response(summary_audio_bytes, headers=headers, media_type="audio/wav")