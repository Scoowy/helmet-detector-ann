import { onMounted, onUnmounted, ref } from "vue";

export function useApiStatus(interval = 5000, timeout = 3000) {
  const apiStatus = ref(false);
  const apiStatusText = ref("");
  const intervalId = ref(0);

  const fetchApiStatus = async () => {
    let response = null;
    // Borrar
    const controller = new AbortController();
    const id = setTimeout(() => {
      apiStatus.value = false;
      apiStatusText.value = "API is down";
      controller.abort();
    }, timeout);
    // Borrar
    try {
      response = await fetch("http://localhost:8000/ping", {
        signal: controller.signal,
      });
      clearTimeout(id);
      if (response.status === 200) {
        apiStatus.value = true;
        apiStatusText.value = "API is running";
      }
    } catch (error) {
      apiStatus.value = false;
      apiStatusText.value = "API is not running for:\n" + error.message;
    }
  };

  onMounted(async () => {
    await fetchApiStatus();
    intervalId.value = setInterval(() => {
      fetchApiStatus();
    }, interval);
  });

  onUnmounted(() => {
    clearInterval(intervalId.value);
  });

  return { apiStatus, apiStatusText };
}
