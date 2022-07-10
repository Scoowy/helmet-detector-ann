<script setup>
import { ref } from 'vue';
import Multicorder from "./MulticorderComposition.vue";
import SelectInput from "./common/SelectInput.vue";

const controls = ref(null);
const videoSource = ref(null);
const videoSourceList = ref([]);
const isPaused = ref(false);
const isPlayerPaused = ref(false);
const isMuted = ref(true);
const isPlayerMuted = ref(true);
const view = ref("video");
const recordings = ref([]);

// Refs html elements
const multicorder = ref(null);

const props = defineProps({
  videoTypes: {
    type: Array,
    default: () => {
      return ["camera", "screen"];
    },
  },
  recorderMode: {
    type: String,
    default: "single",
  },
})

function onError(error) {
  console.log("Error emitted", error);
}

function onCameras(cameras) {
  console.log("Available cameras", cameras);
  /**
   * We are implementing a `multicorder` with camera and screen support.
   * We need to create a list that groups the items for a `v-select` component.
   * We use the `listFromCameras` helper function provided by the component.
   * The Multicorder component maintains a list of `cameras` if we need them independently.
   */
  videoSourceList.value = multicorder.value.listFromCameras(cameras);
}

function onVideoLive() {
  controls.value = "liveVideo";
}

function onViewChange(newView) {
  view.value = newView;
}

function onNewRecording(recording) {
  recordings.value.push(recording);
  if (props.recorderMode == "single") {
    // Load the video into the player and force disposition
    // this.view = "videoPlayer";
    loadRecording(0);
  }
}

function onDeleteRecording(index) {
  recordings.value.splice(index, 1);
  if (props.recorderMode == "single") {
    controls.value = "liveVideo"
  }
}

function onPlayerLoaded() {
  //this.playRecording();
}

function videoRecord() {
  controls.value = "recordingVideo";
  multicorder.value.startVideoRecording();
}

function videoSnapshot(fromView) {
  multicorder.value.videoSnapshot(fromView);
}

function videoClose() {
  multicorder.value.stopVideo();
  video.value = "video";
  controls.value = "liveVideo";
  videoSource.value = null;
}


function videoStopRecording() {
  multicorder.value.stopRecording();
  // resume the video, minus recording
  resume();
}

function resume() {
  isPaused.value = false;
  multicorder.value.resume();
}

function pause() {
  isPaused.value = true;
  multicorder.value.pause();
}

function closeSnapshot() {
  multicorder.value.closeSnapshot();
}

function snapshotDownload() {
  multicorder.value.downloadSnapshot();
}

function downloadRecording(index) {
  if (props.recorderMode === 'single') {
    index = 0;
  }
  multicorder.value.downloadRecording(index);
}

function deleteRecording(index) {
  if (props.recorderMode === 'single') {
    index = 0;
  }
  multicorder.value.deleteRecording(index);
}

async function loadRecording(index) {
  await multicorder.value.loadRecording(index);
}


function playRecording() {
  isPlayerPaused.value = false;
  multicorder.value.playRecording();
}

function pausePlayer() {
  isPlayerPaused.value = true;
  multicorder.value.pausePlayer();
}

function resumePlayer() {
  isPlayerPaused.value = false;
  multicorder.value.resumePlayer();
}

function deletePlayerRecording() {
  multicorder.value.deletePlayerRecording();
}

function closePlayer() {
  multicorder.value.closePlayer();
}

function toggleMuted() {
  isMuted.value = !isMuted.value;
}

function togglePlayerMuted() {
  isPlayerMuted.value = !isPlayerMuted.value;
}
</script>

<template>
  <div class="container-video">
    <div class="videobox">
      <Multicorder :video-source="videoSource" @error="onError" @cameras="onCameras" @video-live="onVideoLive"
        @view-change="onViewChange" @new-recording="onNewRecording" @delete-recording="onDeleteRecording"
        @player-loaded="onPlayerLoaded" ref="multicorder" :videoTypes="videoTypes" :recorderMode="recorderMode" />
    </div>

    <SelectInput v-if="videoSource == null" v-show="view == 'video'" :options="videoSourceList" v-model="videoSource"
      label="Select video input" />

    <div v-if="videoSource" align="right" background-color="black" class="grey--text videobox">
      {{ videoSource.text }}
      <fa-icon @click="videoClose" color="grey" icon="fa-regular fa-circle-xmark" />
    </div>

    <div v-show="view == 'videoPlayer'" class="row text-center mt-3 pt-0">
      <div cols="col auto" align="left">
        <fa-icon class="mx-2" large color="red" v-if="!isPlayerMuted" @click="togglePlayerMuted"
          icon="fa-solid fa-volume-high" />
        <fa-icon class="mx-2" large v-if="isPlayerMuted" @click="togglePlayerMuted" icon="fa-solid fa-volume-xmark" />
      </div>
      <div class="col" align="center">
        <button class="mx-2" @click="playRecording" fab mdi-icon x-small light>
          <fa-icon x-large color="red" icon="fa-regular fa-circle-play" />
        </button>
        <button class="mx-2" @click="downloadRecording" fab mdi-icon x-small light>
          <fa-icon x-large icon="fa-regular fa-circle-down" />
        </button>
        <button class="mx-2" @click="deleteRecording" fab mdi-icon x-small light>
          <fa-icon x-large color="red" icon="fa-regular fa-circle-xmark" />
        </button>
      </div>
      <div class="col" align="right">
        <fa-icon x-large @click="videoSnapshot(view)" color="teal" icon="fa-solid fa-camera" />
      </div>
    </div>

    <div class="row" v-show="view == 'video' && videoSource != null">
      <div class="col center">
        <fa-icon large color="red" v-if="!isMuted" @click="toggleMuted" icon="fa-solid fa-microphone" />
        <fa-icon large v-if="isMuted" @click="toggleMuted" icon="fa-solid fa-microphone-slash" />
      </div>
      <div class="col center">
        <button v-show="controls == 'liveVideo'" class="mx-2" @click="videoRecord" fab mdi-icon x-small light>
          <fa-icon icon="fa-regular fa-circle-dot" x-large color="red" />
        </button>
        <button v-show="controls == 'recordingVideo'" class="mx-2" @click="videoStopRecording" fab mdi-icon x-small
          light>
          <fa-icon icon="fa-regular fa-circle-stop" color="red" x-large />
        </button>
        <button v-show="controls == 'recordingVideo'" class="mx-2" @click="pause" fab mdi-icon x-small light
          v-if="!isPaused">
          <fa-icon icon="fa-regular fa-circle-pause" />
        </button>
        <button v-show="controls == 'recordingVideo'" class="mx-2" @click="resume" fab mdi-icon x-small dark
          v-if="isPaused">
          <fa-icon icon="fa-regular fa-circle-pause" />
        </button>
      </div>
      <div class="col center">
        <fa-icon icon="fa-solid fa-camera" @click="videoSnapshot(view)" color="teal" />
      </div>
    </div>

    <div v-show="view == 'snapshot'" class="snapshot-menu">
      <button class="btn-primary" @click="closeSnapshot()">
        <fa-icon icon="fa-regular fa-circle-xmark" />
      </button>
      <button class="btn-primary" @click="snapshotDownload">
        <fa-icon icon="fa-regular fa-floppy-disk" />
      </button>
    </div>
  </div>
</template>

<style scoped>
.container-video {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.videobox {
  background-color: black;
}
</style>