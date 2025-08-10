<script setup lang="ts">
import InputDialogBox from './components/InputDialogBox.vue';
import OutputDialogBox from './components/OutputDialogBox.vue';
</script>

<template>
  <div id="baseboard" className="grid grid-cols-2 h-screen w-screen">
    <div id="inputs" className="flex items-center justify-center ml-20">
      <InputDialogBox />
    </div>
    <div id="outputs" className="flex items-center justify-center mr-20">
      <OutputDialogBox />
    </div>
  </div>
</template>