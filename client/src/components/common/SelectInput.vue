<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  options: {
    type: Array,
    default: () => ([]),
  },
  modelValue: {
    type: Object,
    default: () => ({}),
  },
  label: {
    type: String,
    default: () => (""),
  },
});

const emit = defineEmits(['update:modelValue']);

const value = ref(null);

watch(value, (newValue) => {
  console.log("New value", newValue);

  const sel = props.options.find(option => option.value == newValue);

  if (sel) {
    emit('update:modelValue', sel);
  }

});
</script>

<template>
  <div class="selectGroup">
    <div class="selectGroup__label">
      <label for="selector">{{ label }}</label>
    </div>
    <div class="selectGroup__select">
      <select name="selector" v-model="value">
        <option v-for="option in options" :key="option.value" :value="option.value">{{ option.text }}</option>
      </select>
    </div>
  </div>
</template>

<style scoped>
.selectGroup {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
}

.selectGroup__label {
  margin-bottom: 0.5rem;
}

.selectGroup__select {
  margin-bottom: 1rem;
}
</style>