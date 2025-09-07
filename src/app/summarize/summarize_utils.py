import math


def chunk_input(input: list, n_items_per_chunk: int = 3) -> list[list]:
    chunked_inputs = []

    for idx in range(math.ceil(len(input) / n_items_per_chunk)):
        start, end = idx * n_items_per_chunk, (idx+1) * n_items_per_chunk
        chunked_inputs.append(input[start:end])

    return chunked_inputs


def get_file_ext(fpath: str) -> str:
    return fpath.split(".")[-1]


def group_indices(n_indices: int, n_groups: int) -> list[list]:
    grouped_indices, current_index_group = [], []

    for index in range(n_indices):
        current_index_group.append(index)
        if len(current_index_group) == n_groups:
            grouped_indices.append(current_index_group)
            current_index_group = []

    if current_index_group:
        grouped_indices.append(current_index_group)
    
    return grouped_indices