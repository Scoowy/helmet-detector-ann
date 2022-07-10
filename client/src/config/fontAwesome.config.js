import { library } from "@fortawesome/fontawesome-svg-core";

import {
  faVolumeMute,
  faVolumeDown,
  faVolumeHigh,
  faVolumeXmark,
  faVolumeOff,
  faDownload,
  faCamera,
  faVideo,
  faVideoCamera,
  faMicrophone,
  faMicrophoneSlash,
} from "@fortawesome/free-solid-svg-icons";
import {
  faCirclePlay,
  faCircleStop,
  faCirclePause,
  faCircleXmark,
  faCircleDot,
  faCircleDown,
  faTrashCan,
  faFloppyDisk,
  faEyeSlash,
} from "@fortawesome/free-regular-svg-icons";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

library.add(
  faVolumeMute,
  faVolumeDown,
  faVolumeHigh,
  faVolumeXmark,
  faVolumeOff,
  faDownload,
  faCamera,
  faVideo,
  faVideoCamera,
  faMicrophone,
  faMicrophoneSlash,
  faCirclePlay,
  faCircleStop,
  faCirclePause,
  faCircleXmark,
  faCircleDot,
  faCircleDown,
  faTrashCan,
  faFloppyDisk,
  faEyeSlash
);

export default function (app) {
  app.component("fa-icon", FontAwesomeIcon);
}
