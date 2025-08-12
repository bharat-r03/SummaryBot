from ollama import pull, generate
import math
from processing.file_preprocess import process_pdf
from .summarize_utils import chunk_input, get_file_ext


def summarize(input_text: str|list[str], model_name: str, target_word_ct: int, current_summary: str = None, context_length: int = 8192) -> str:
    summary_prompt = f"You are an assistant that is tasked with summarizing a set of documents that are given to you. The documents will be given in chunks. Write a summary using the information provided. Do not use bullet points or any other formatting. The summary should be between {target_word_ct-100} and {target_word_ct+100} words long. The text is as follows: "

    if current_summary:
        summary_prompt = f"You are an assistant that is tasked with summarizing a set of documents that are given to you. The documents will be given in chunks, and you will be given the current summary. Write a summary using the information provided. Do not use bullet points or any other formatting. The summary should be between {target_word_ct-100} and {target_word_ct+100} words long. The current summary is as follows: {current_summary}. The text is as follows: "

    if isinstance(input_text, str):
        summary_prompt += input_text
    elif isinstance(input_text, list) and all(isinstance(element, str) for element in input_text):
        full_input = "\n".join([chunk for chunk in input_text])
        summary_prompt += full_input
    else:
        raise TypeError("The input text does not align with the intended types of `str` or `list[str]`. Please verify that your input text is either a string or a list of strings.")

    summary_response = generate(
        model=model_name,
        prompt=summary_prompt,
        options={
            "num_ctx": context_length
        }
    )

    return summary_response["response"]


def create_chunked_summary(input_fpath: str, model_name: str) -> list[str]:
    file_ext = get_file_ext(input_fpath)
    if file_ext == "pdf":
        parsed_input = process_pdf(input_fpath)
    else:
        raise ValueError(f"Uploaded file type of `{file_ext}` is not supported for text parsing. Please try again without using any files with the specified file extension.")
    
    summary_input = chunk_input(parsed_input)
    chunk_summary = None

    if isinstance(summary_input, list) and len(summary_input) > 30:
        n_chunk_groups = math.ceil(len(summary_input) / 30)
        chunk_group_summary = None

        for chunk_group_idx in range(n_chunk_groups):
            chunk_group_start_idx, chunk_group_end_idx = chunk_group_idx * n_chunk_groups, (chunk_group_idx + 1) * n_chunk_groups
            chunk_group = summary_input[chunk_group_start_idx:chunk_group_end_idx]

            for chunk in chunk_group:
                chunk_summary = summarize(input_text=chunk, model_name=model_name, target_word_ct=200, current_summary=chunk_summary)
            
            chunk_group_summary = summarize(input_text=chunk_summary, model_name=model_name, target_word_ct=500, current_summary=chunk_group_summary)
            output_summary = chunk_group_summary

    elif isinstance(summary_input, list) and len(summary_input) <= 30:
        for chunk in summary_input:
            chunk_summary = summarize(input_text=chunk, model_name=model_name, target_word_ct=200, current_summary=chunk_summary)
        output_summary = chunk_summary

    return output_summary


def create_main_summary(chunked_summary: str|list[str], model_name: str, summary_type: str = "summary", target_word_ct: int = 500) -> str:
    if isinstance(chunked_summary, list):
        input_summary = "\n".join([summary for summary in chunked_summary])
    elif isinstance(chunked_summary, str):
        input_summary = chunked_summary

    if summary_type == "summary":
        main_summary = summarize(input_text=input_summary, model_name=model_name, target_word_ct=target_word_ct)
    # elif summary_type == "podcast":
    #     main_summary = podcastify(input_text=input_summaries, target_word_ct=target_word_ct)

    return main_summary