import {createApp} from "vue";
import {createRouter, createWebHistory} from "vue-router";
import Notifications from "@kyvg/vue3-notification";

import FontAwesomePlugin from "./config/fontAwesome.config";

import App from "./App.vue";
import IndexView from "./views/IndexView.vue";
import UploadFilesView from "./views/UploadFilesView.vue";
import AboutView from "./views/AboutView.vue";
import DetectionView from "./views/DetectionView.vue";
import StreamView from "./views/StreamView.vue";

const routes = [
  {path: "/", component: IndexView},
  {
    path: "/upload/:typeFile",
    name: "upload",
    component: UploadFilesView,
    props: true,
  },
  {
    path: "/predict/:typeFile",
    name: "predict",
    component: DetectionView,
    props: true
  },
  {
    path: "/stream",
    name: "stream",
    component: StreamView,
  },
  {
    path: "/about",
    component: AboutView,
  },
];

const app = createApp(App);

FontAwesomePlugin(app);

app.use(
  createRouter({
    history: createWebHistory(),
    routes,
    linkActiveClass: "active",
    linkExactActiveClass: "exact-active",
  })
);
app.use(Notifications);
app.mount("#app");
