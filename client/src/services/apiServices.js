import Cookies from "js-cookie";

const API_BASE = import.meta.env.VITE_BACKEND_BASE_URL;
export const getToken = () => Cookies.get("access_token");
export const setToken = (accessToken, refreshToken) => {
  Cookies.set("access_token", accessToken);
  Cookies.set("refresh_token", refreshToken);
};
export const removeToken = () => {
  Cookies.remove("access_token");
  // Cookies.remove("refresh_token");
};

export const login = async (username, password) => {
  const res = await fetch(`${API_BASE}${import.meta.env.VITE_LOGIN_URL}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) throw new Error("Login failed");
  const data = await res.json();
  setToken(data.access, data.refresh);
  return data;
};

export const fetchWithAuth = async (url, options = {}) => {
  const token = getToken();
  // console.log("token", token);
  const headers = {
    ...(options.headers || {}),
    Authorization: token ? `Bearer ${token}` : undefined,
  };
  const opts = { ...options, headers };
  console.log("opts", opts);
  let res = await fetch(url, opts);

  if (res.status === 401) {
    const refreshToken = Cookies.get("refresh_token");
    console.log("refreshToken", refreshToken);
    if (refreshToken) {
      const refreshRes = await fetch(`${API_BASE}${import.meta.env.VITE_REFRESH_TOKEN_URL}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh: refreshToken }),
      });
      console.log("refreshRes", refreshRes);
      if (refreshRes.status===200) {
        const refreshData = await refreshRes.json();
        console.log("refreshData", refreshData);
        setToken(refreshData.access);
        headers.Authorization = `Bearer ${refreshData.access}`;
        res = await fetch(url, { ...options, headers });
      }
      // else {
      //   removeToken();
      //   Cookies.remove("refresh_token");
      //   window.location.href = `${import.meta.env.VITE_LOGIN_URL}`;
      //   throw new Error("Unauthorized");
      // }
    } 
    // else {
    //   removeToken();
    //   window.location.href = `${import.meta.env.VITE_LOGIN_URL}`;
    //   throw new Error("Unauthorized");
    // }
  }

  return res;
};

export const uploadFile = async (formData) => {
  return fetchWithAuth(`${API_BASE}/upload_file/`, {
    method: "POST",
    body: formData,
  });
};

export const processQuery = async (formData) => {
  return fetchWithAuth(`${API_BASE}/test_url/`, {
    method: "POST",
    body: formData,
  });
};

export const listDatasets = async () => {
  const res = await fetchWithAuth(`${API_BASE}/datasets/`);
  return res.json();
};

export const setDataset = async (fileName) => {
  const res = await fetchWithAuth(`${API_BASE}/set_datasets/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ file_name: fileName }),
  });
  return res.json();
}; 