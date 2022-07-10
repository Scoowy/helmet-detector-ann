<script setup>
import {ref, computed, watch, onMounted, onBeforeUnmount} from 'vue';
// import WebCam from 'vue-web-cam';
import WebCam from '../components/WebCamComposite.vue';
import {useSocketConnection} from '../composables/socketConnection.js';
import {Mat, VideoCapture} from '@techstark/opencv-js'

const result = ref(null);
const img = ref(null);
const camera = ref(null);
const deviceId = ref(null);
const devices = ref([]);
const resolution = ref({width: 500, height: 500});
const FPS = ref(1);
const captureIntervalId = ref(null);
const numPredictions = ref(null)

// Socket refs
const {connect, disconnect, isConnected, send, on, predict, emitCustomEvent} = useSocketConnection();

// Refs for htlm elements
const webcam = ref(null);

const device = computed(
    () => devices.value.find(d => d.deviceId === deviceId.value)
);

watch(camera, (newVal) => {
  deviceId.value = newVal;
});

watch(devices, () => {
  let first = devices.value[0];
  if (first) {
    camera.value = first.deviceId;
    deviceId.value = first.deviceId;
  }
});

// Methods
function onCapture() {
  img.value = webcam.value.capture();
}

function onStarted(stream) {
  console.log("On Started Event", stream);
}

function onStopped(stream) {
  console.log("On Stopped Event", stream);
}

function onStop() {
  webcam.value.stop();
}

function onStart() {
  webcam.value.start();
}

function onError(error) {
  console.log("On Error Event", error);
}

function onCameras(cameras) {
  devices.value = cameras;
  console.log("On Cameras Event", cameras);
}

function onCameraChange(newDeviceId) {
  deviceId.value = newDeviceId;
  camera.value = newDeviceId;
  console.log("On Camera Change Event", newDeviceId);
}

function initPredict() {
  connect();
  // send('load-model', null)

  emitCustomEvent('load-model');

  on('model-loaded', () => {
    console.log('Model loaded')

    captureIntervalId.value = setInterval(() => {
      if (img.value) {
        let data = img.value
        // data = data.replace(/^data:image\/png;base64,/, "");
        predict(data);
      }
      onCapture();
    }, 1000 / FPS.value);
  });

  on('predicted', (dataImage, numPred) => {
    // console.log("Predicted", dataImage);
    result.value = dataImage;
    numPredictions.value = numPred;
  });
}

function endPredict() {
  disconnect();
  captureIntervalId.value && clearInterval(captureIntervalId.value);
  captureIntervalId.value = null;
  img.value = null;
  result.value = null
}

// onMounted(() => {
//   connect();
// });

onBeforeUnmount(() => {
  disconnect();
  captureIntervalId.value && clearInterval(captureIntervalId.value);
});


</script>

<template>
  <h1 class="page-title">Stream detect helmet</h1>
  <div class="wrapper">
    <div class="row">

      <div class="column">
        <div class="box-content shadow-lg">
          <div class="box-header">
            <h3 class="box-title">WebCam</h3>
          </div>
          <div class="box-body">
            <div class="camera-container">
              <code class="camera-title" v-if="device">{{ device.label }}</code>
              <web-cam ref="webcam" :device-id="deviceId" width="500" @started="onStarted" @stopped="onStopped"
                       @error="onError" @cameras="onCameras" @camera-change="onCameraChange"/>
              <div class="camera-menu">
                <button type="button" class="btn-circle btn-primary" @click="onCapture">
                  <fa-icon icon="fa-solid fa-camera"/>
                </button>
                <button type="button" class="btn-circle btn-danger" @click="onStop">
                  <fa-icon icon="fa-regular fa-circle-pause"/>
                </button>
                <button type="button" class="btn-circle btn-success" @click="onStart">
                  <fa-icon icon="fa-regular fa-circle-play"/>
                </button>
                <select v-if="devices" v-model="camera">
                  <option>-- Select Device --</option>
                  <option v-for="device in devices" :key="device.deviceId" :value="device.deviceId">{{ device.label }}
                  </option>
                </select>
              </div>
            </div>

          </div>
        </div>
      </div>

      <div class="column">
        <div class="box-content shadow-lg">
          <div class="box-header">
            <h3 class="box-title">Result</h3>
          </div>
          <div class="box-body">
            <figure class="figure">
              <img v-if="result" :src="result" class="img-responsive">
              <fa-icon v-else fade style="--fa-animation-duration: 2.3s" size="6x" icon="fa-regular fa-eye-slash"/>
            </figure>
          </div>
        </div>
      </div>

      <!--      <div class="column">-->
      <!--        <div class="box-content shadow-lg">-->
      <!--          <div class="box-header">-->
      <!--            <h3 class="box-title">Preview</h3>-->
      <!--          </div>-->
      <!--          <div class="box-body">-->
      <!--            <figure class="figure">-->
      <!--              <img v-if="img" :src="img" class="img-responsive">-->
      <!--              <fa-icon v-else fade style="&#45;&#45;fa-animation-duration: 2.3s" size="6x" icon="fa-regular fa-eye-slash" />-->
      <!--            </figure>-->
      <!--          </div>-->
      <!--        </div>-->
      <!--      </div>-->

    </div>
  </div>
  <div class="float-menu">
    <h2 v-if="isConnected">Conectado al cocket</h2>
    <button class="btn-circle btn-md" @click="initPredict">
      <fa-icon size="2x" icon="fa-regular fa-circle-play"/>
    </button>
    <button class="btn-circle btn-red btn-md" @click="endPredict">
      <fa-icon size="2x" icon="fa-regular fa-circle-pause"/>
    </button>
  </div>

</template>

<style>
video,
img,
figure {
  max-width: 100%;
  width: 100%;
  margin: 0;
}

.float-menu {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  top: 2rem;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-end;
  row-gap: .5rem;
  z-index: 1;
}

.btn-circle {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  color: #fff;
  background-color: #007bff;
  border: none;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.589);
}

.btn-circle:hover {
  background-color: #0069d9;
}

.btn-sm {
  width: 2.5rem;
  height: 2.5rem;
}

.btn-md {
  width: 3rem;
  height: 3rem;
}

.btn-lg {
  width: 5rem;
  height: 5rem;
}

.btn-red {
  background-color: #dc3545;
}

.btn-red:hover {
  background-color: #c82333;
}

.wrapper {
  margin: 1rem;
}

.row {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  width: 100%;
  column-gap: 2rem;
}

.column {
  display: flex;
  flex-direction: column;
  flex-basis: 100%;
}

.double-column {
  display: flex;
  flex-direction: column;
  flex-basis: 100%;
}

@media screen and (min-width: 800px) {
  .column {
    flex: 1
  }

  .double-column {
    flex: 2
  }
}

.box-content {
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 0.25rem;
  background-color: #fff;
}

.box-content .box-header {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 1rem;
}

.box-content .box-body {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.camera-container {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  justify-content: center;
  align-items: center;
  position: relative;
}

.camera-container > .camera-title {
  position: absolute;
  top: 0;
  left: 0;
  font-size: 1rem;
  color: #fff;
  background-color: rgba(85, 85, 85, 0.281);
  padding: 0.5rem;
  border-radius: 0.25rem;
}

.camera-container > .camera-menu {
  position: absolute;
  width: 100%;
  bottom: 0;
  right: 0;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-end;
  row-gap: .5rem;
  padding: 0.5rem;
  border-radius: 0.25rem;
}

.camera-container > .camera-menu > select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 0.25rem;
  background-color: #fff;
}
</style>
