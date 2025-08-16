import { reactive, ref } from "vue";

export const audioBytes = reactive({
    bytes: null as Uint8Array | null
});


export const isPressed = ref(false);
export const wasPressed = ref(false);


export const stageCompletion = reactive({
    load_model: false,
    process_files: false,
    summarize_files: false,
    summarize_main: false,
    text_to_audio: false,
    processing_complete: false
})