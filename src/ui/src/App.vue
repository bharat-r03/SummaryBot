<script setup lang="ts">
import InputDialogBox from './components/InputDialogBox.vue';
</script>

<template>
  <div id="baseboard" className="grid grid-cols-2 h-screen w-screen">
    <div id="inputs" className="flex items-center justify-center">
      <InputDialogBox />
    </div>
    <div id="outputs" className="flex items-center justify-center">
      <p>hello world 2</p>
    </div>
  </div>
</template>