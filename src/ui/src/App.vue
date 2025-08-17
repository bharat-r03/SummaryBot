<script setup lang="ts">
import InputDialogBox from './components/InputDialogBox.vue';
import OutputDialogBox from './components/OutputDialogBox.vue';
import { isDarkMode } from './components/varStore';
</script>

<template>
  <div id="baseboard" :class="[ isDarkMode ? 'bg-gray-900' : 'bg-white', 'grid grid-cols-2 h-screen w-screen' ]">
    <div id="inputs" className="flex items-center justify-center ml-20">
      <InputDialogBox />
    </div>
    <div id="outputs" className="flex items-center justify-center mr-20">
      <OutputDialogBox />
    </div>
  </div>
</template>