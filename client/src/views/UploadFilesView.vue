<script setup>
import {onMounted, ref, watch} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {useApiFiles} from '../composables/uploadFiles';
import CircularLoader from '../components/common/CircularLoader.vue';

const props = defineProps({
  typeFile: {
    type: String,
    default: 'image',
    validator: value => ['image', 'video'].includes(value),
  },
})

const inputFile = ref(null);
const formats = ref([]);
const filesSelected = ref([]);
const previewFiles = ref([]);
const isImages = ref(false);

const {uploadFiles, form, isLoading, status} = useApiFiles();

const route = useRoute();
const router = useRouter();

onMounted(() => {
  updateFileTypes(props.typeFile);
});

watch(route, (newVal) => {
  updateFileTypes(newVal.params.typeFile);
});

watch(status, (newVal) => {
  // console.log('status', newVal);
  if (newVal === 'success') {
    // console.log('Wacheando');
    router.push({name: 'predict', params: {'typeFile': props.typeFile}});
  } else if (newVal === 'error') {
    router.push({name: 'upload', params: {'typeFile': props.typeFile}});
  }
});

function updateFileTypes(typeFileVar) {
  previewFiles.value = [];
  filesSelected.value = [];
  if (typeFileVar === 'image') {
    formats.value = ['image/png', 'image/jpeg'];
    isImages.value = true;
  } else if (typeFileVar === 'video') {
    formats.value = ['video/mp4'];
    isImages.value = false;
  }
}


function selectFile(event) {
  // console.log("Selected files", inputFile.value.files);

  filesSelected.value = inputFile.value.files;
  previewFiles.value = [];
  for (const file of filesSelected.value) {
    // console.log("File", file);
    createPreview(file);
  }

  // console.log("Preview images", previewFiles.value);
}

function createPreview(file) {
  const reader = new FileReader();
  reader.onload = (event) => {
    previewFiles.value.push(event.target.result);
  };
  reader.readAsDataURL(file);
}

</script>

<template>
  <h1 class="page-title">{{ isImages ? 'Image selector' : 'Video selector' }}</h1>
  <form class="form" enctype="multipart/form-data" v-on:submit.prevent="uploadFiles" ref="form">
    <div class="form-group">
      <input class="input-file-input" id="file-input" required type="file" name="file" :accept="formats"
             @change="selectFile" ref="inputFile" :multiple="isImages"/>
      <label class="input-file-btn" for="file-input">
        {{ isImages ? '🖼️ Select photos...' : '🎞️ Select video...' }}
      </label>
      <input class="form-upload-btn" type="submit" value="⬆️"/>
    </div>
  </form>
  <div class="files-secction">
    <ul class="files-list">
      <li class="files-item" v-for="(file, index) in filesSelected">

        <img v-if="isImages" :src="previewFiles[index]"/>
        <video v-else :src="previewFiles[index]" controls/>
        <p>{{ file.name }}</p>
      </li>
    </ul>
  </div>

  <circular-loader v-if="isLoading" animation-type="ease-in-out" :speed="1.5"
                   :message="`Uploading ${filesSelected.length} files...`"/>

</template>

<style>
.form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin: 1rem 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-upload-btn {
  background-color: transparent;
  border: none;
  /* padding: 0.5rem; */
  font-size: 2.5rem;
  line-height: 2.5rem;
  cursor: pointer;
  text-align: center;

  transition: text-shadow 0.2s ease-in-out;
}

.form-upload-btn:hover {
  text-shadow: 0px 0px .3rem #2727277a;
}

.input-file-input {
  display: none;
}

.input-file-btn {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 1rem 2rem;
  font-size: 1rem;
  cursor: pointer;
  user-select: none;
  transition: all 0.2s ease-in-out;
}

.input-file-btn:hover {
  background-color: #00a6ed;
  color: #fff;
}

.input-file-btn:active {
  box-shadow: 0 0 0.2rem 0.2rem #ccc;
}

.files-secction {
  margin: 1rem 0;
  display: flex;
  flex-direction: row;
  justify-content: center;
}

.files-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
}

.files-item {
  margin: 0.5rem 0;
  padding: 0.5rem 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #fff;
  transition: box-shadow 0.2s ease-in-out;
  display: flex;
  flex-direction: column;
}

.files-item:hover {
  box-shadow: 0 0 0.2rem 0.2rem #ccc;
}

.files-item img {
  max-height: 200px;
  width: auto;
}
</style>