// eslint-disable-next-line no-unused-vars
import axios, { AxiosRequestConfig } from "axios";

/**
 * @param {AxiosRequestConfig} config
 * @returns {Promise<T>}
 */
export async function request(config) {
  return (
    axios
      .request(config)
      .then(({ data }) => data)
      .catch(({ response }) => response.data)
  );
}

/**
 * @param {String} url
 * @param {AxiosRequestConfig} config
 * @returns {Promise<T>}
 */
export async function get(url, config = {}) {
  return request({ url, method: "GET", ...config });
}

/**
 * @param {String} url
 * @param data
 * @param {AxiosRequestConfig} config
 * @returns {Promise<T>}
 */
export async function post(url, data = undefined, config = {}) {
  return request({
    url,
    data,
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    ...config,
  });
}
