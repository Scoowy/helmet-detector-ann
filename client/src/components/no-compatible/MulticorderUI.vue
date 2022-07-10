<script>
// import Multicorder from "./Multicorder.vue";
import Multicorder from "./MulticorderComposition.vue";
import SelectInput from "./common/SelectInput.vue";

export default {
  name: "MulticorderUI",
  components: {
    Multicorder,
    SelectInput
  },
  props: {
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
  },
  data() {
    return {
      controls: null,
      videoSource: null,
      videoSourceList: [],
      isPaused: false,
      isPlayerPaused: false,
      isMuted: true,
      isPlayerMuted: true,
      view: "video",
      recordings: [], // local sparsed list of recording data
    };
  },
  methods: {
    onError(error) {
      console.log("Error emitted", error);
    },
    onCameras(cameras) {
      console.log("Available cameras", cameras);
      /**
       * We are implementing a `multicorder` with camera and screen support.
       * We need to create a list that groups the items for a `v-select` component.
       * We use the `listFromCameras` helper function provided by the component.
       * The Multicorder component maintains a list of `cameras` if we need them independently.
       */
      this.videoSourceList = this.$refs.multicorder.listFromCameras(cameras);
    },
    onVideoLive() {
      this.controls = "liveVideo";
    },
    onViewChange(view) {
      this.view = view;
    },
    onNewRecording(recording) {
      this.recordings.push(recording);
      if (this.recorderMode == "single") {
        // Load the video into the player and force disposition
        // this.view = "videoPlayer";
        this.loadRecording(0);
      }
    },
    onDeleteRecording(index) {
      this.recordings.splice(index, 1);
      if (this.recorderMode == "single") {
        this.controls = "liveVideo"
      }
    },
    onPlayerLoaded() {
      //this.playRecording();
    },
    videoRecord() {
      this.controls = "recordingVideo";
      this.$refs.multicorder.startVideoRecording();
    },
    videoSnapshot(fromView) {
      this.$refs.multicorder.videoSnapshot(fromView);
    },
    videoClose() {
      this.$refs.multicorder.stopVideo();
      this.view = "video";
      this.controls = "liveVideo";
      this.videoSource = null;
    },
    videoStopRecording() {
      this.$refs.multicorder.stopRecording();
      // resume the video, minus recording
      this.resume();
    },
    resume() {
      this.isPaused = false;
      this.$refs.multicorder.resume();
    },
    pause() {
      this.isPaused = true;
      this.$refs.multicorder.pause();
    },
    closeSnapshot() {
      this.$refs.multicorder.closeSnapshot();
    },
    snapshotDownload() {
      this.$refs.multicorder.downloadSnapshot();
    },
    downloadRecording(index) {
      if (this.recorderMode === 'single') {
        index = 0;
      }
      this.$refs.multicorder.downloadRecording(index);
    },
    deleteRecording(index) {
      if (this.recorderMode === 'single') {
        index = 0;
      }
      this.$refs.multicorder.deleteRecording(index);
    },
    async loadRecording(index) {
      await this.$refs.multicorder.loadRecording(index);
    },
    playRecording() {
      this.isPlayerPaused = false;
      this.$refs.multicorder.playRecording();
    },
    pausePlayer() {
      this.isPlayerPaused = true;
      this.$refs.multicorder.pausePlayer();
    },
    resumePlayer() {
      this.isPlayerPaused = false;
      this.$refs.multicorder.resumePlayer();
    },
    deletePlayerRecording() {
      this.$refs.multicorder.deletePlayerRecording();
    },
    closePlayer() {
      this.$refs.multicorder.closePlayer();
    },
    toggleMuted() {
      this.isMuted = !this.isMuted;
    },
    togglePlayerMuted() {
      this.isPlayerMuted = !this.isPlayerMuted;
    },
  },
};
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