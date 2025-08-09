from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse, Response
from summarize.summarize import create_chunked_summary, create_main_summary
from audio.audio import text_to_audio
import soundfile as sf
import uuid
import os


MODEL_NAME = "gemma3:4b"
SPEAKER_VOICE = "af_heart"

app = FastAPI()


@app.post("/test/")
async def generate_audio(files: list[UploadFile]):
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

    headers = {'Content-Disposition': f'attachment; filename="test.wav"'}
    return Response(summary_audio_bytes, headers=headers, media_type="audio/wav")


@app.get("/")
async def main():
    content = """
        <body>
        <form action="/test/" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple>
        <input type="submit">
        </form>
        </body>
    """
    return HTMLResponse(content=content)