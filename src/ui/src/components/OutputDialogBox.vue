<script setup lang="ts">

import { PhLegoSmiley } from '@phosphor-icons/vue';

</script>

<template>
    <div className="h-3/4 w-1/2 rounded-xl shadow-xl bg-white flex flex-col items-center justify-center">
        <div className="h-95/100 w-95/100 border-1 rounded-xl border-gray-300 border-dashed flex flex-col items-center justify-center">
            <PhLegoSmiley :size="96" color="#9CA3AF" weight="thin" />
            <p className="mt-5 text-gray-400 text-xl">Waiting for a task!</p>
        </div>
    </div>
</template>