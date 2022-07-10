import {ref} from "vue";

export function useDetectApi() {
  const response = ref(null);
  const isLoading = ref(false);
  const hasError = ref(false);

  const detectHelmets = async (fileType = 'images') => {
    isLoading.value = true;
    try {
      const res = await fetch(`http://localhost:8000/api/v1/predict/${fileType}`);
      const data = await res.json();
      isLoading.value = false;
      response.value = data;
    } catch (error) {
      hasError.value = true;
      isLoading.value = false;
    }
  };

  return {response, isLoading, hasError, detectHelmets};
}
