// eslint-disable-next-line no-unused-vars
import axios, { AxiosRequestConfig } from "axios";

/**
 * @typedef {Object} ApiResponse
 * @property {Boolean} success
 * @property data
 * @property {Array} errors
 */

/**
 * @param {AxiosRequestConfig} config
 * @returns {Promise<ApiResponse>}
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
 * @returns {Promise<ApiResponse>}
 */
export async function get(url, config = {}) {
  return request({ url, method: "GET", ...config });
}

/**
 * @param {String} url
 * @param data
 * @param {AxiosRequestConfig} config
 * @returns {Promise<ApiResponse>}
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

/**
 * @param {String} url
 * @param {AxiosRequestConfig} config
 * @returns {Promise<ApiResponse>}
 */
export async function del(url, config = {}) {
  return request({
    url,
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    config,
  });
}
