import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  timeout: 60000,
});

export async function verifyClaim(claim) {
  if (!claim || !claim.trim()) {
    throw new Error("Please enter a claim to verify.");
  }

  try {
    const response = await api.post("/verify", { claim: claim.trim() });
    if (!response?.data) {
      throw new Error("The verification service returned an empty response.");
    }

    return response.data;
  } catch (error) {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      "Unable to reach the verification service.";

    throw new Error(message, { cause: error });
  }
}

export default api; 