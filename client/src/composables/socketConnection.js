import { ref } from "vue";
import { io } from "socket.io-client";

export function useSocketConnection(url = "http://localhost:8000") {
  const socket = ref(null);
  const isConnected = ref(false);
  const isLoading = ref(false);
  const hasError = ref(false);

  const connect = async () => {
    isLoading.value = true;
    try {
      socket.value = io(url, { transports: ["websocket"] });
      isConnected.value = true;
      isLoading.value = false;
    } catch (error) {
      hasError.value = true;
      isLoading.value = false;
    }
  };

  const disconnect = async () => {
    isLoading.value = true;
    try {
      socket.value.close();
      isConnected.value = false;
      isLoading.value = false;
    } catch (error) {
      hasError.value = true;
      isLoading.value = false;
    }
  };

  const send = async (data) => {
    isLoading.value = true;
    try {
      socket.value.emit("message", data);
      isLoading.value = false;
    } catch (error) {
      hasError.value = true;
      isLoading.value = false;
    }
  };

  const on = async (event, callback) => {
    isLoading.value = true;
    try {
      socket.value.on(event, callback);
      isLoading.value = false;
    } catch (error) {
      hasError.value = true;
      isLoading.value = false;
    }
  };

  const predict = async (data) => {
    isLoading.value = true;
    try {
      socket.value.emit("predict", data);
      isLoading.value = false;
    } catch (error) {
      hasError.value = true;
      isLoading.value = false;
    }
  };

  const emitCustomEvent = async (eventName, data=null) => {
    isLoading.value = true;
    try {
      if (data != null) {
        socket.value.emit(eventName, data);
      } else {
        socket.value.emit(eventName);
      }
      isLoading.value = false;
    } catch (error) {
      hasError.value = true;
      isLoading.value = false;
    }
  };

  return {
    socket,
    isConnected,
    isLoading,
    hasError,
    predict,
    connect,
    disconnect,
    send,
    on,
    emitCustomEvent,
  };
}
