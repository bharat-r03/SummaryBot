from ollama import generate
import math
from processing.file_preprocess import process_pdf
from .summarize_utils import chunk_input, get_file_ext, group_indices


def summarize_chunks(input_text: str|list[str], model_name: str, target_word_ct: int, temperature: float, context_length: int = 8192) -> str:
    summary_prompt = f"You are an assistant that is tasked with summarizing a set of documents that are given to you. The documents will be given in chunks. Write a summary using the information provided. Do not use bullet points or any other formatting. The summary should be between {target_word_ct-100} and {target_word_ct+100} words long. The text is as follows: "

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
            "num_ctx": context_length,
            "temperature": temperature
        }
    )

    return summary_response["response"]


def summarize_final(input_summaries: list[str], model_name: str, target_word_ct: int, temperature: float, context_length: int = 8192) -> str:
    summary_prompt = f"You are an assistant that is tasked with summarizing a set of documents that are given to you. Write a summary using the information provided. Ensure that you treat each document as separate and summarize them individually, not together. Do not use bullet points or any other formatting. The summary should be between {target_word_ct-100} and {target_word_ct+100} words long."

    if isinstance(input_summaries, list) and all(isinstance(element, str) for element in input_summaries):
        for idx, summary in enumerate(input_summaries):
            summary_prompt += f"Text {idx} is as follows: {summary}."
    else:
        raise TypeError("The input text does not align with the intended types of `str` or `list[str]`. Please verify that your input text is either a string or a list of strings.")

    print(len(summary_prompt))

    summary_response = generate(
        model=model_name,
        prompt=summary_prompt,
        options={
            "num_ctx": context_length,
            "temperature": temperature
        }
    )

    return summary_response["response"]

def create_chunked_summaries(input_fpath: str, model_name: str) -> list[str]:
    file_ext = get_file_ext(input_fpath)
    if file_ext == "pdf":
        processed_input = process_pdf(input_fpath)
    else:
        raise ValueError(f"Uploaded file type of `{file_ext}` is not supported for text parsing. Please try again without using any files with the specified file extension.")
    
    chunked_input = chunk_input(processed_input)
    chunk_summaries = []

    for chunk_num, chunk_text in enumerate(chunked_input):
        print(f"Processing chunk #{chunk_num+1}")
        chunk_summary = summarize_chunks(input_text=chunk_text, model_name=model_name, target_word_ct=500, temperature=0.25)
        chunk_summaries.append(chunk_summary)

    return chunk_summaries


def create_main_summary(chunk_summaries: list[list], model_name: str, summary_type: str = "summary", target_word_ct: int = 500, n_chunk_summary_groups: int = 2) -> str:
    if summary_type == "summary":
        print("Now processing main summary.")
        
        final_doc_summaries = []
        for doc_chunked_summary in chunk_summaries:
            chunk_summaries_to_process = doc_chunked_summary

            while len(chunk_summaries_to_process) > n_chunk_summary_groups:
                intermediate_summary_store = []
                summary_index_groups = group_indices(n_indices=len(chunk_summaries_to_process), n_groups=n_chunk_summary_groups)

                for index_group in summary_index_groups:
                    input_text = "\n".join([chunk_summaries_to_process[index] for index in index_group])

                    group_summary = summarize_chunks(input_text=input_text, model_name=model_name, target_word_ct=target_word_ct, temperature=1)
                    intermediate_summary_store.append(group_summary)

                chunk_summaries_to_process = intermediate_summary_store

            input_text = "\n".join(chunk_summaries_to_process)
            main_summary = summarize_chunks(input_text=input_text, model_name=model_name, target_word_ct=target_word_ct, temperature=1)
            final_doc_summaries.append(main_summary)

        final_summary = summarize_final(input_summaries=final_doc_summaries, model_name=model_name, target_word_ct=target_word_ct, temperature=1)

    # elif summary_type == "podcast":
    #     main_summary = podcastify(input_text=input_summaries, target_word_ct=target_word_ct)

    return final_summary