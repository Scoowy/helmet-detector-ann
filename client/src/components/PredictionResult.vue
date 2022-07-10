<script setup>
import {ref} from 'vue';

const props = defineProps({
  numDetections: {
    type: Number,
    default: 0
  },
  fileName: {
    type: String,
    default: ''
  },
  typeFile: {
    type: String,
    default: 'image',
    validator: value => ['image', 'video'].includes(value),
  },
})

const predictionClass = ref('prediction');
const predictionText = ref('No helmet detected');

if (props.numDetections > 0) {
  predictionClass.value = predictionClass.value + ' bg-green';
} else {
  predictionClass.value = predictionClass.value + ' bg-red';
}

if (props.numDetections === 1) {
  predictionText.value = '1 helmet detected';
} else if (props.numDetections > 1) {
  predictionText.value = `${props.numDetections} helmets detected`;
}
</script>

<template>
  <div :class="predictionClass">
    <div class="prediction-image">
      <img v-if="typeFile === 'image'" :src="'http://localhost:8000/api/v1/files/' + fileName"/>
      <video v-else :src="'http://localhost:8000/api/v1/files/' + fileName" controls></video>
    </div>
    <div class="prediction-label">
      <h2>{{ predictionText }}</h2>
    </div>
  </div>
</template>

<style scoped>
.prediction {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 1rem 0;
  width: 100%;
  border: 1px solid #ccc;
}

.prediction img,
.prediction video {
  width: 100%;
  height: auto;
}

.bg-green,
.bg-red {
  background: #fafafa;
  border-radius: 1rem;
  border-width: 3px;
  border-style: solid;
  border-color: #ccc;
}

.bg-green {
  border-color: #9bf09b;
  box-shadow: 0 0 10px rgba(153, 240, 153, 0.5);
}

.bg-red {
  border-color: #ee9292;
  box-shadow: 0 0 10px rgba(240, 153, 153, 0.5);
}
</style>