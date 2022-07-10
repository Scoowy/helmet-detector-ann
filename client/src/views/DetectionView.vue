<script setup>
import {onMounted, ref, watch} from 'vue';
import {useDetectApi} from '../composables/detectApi';
import CircularLoader from '../components/common/CircularLoader.vue';
import PredictionResult from '../components/PredictionResult.vue';

const props = defineProps({
  typeFile: {
    type: String,
    default: 'image',
    validator: value => ['image', 'video'].includes(value),
  },
})

const {detectHelmets, isLoading, response, hasError} = useDetectApi();

const predictions = ref([]);
const dropdownCode = ref(null);
const isShowCode = ref(false);

onMounted(async () => {
  await detectHelmets(props.typeFile);
  predictions.value = response.value.data.predictions;
});

const onShowCode = (event) => {
  dropdownCode.value.classList.toggle('active');
};

</script>

<template>
  <h1 class="page-title">Detection results</h1>
  <div class="predictions" v-if="predictions">
    <PredictionResult v-for="prediction in predictions" :key="prediction.id"
                      :numDetections="prediction.detections.length" :fileName="prediction.filename"
                      :typeFile="typeFile"/>
  </div>
  <div class="code" ref="dropdownCode">
    <button class="btn-primary" @click="onShowCode">{{
        isShowCode ? 'Hide response code' : 'Show response code'
      }}
    </button>
    <pre>{{ response }}</pre>
  </div>
  <p v-if="hasError">ERROR</p>
  <CircularLoader v-if="isLoading" message="Detecting helmets, please wait..."/>
</template>

<style>
.code {
  padding: 1rem;
  background: #fafafa;
  border-radius: 0.5rem;
  border: 1px solid #ccc;
  height: min-content;
}

.code > pre {
  display: none;
}

.code.active > pre {
  display: block;
}

pre {
  text-align: left;
  font-size: 1rem;
  line-height: 1.5;
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.predictions {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 1rem 0;
  width: 100%;
}
</style>