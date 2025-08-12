import math


def chunk_input(input: list, n_items_per_chunk: int = 5) -> list[list]:
    chunked_inputs = []

    for idx in range(math.ceil(len(input) / n_items_per_chunk)):
        start, end = idx * n_items_per_chunk, (idx+1) * n_items_per_chunk
        chunked_inputs.append(input[start:end])

    return chunked_inputs


def get_file_ext(fpath: str) -> str:
    return fpath.split(".")[-1]