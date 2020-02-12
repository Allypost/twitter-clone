import { postFile } from "@/helpers/axios";

const FILE_BASE = "/api/file";

const state = {};

const getters = {};

const mutations = {};

const actions = {

  async upload(_, {
    file,
    name = "file",
    onProgress = () => 1,
  }) {
    const { success, data, errors } = await postFile(
      `${ FILE_BASE }/upload`,
      name,
      file,
      {
        onUploadProgress: onProgress,
      },
    );

    if (!success) {
      return { data: null, error: errors.join(" ") };
    }

    return { data, error: "" };
  },

};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
