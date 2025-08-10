<script setup lang="ts">

import { PhLegoSmiley } from '@phosphor-icons/vue';
import { audioBytes } from './varStore';
import { ref } from 'vue';

let url = "";

const isAudioPresent = () => {
    if (audioBytes.bytes != null) {
        var wav = new Blob([audioBytes.bytes], { type: 'audio/wav' });
        url = window.URL.createObjectURL(wav);

        return true;
    }

    else {
        return false;
    };
}

</script>

<template>
    <div className="h-3/4 w-1/2 rounded-xl shadow-xl bg-white flex flex-col items-center justify-center">
        <div :class="[ isAudioPresent() ? '' : 'border-1 rounded-xl border-gray-300 border-dashed', 'h-95/100 w-95/100 flex flex-col items-center justify-center', ]">
            <!-- If audio IS NOT present -->
            <PhLegoSmiley :size="96" color="#9CA3AF" weight="thin" v-if="!isAudioPresent()" />
            <p className="my-5 text-gray-400 text-xl" v-if="!isAudioPresent()">Waiting for a task!</p>

            <!-- If audio IS present -->
            
            <audio :src="url" v-if="isAudioPresent()" className="w-full" controls></audio>
        </div>
    </div>
</template>