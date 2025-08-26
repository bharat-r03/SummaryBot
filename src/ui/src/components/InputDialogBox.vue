<script setup lang="ts">
import { PhCloudArrowUp } from '@phosphor-icons/vue';
import { reactive, ref } from 'vue'
import {
Listbox,
ListboxButton,
ListboxOptions,
ListboxOption,
} from '@headlessui/vue'
import { CheckIcon, ChevronUpDownIcon } from "@heroicons/vue/20/solid"
import axios from 'axios';
import { audioBytes, isPressed, stageCompletion, isDarkMode } from './varStore';


const voices = [
    "Female",
    "Male"
]
const selectedVoice = ref(voices[0])

const summaryTypes = [
    "Summary",
]
const selectedSummaryType = ref(summaryTypes[0])

const models = [
    "Gemma 3 - 4B",
    "Llama 3.2 - 3B"
]

const selectedModel = ref(models[0])

const apiClient = axios.create({
    baseURL: "http://127.0.0.1:8000/generate",
    withCredentials: false,
    headers: {
        "Content-Type": "multipart/form-data"
    },
    timeout: 3600000
});

const formState = reactive({
    files: null as FileList | null
});

const handleInput = (event: Event) => {
    let files = (event.target as HTMLInputElement).files;

    if (files != null) {
        appendFiles(files);
    }
};

const appendFiles = (uploaded_files: FileList) => {
    formState.files = uploaded_files;
};

const submitForm = () => {
    try {
        if (isPressed.value) return;
        isPressed.value = true;

        stageCompletion.load_model = false;
        stageCompletion.process_files = false;
        stageCompletion.summarize_files = false;
        stageCompletion.summarize_main = false;
        stageCompletion.text_to_audio = false;
        stageCompletion.processing_complete = false;


        audioBytes.bytes = null;
    
        let formData = new FormData();
        
        if (formState.files != null) {
            for (var x=0; x<formState.files.length; x++) {
                formData.append("files", formState.files[x]);
            }
        }
        formData.append("voice", selectedVoice.value);
        formData.append("summary_type", selectedSummaryType.value);
        formData.append("model", selectedModel.value)
        
        apiClient.post('', formData)
            .then((response) => {
                console.log("API was called succesfully!");

                audioBytes.bytes = Uint8Array.from(atob(response.data), c => c.charCodeAt(0));
                isPressed.value = false;
            })
            .catch(() => {
                if (isPressed.value) {
                    isPressed.value = false;
                }
            });
        } catch (error) {
            console.log(error);
            if (isPressed.value) {
                isPressed.value = false;
            };
        };
}



</script>

<template>
    <div :class="[ isDarkMode ? 'bg-gray-800' : 'bg-white', 'h-7/8 w-1/2 rounded-xl shadow-xl flex flex-col items-center justify-center' ]">
        <h3 :class="[ isDarkMode ? 'text-white' : 'text-black', '2xl:text-2xl text-xl font-bold my-3 mx-5 text-center' ]">Audio Summary Converter</h3>
        <p :class="[ isDarkMode ? 'text-gray-400' : 'text-gray-500', 'text-center mb-5 2xl:text-base text-sm']">Convert uploaded files into an audio summary or podcast</p>
        <form enctype="multipart/form-data" method="post" className="flex flex-col items-center justify-center w-full 2xl:h-4/7 h-5/8" v-on:submit.prevent="submitForm">
            <div :class="[ isDarkMode ? 'border-gray-600' : 'border-gray-300', 'flex flex-row w-2/3 h-1/7 border-1 rounded-lg items-center mb-5 min-h-10' ]">
                <label for="files" :class="[ isDarkMode ? 'text-white' : 'text-gray-500', 'h-full flex items-center pl-5 2xl:text-2xl text-xl cursor-pointer' ]"><PhCloudArrowUp /></label>
                <input :class="[ isDarkMode ? 'file:text-white dark:text-gray-200' : 'file:text-gray-500 dark:text-gray-400', 'file:h-full dark:h-full w-full flex flex-col items-center file:cursor-pointer file:pl-3 file:pr-2 2xl:file:text-base file:text-sm file:font-medium dark:cursor-pointer dark:font-light 2xl:dark:text-sm dark:text-xs dark:mr-3' ]" name="files" type="file" id="files" @input="handleInput" multiple>
            </div>
            <div className="flex flex-col w-2/3 h-1/5 mb-5">
                <label for="voice" :class="[ isDarkMode ? 'text-white' : 'text-black', 'font-medium mb-2 2xl:text-base text-sm' ]">Speaker Voice</label>
                <Listbox v-model="selectedVoice" name="voice" id="voice">
                    <div class="relative h-full">
                        <ListboxButton :class="[ isDarkMode ? 'bg-gray-700 border-gray-600' : 'bg-white border-gray-300', 'relative w-full h-full cursor-default rounded-lg py-2 pl-5 pr-10 text-left border-1' ]">
                            <span :class="[ isDarkMode ? 'text-white' : 'text-black', 'block truncate 2xl:text-base font-normal text-sm' ]">{{ selectedVoice }}</span>
                            <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                                <ChevronUpDownIcon :class="[ isDarkMode ? 'text-white' : 'text-gray-400', 'h-5 w-5' ]" aria-hidden="true" />
                            </span>
                        </ListboxButton>

                        <transition leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100" leave-to-class="opacity-0">
                            <ListboxOptions :class="[ isDarkMode ? 'bg-gray-700' : 'bg-white', 'absolute mt-1 max-h-60 w-full overflow-auto rounded-md py-1 text-base shadow-lg ring-1 ring-black/5 focus:outline-none sm:text-sm z-50' ]">
                                    <ListboxOption v-slot="{ active, selected }" v-for="voice in voices" :key="voice" :value="voice" as="template">
                                        <li :class="[ active ? isDarkMode ? 'bg-gray-600 text-white' : 'bg-gray-200 text-gray-600' : isDarkMode ? 'text-white' : 'text-gray-600', 'relative cursor-default select-none py-2 pl-10 pr-4', ]">
                                            <span :class="[ selected ? 'font-medium' : 'font-normal', 'block truncate', ]">{{ voice }}</span>   
                                            <span v-if="selected" :class="[ isDarkMode ? 'text-white' : 'text-gray-400', 'absolute inset-y-0 left-0 flex items-center pl-3' ]">
                                                <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                            </span>
                                        </li>
                                    </ListboxOption>
                            </ListboxOptions>
                        </transition>
                    </div>
                </Listbox>
            </div>
            <div className="flex flex-col w-2/3 h-1/5 mb-5">
                <label for="type" :class="[ isDarkMode ? 'text-white' : 'text-black', 'font-medium mb-2 2xl:text-base text-sm' ]">Summary Type</label>
                <Listbox v-model="selectedSummaryType" name="type" id="type">
                    <div class="relative h-full">
                        <ListboxButton :class="[ isDarkMode ? 'bg-gray-700 border-gray-600' : 'bg-white border-gray-300', 'relative w-full h-full cursor-default rounded-lg py-2 pl-5 pr-10 text-left border-1' ]">
                            <span :class="[ isDarkMode ? 'text-white' : 'text-black', 'block truncate 2xl:text-base font-normal text-sm' ]">{{ selectedSummaryType }}</span>
                            <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                                <ChevronUpDownIcon :class="[ isDarkMode ? 'text-white' : 'text-gray-400', 'h-5 w-5' ]" aria-hidden="true" />
                            </span>
                        </ListboxButton>

                        <transition leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100" leave-to-class="opacity-0">
                            <ListboxOptions :class="[ isDarkMode ? 'bg-gray-700' : 'bg-white', 'absolute mt-1 max-h-60 w-full overflow-auto rounded-md py-1 text-base shadow-lg ring-1 ring-black/5 focus:outline-none sm:text-sm z-50' ]">
                                    <ListboxOption v-slot="{ active, selected }" v-for="summaryType in summaryTypes" :key="summaryType" :value="summaryType" as="template">
                                        <li :class="[ active ? isDarkMode ? 'bg-gray-600 text-white' : 'bg-gray-200 text-gray-600' : isDarkMode ? 'text-white' : 'text-gray-600', 'relative cursor-default select-none py-2 pl-10 pr-4', ]">
                                            <span :class="[ selected ? 'font-medium' : 'font-normal', 'block truncate', ]">{{ summaryType }}</span>
                                            <span v-if="selected" :class="[ isDarkMode ? 'text-white' : 'text-gray-400', 'absolute inset-y-0 left-0 flex items-center pl-3' ]">
                                                <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                            </span>
                                        </li>
                                    </ListboxOption>
                            </ListboxOptions>
                        </transition>
                    </div>
                </Listbox>
            </div>
            <div className="flex flex-col w-2/3 h-1/5 mb-5">
                <label for="model" :class="[ isDarkMode ? 'text-white' : 'text-black', 'font-medium mb-2 2xl:text-base text-sm' ]">Summarization Model</label>
                <Listbox v-model="selectedModel" name="model" id="model">
                    <div class="relative h-full">
                        <ListboxButton :class="[ isDarkMode ? 'bg-gray-700 border-gray-600' : 'bg-white border-gray-300', 'relative w-full h-full cursor-default rounded-lg py-2 pl-5 pr-10 text-left border-1' ]">
                            <span :class="[ isDarkMode ? 'text-white' : 'text-black', 'block truncate 2xl:text-base font-normal text-sm' ]">{{ selectedModel }}</span>
                            <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                                <ChevronUpDownIcon :class="[ isDarkMode ? 'text-white' : 'text-gray-400', 'h-5 w-5' ]" aria-hidden="true" />
                            </span>
                        </ListboxButton>

                        <transition leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100" leave-to-class="opacity-0">
                            <ListboxOptions :class="[ isDarkMode ? 'bg-gray-700' : 'bg-white', 'absolute mt-1 max-h-60 w-full overflow-auto rounded-md py-1 text-base shadow-lg ring-1 ring-black/5 focus:outline-none sm:text-sm z-50' ]">
                                    <ListboxOption v-slot="{ active, selected }" v-for="model in models" :key="model" :value="model" as="template">
                                        <li :class="[ active ? isDarkMode ? 'bg-gray-600 text-white' : 'bg-gray-200 text-gray-600' : isDarkMode ? 'text-white' : 'text-gray-600', 'relative cursor-default select-none py-2 pl-10 pr-4', ]">
                                            <span :class="[ selected ? 'font-medium' : 'font-normal', 'block truncate', ]">{{ model }}</span>
                                            <span v-if="selected" :class="[ isDarkMode ? 'text-white' : 'text-gray-400', 'absolute inset-y-0 left-0 flex items-center pl-3' ]">
                                                <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                            </span>
                                        </li>
                                    </ListboxOption>
                            </ListboxOptions>
                        </transition>
                    </div>
                </Listbox>
            </div>
            <input type="submit" :class="[isPressed ? 'bg-gray-500 cursor-default' : 'bg-blue-500 cursor-pointer', 'w-2/3 h-1/7 min-h-10 text-white font-medium rounded-lg my-3 2xl:text-base text-sm', ]" value="Generate audio summary">
        </form>
    </div>
</template>