from summarize.summarize import create_chunked_summary, create_main_summary
from audio.audio import text_to_audio
import soundfile as sf
import datetime
import os


MODEL_NAME = "gemma3:4b"
SPEAKER_VOICE = "af_heart"


if __name__ == "__main__":
    files = []

    n_files_to_upload = input("How many files would you like to upload? ")
    try:
        n_files_to_upload = int(n_files_to_upload)
    except Exception as e:
        raise ValueError("Please ensure that you input a number corresponding to the number of files that you'd like to enter.")

    for input_file_idx in range(n_files_to_upload):
        files.append(input(f"Please input a file path for input file {input_file_idx+1}: "))

    chunk_summaries = []
    for file in files:
        file_summary = create_chunked_summary(file, model_name=MODEL_NAME)
        chunk_summaries.append(file_summary)

    main_summary = create_main_summary(chunk_summaries, model_name=MODEL_NAME)
    summary_audio = text_to_audio(script_text=main_summary, speaker_voice=SPEAKER_VOICE)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S")
    sf.write(f"outputs/summary_{timestamp}.wav", summary_audio, samplerate=24000)
    print("Audio file successfully processed to file!")