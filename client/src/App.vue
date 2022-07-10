<script setup>
import { notify } from '@kyvg/vue3-notification';
import { watch } from 'vue';
import NavBar from './components/common/NavBar.vue';

import { useApiStatus } from './composables/apiStatus';

const { apiStatus, apiStatusText } = useApiStatus(10000);

watch(apiStatus, (newStatus) => {
  notify({
    group: 'api-status',
    clear: true,
  })
  if (newStatus) {
    notify({
      group: 'api-status',
      title: 'API status',
      text: apiStatusText.value,
      type: 'success',
    });
  } else {
    notify({
      group: 'api-status',
      title: 'API status',
      text: apiStatusText.value,
      type: 'error',
      duration: -1,
    });
  }
});

</script>

<template>
  <NavBar />
  <div class="container">
    <router-view></router-view>
  </div>
  <notifications group="api-status" position="bottom right" :closeOnClick="false" />
</template>

<style>
:root {
  --color-text-dark: #2c3e50;
  --color-text-light: #fafafa;
  --color-primary: #2c3e50;
  --color-accent: #00a6ed;
  --color-danger: #f55c5c;
  --color-success: #5dee81;
  --color-warning: #ffd700;
  --color-info: #34bcf7;

  --font-primary: Avenir, Helvetica, Arial, sans-serif;
  --font-sencondary: code;
}

* {
  box-sizing: border-box;
}

.shadow-sm {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.2);
}

.shadow-md {
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.2);
}

.shadow-lg {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.2);
}

#app {
  font-family: var(--font-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: var(--color-text-dark);
}

a {
  color: var(--color-accent);
  text-decoration: none;
  border-bottom: 3px solid transparent;
  transition: border 0.2s ease-in-out;
}

a:hover {
  /* text-decoration: underline solid var(--color-accent) 3px; */
  border-bottom: 3px solid var(--color-accent);
}

.btn-primary,
.btn-danger,
.btn-success {
  border: none;
  border-radius: 0.5rem;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: box-shadow 0.2s ease-in-out;
}

.btn-primary {
  background: var(--color-accent);
  color: var(--color-text-light);
}

.btn-primary:hover {
  box-shadow: 0 0 0.5rem rgba(0, 166, 237, 0.80);
}

.btn-danger {
  background: var(--color-danger);
  color: var(--color-text-light);
}

.btn-danger:hover {
  box-shadow: 0 0 0.5rem rgba(245, 92, 92, 0.80);
}

.btn-success {
  background: var(--color-success);
  color: var(--color-text-light);
}

.btn-success:hover {
  box-shadow: 0 0 0.5rem rgba(93, 238, 129, 0.80);
}


.container {
  width: 100%;
  margin: 0 auto;
}

.page-title {
  font-size: 2em;
  margin-bottom: 1em;
}

@media only screen and (min-width: 768px) {
  .container {
    width: 90%;
  }
}

@media only screen and (min-width: 1200px) {
  .container {
    width: 80%;
    max-width: 1200px;
  }
}
</style>
