<script setup>
import { ref } from 'vue';

defineProps({
  message: String
})

const showNotification = ref(false);

</script>

<template>
  <div class="floatNotification">
    <div class="floatNotification__content">
      <div class="floatNotification__content__icon">
        <i class="fas fa-exclamation-triangle"></i>
      </div>
      <div class="floatNotification__content__text">
        <p>{{ message }}</p>
      </div>
    </div>
  </div>
</template>

<style>
</style>