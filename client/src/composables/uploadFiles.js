import { ref } from "vue";

export function useApiFiles() {
  const status = ref("not-started");
  const form = ref(null);
  const response = ref(null);
  const isLoading = ref(false);

  const uploadFiles = async () => {
    const formData = new FormData(form.value);
    status.value = "pending";
    isLoading.value = true;
    try {
      const res = await makeRequest(
        "POST",
        "http://localhost:8000/api/v1/files/upload",
        formData
      );
      response.value = res;
      status.value = "success";
      isLoading.value = false;
    } catch (error) {
      isLoading.value = false;
      status.value = "error";
    }
  };

  const makeRequest = (method, url, data) => {
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      xhr.open(method, url, true);
      xhr.onload = () => {
        if (xhr.status === 200) {
          resolve(xhr.response);
        } else {
          reject(xhr.statusText);
        }
      };
      xhr.onerror = () => {
        reject(xhr.statusText);
      };
      xhr.send(data);
    });
  };

  return { uploadFiles, status, form, response, isLoading };
}
