<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue';
import { v4 as uuidv4 } from "uuid";

const props = defineProps({
  videoSource: {
    type: Object,
    default: null,
  },
  width: {
    type: [Number, String],
    default: "100%",
  },
  height: {
    type: [Number, String],
    default: "100%",
  },
  autoplay: {
    type: Boolean,
    default: true,
  },
  playsinline: {
    type: Boolean,
    default: true,
  },
  recorderMuted: {
    type: Boolean,
    default: true,
  },
  playerMuted: {
    type: Boolean,
    default: true,
  },
  screenshotFormat: {
    type: String,
    default: "image/jpeg",
  },
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
  camerasHeader: {
    type: Array,
    default: () => {
      return [
        {
          divider: true,
          header: "Cameras",
        },
      ];
    },
  },
  staticVideoOptions: {
    type: Array,
    default: () => {
      return [
        {
          text: "Screen share",
          value: "screenshare",
        },
      ];
    },
  },
  staticVideoOptionsHeader: {
    type: Array,
    default: () => {
      return [
        {
          divider: true,
          header: "Screen Sharing",
        },
      ];
    },
  },
});

const source = ref(null);
const playerSource = ref(null);
const canvas = ref(null);
const snapshot = ref(null);
const snapshotSource = ref(null);
const cameras = ref([]);
const camerasEmitted = ref(false);
const browserScreenshareSupported = ref(null);
const recorder = ref(null);
const recordings = ref([]);
const view = ref("video");
const nowPlaying = ref(null);

// Other refs
const ctx = ref(null);
const resolution = ref({
  height: 400,
  width: 400,
});

// Refs html elements
const video = ref(null);
const videoPlayer = ref(null);

// Define emits
const emit = defineEmits([
  'video-change',
  'error',
  'video-change',
  'started',
  'cameras',
  'notsupported',
  'stoppedVideo',
  'new-recording',
  'delete-recording',
  'player-loaded'
])

// Methods
function setView(newView) {
  view.value = newView;
  emit("view-change", newView);
}

function changeVideoSource(videoSource) {
  stopVideo();
  emit("video-change", videoSource);
  if (videoSource) {
    if (videoSource == "screenshare") {
      startScreenshare();
    } else {
      loadCamera(videoSource.value);
    }
  }
}

function loadCamera(device) {
  let constraints = {
    video: {
      deviceId: { exact: device }
    },
    audio: { echoCancellation: true }
  };
  if (resolution.value) {
    constraints.video.height = resolution.value.height;
    constraints.video.width = resolution.value.width;
  }
  navigator.mediaDevices
    .getUserMedia(constraints)
    .then((stream) => loadSrcStream(stream))
    .catch((error) => emit("error", error));
}

function startScreenshare() {
  try {
    navigator.mediaDevices
      .getDisplayMedia()
      .then((stream) => loadSrcStream(stream));
  } catch (err) {
    console.error("Error: " + err);
  }
}

function loadSrcStream(stream) {
  if ("srcObject" in video) {
    // new browsers api
    video.srcObject = stream;
  } else {
    // old broswers
    source.value = window.HTMLMediaElement.srcObject(stream);
  }
  // Emit video start/live event
  video.onloadedmetadata = () => {
    emit("video-live", stream);
  };
  emit("started", stream);
}

function initVideoOptions() {
  if (props.videoTypes.includes("screen")) {
    initScreen();
  }
  if (props.videoTypes.includes("camera")) {
    initCameras();
  } else {
    emit("cameras", []);
    camerasEmitted.value = true;
  }
}

function initScreen() {
  // @todo Add check for browsers that don't support screenshare.
  browserScreenshareSupported.value = true;
}

function initCameras() {
  if (navigator.mediaDevices === undefined) {
    navigator.mediaDevices = {};
  }
  if (navigator.mediaDevices.getUserMedia === undefined) {
    navigator.mediaDevices.getUserMedia = legacyGetUserMediaSupport();
  }
  testVideoAccess();
}

function testVideoAccess() {
  let constraints = { video: true, audio: { echoCancellation: true } };
  if (resolution.value) {
    constraints.video = {};
    constraints.video.height = resolution.value.height;
    constraints.video.width = resolution.value.width;
  }
  navigator.mediaDevices
    .getUserMedia(constraints)
    .then((stream) => {
      let tracks = stream.getTracks();
      tracks.forEach((track) => {
        track.stop();
      });
      loadCameras();
    })
    .catch((error) => emit("error", error));
}

// function testVideoAccess() {
//   let constraints = { video: true, audio: { echoCancellation: true } };
//   if (this.resolution) {
//     constraints.video = {};
//     constraints.video.height = this.resolution.height;
//     constraints.video.width = this.resolution.width;
//   }
//   navigator.mediaDevices
//     .getUserMedia(constraints)
//     .then((stream) => {
//       let tracks = stream.getTracks();
//       tracks.forEach((track) => {
//         track.stop();
//       });
//       loadCameras();
//     })
//     .catch((error) => emit("error", error));
// }

function legacyGetUserMediaSupport() {
  return (constraints) => {
    let getUserMedia =
      navigator.getUserMedia ||
      navigator.webkitGetUserMedia ||
      navigator.mozGetUserMedia ||
      navigator.msGetUserMedia ||
      navigator.oGetUserMedia;
    // Some browsers just don't implement it - return a rejected promise with an error
    // to keep a consistent interface
    if (!getUserMedia) {
      return Promise.reject(
        new Error("getUserMedia is not implemented in this browser")
      );
    }
    // Otherwise, wrap the call to the old navigator.getUserMedia with a Promise
    return new Promise(function (resolve, reject) {
      getUserMedia.call(navigator, constraints, resolve, reject);
    });
  };
}

function loadCameras() {
  navigator.mediaDevices
    .enumerateDevices()
    .then((deviceInfos) => {
      for (let i = 0; i !== deviceInfos.length; ++i) {
        let deviceInfo = deviceInfos[i];
        if (deviceInfo.kind === "videoinput") {
          // store only the data we need
          cameras.value.push({
            text: deviceInfo.label,
            value: deviceInfo.deviceId,
          });
        }
      }
    })
    .then(() => {
      if (!camerasEmitted.value) {
        emit("cameras", cameras.value);
        camerasEmitted.value = true;
      }
    })
    .catch((error) => emit("notsupported", error));
}

function stopVideo() {
  if (video.value !== null && video.value.srcObject) {
    stopStreamedVideo(video.value);
  }
}

function stopStreamedVideo(videoElem) {
  let stream = videoElem.srcObject;
  let tracks = stream.getTracks();
  tracks.forEach((track) => {
    track.stop();
    emit("stoppedVideo", stream);
    video.srcObject = null;
    source.value = null;
  });
}

function listFromCameras(cameras) {
  if (browserScreenshareSupported.value && cameras.length > 0) {
    return [
      // ...props.camerasHeader,
      ...cameras,
      // ...props.staticVideoOptionsHeader,
      ...props.staticVideoOptions,
    ];
  } else if (browserScreenshareSupported.value && cameras.length === 0) {
    return props.staticVideoOptions;
  }
  return cameras;
}


function startVideoRecording() {
  const stream = video.srcObject;
  const recorderMedia = new MediaRecorder(stream);
  recorder.value = recorderMedia;
  recorder.value.ondataavailable = (event) => pushVideoData(event.data);
  recorder.value.start();
}

async function pushVideoData(data) {
  if (data.size > 0) {
    const uid = await uuidv4();
    data.name = "clip-" + uid + ".webm";
    recordings.value.push(data);
    if (props.recorderMode == "single") {
      setView("videoPlayer");
    }
    emit("new-recording", { name: data.name, size: data.size });
  }
}

async function stopRecording() {
  if (video.value !== null && video.value.srcObject) {
    recorder.value.stop();
  }
}

function pause() {
  if (video.value !== null && video.value.srcObject) {
    video.value.pause();
  }
}

function resume() {
  if (video.value !== null && video.value.srcObject) {
    video.value.play();
  }
}

function videoSnapshot(fromView) {
  snapshot.value = getCanvas().toDataURL(props.screenshotFormat);
  snapshotSource.value = fromView;
  setView("snapshot");
}

function getCanvas() {
  let video = video.value;
  if (!ctx.value) {
    let canvasHtml = document.createElement("canvas");
    canvasHtml.height = video.videoHeight;
    canvasHtml.width = video.videoWidth;
    canvas.value = canvasHtml;
    ctx.value = canvasHtml.getContext("2d");
  }

  ctx.value.drawImage(video, 0, 0, canvas.value.width, canvas.value.height);
  return canvas.value;
}

async function dataURItoBlob(dataURI) {
  // convert base64/URLEncoded data component to raw binary data held in a string
  var byteString;
  if (dataURI.split(",")[0].indexOf("base64") >= 0)
    byteString = atob(dataURI.split(",")[1]);
  else byteString = unescape(dataURI.split(",")[1]);
  // separate out the mime component
  var mimeString = dataURI.split(",")[0].split(":")[1].split(";")[0];
  // write the bytes of the string to a typed array
  var ia = new Uint8Array(byteString.length);
  for (var i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i);
  }
  return new Blob([ia], { type: mimeString });
}

async function closeSnapshot() {
  setView(snapshotSource.value);
  snapshot.value = null;
}


async function downloadSnapshot() {
  const imgInfo = await dataURItoBlob(snapshot.value);
  const a = document.createElement("a");
  document.body.appendChild(a);
  a.style = "display: none";
  a.href = snapshot.value;
  const uid = await uuidv4();
  a.download = uid + imgInfo.type.split("/").pop();
  a.click();
}

async function downloadRecording(recordingIndex) {
  var blob = recordings.value[recordingIndex];
  var url = URL.createObjectURL(blob);
  var a = document.createElement("a");
  document.body.appendChild(a);
  a.style = "display: none";
  a.href = url;
  a.download = "video.webm";
  a.click();
  window.URL.revokeObjectURL(url);
}

function deleteRecording(index) {
  if (props.recorderMode == "single") {
    setView("video");
  }
  recordings.value.splice(index, 1);
  emit("delete-recording", index);
}

async function loadRecording(index) {
  const recording = recordings.value[index];
  const clip = window.URL.createObjectURL(recording);
  playerSource.value = clip;
  nowPlaying.value = index;
  setView("videoPlayer");
  emit("player-loaded", true);
}

function playRecording() {
  videoPlayer.value.play();
}

function pausePlayer() {
  if (videoPlayer.value !== null) {
    videoPlayer.value.pause();
  }
}

function resumePlayer() {
  if (videoPlayer.value !== null) {
    videoPlayer.value.play();
  }
}

function deletePlayerRecording() {
  setView("video");
  deleteRecording(nowPlaying.value);
}

function closePlayer() {
  setView("video");
}

function muteRecorder() {
  video.value.mute();
}

// Life cycle hooks
onMounted(() => {
  initVideoOptions()
});

onBeforeUnmount(() => {
  stopVideo()
})

// Watchers
watch(() => props.videoSource, (newVal, preVal) => {
  console.log(newVal)
  changeVideoSource(newVal)
})

</script>

<template>
  <div class="multicorder">
    <video v-show="view == 'video'" ref="video" :width="width" :height="height" :src="source" :autoplay="autoplay"
      :playsinline="playsinline" muted="muted" />
    <img v-show="view == 'snapshot'" :src="snapshot" width="100%" height="100%" />
    <video v-show="view == 'videoPlayer'" ref="videoPlayer" :width="width" :height="height" :src="playerSource"
      :playsinline="playsinline" />
  </div>
</template>