<script setup>
import { ref, reactive } from 'vue';

const links = reactive([
  {
    name: 'Home',
    path: '/',
    active: true,
  },
  {
    name: 'Predict',
    path: '/upload',
    active: false,
    subroutes: [
      {
        name: 'Images',
        path: '/upload/image',
        active: false,
      },
      {
        name: 'Video',
        path: '/upload/video',
        active: false,
      },
      {
        name: 'Camera',
        path: '/stream',
        active: false,
      },
    ],
  },
  {
    name: 'About',
    path: '/about',
    active: false,
  },
]);
</script>

<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <a class="navbar-title" href="/">IA Project</a>
    </div>

    <div class="navbar-menu">
      <ul class="navbar-nav">
        <li v-for="link in links" class="nav-item">
          <button v-if="link.subroutes" class="dropdownBtn">{{ link.name }}</button>
          <ul v-if="link.subroutes" class="navbar-submenu">
            <li v-for="sublink in link.subroutes" class="nav-item">
              <router-link class="nav-link" :to="sublink.path">{{ sublink.name }}</router-link>
            </li>
          </ul>
          <router-link v-else class="nav-link" :to="link.path">{{ link.name }}</router-link>
        </li>
      </ul>
    </div>
  </nav>
</template>

<style>
.navbar {
  min-height: 2rem;
  display: flex;
  justify-content: space-between;
  padding: 0 5rem;
  margin: 2rem 0;
}

.navbar-brand {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 2rem;
}

.navbar-menu {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  height: 2rem;
}

.navbar-title {
  font-size: 2rem;
  line-height: 2rem;
  font-weight: bold;
  color: #2c3e50;
  text-decoration: none;
}

.navbar-nav {
  height: 2rem;
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  align-items: center;
  list-style: none;
}

.nav-item {
  color: #2c3e50;
  position: relative;
}

.nav-link,
.dropdownBtn {
  color: #2c3e50;
  text-decoration: none;
  padding: 0 1rem;
  font-size: 1rem;
  line-height: 2rem;
  font-weight: bold;
  border: none;
  background-color: transparent;
  cursor: pointer;
  transition: color 0.2s ease-in-out;
}


.nav-link:hover,
.dropdownBtn:hover {
  color: #00a6ed;
  border: none;
}

.nav-link.active {
  text-decoration: underline solid #00a6ed 3px;
}

.navbar-submenu {
  display: none;
  position: absolute;
  padding: 1rem .5rem;
  row-gap: .5rem;
  background-color: #fff;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.2);
  list-style: none;
  top: 0;
  left: calc(50% - 60%);
  margin-top: 2.5rem;
  z-index: 1;
}

.navbar-submenu::before {
  content: '';
  position: absolute;
  top: -0.5rem;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-bottom: .5rem solid #00a6ed;
  border-left: .5rem solid transparent;
  border-right: .5rem solid transparent;
  border-top: 0;
  padding: auto;
}

.nav-item:hover .navbar-submenu,
.navbar-submenu:hover,
.navbar-submenu:hover::before {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>