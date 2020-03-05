import Vue from 'vue';
import Vuex from 'vuex';
import { request } from '../utils/requests'

Vue.use(Vuex);

//const base = window.location.href
const base = 'http://localhost:5000'

const state = {
  github_version: null,
  version: null,
  api_key: null,
  bgn_de: '',
  end_de: '',
  corps: [],
  path: '',
  separate: false,
  report_tp: 'Annual',
  base_path: null,
  base_path_error: false,
  subdir: [],
}

const getters = {}

const mutations = {
  setGithubVersion(state, version) {
    state.github_version = version
  },
  setVersion(state, version) {
    state.version = version
  },
  setAPIKey(state, api_key) {
    state.api_key = api_key
  },
  setBgnDe(state, bgn_de) {
    state.bgn_de = bgn_de
  },
  setEndDe(state, end_de) {
    state.end_de = end_de
  },
  setCorps(state, corps) {
    state.corps = [...corps]
  }, 
  setPath(state, path) {
    state.path = path
  },
  setSeparate(state, separate) {
    state.separate = separate
  },
  setReportTp(state, report_tp) {
    state.report_tp = report_tp
  },
  setBasePath(state, base_path) {
    state.base_path = base_path
  },
  setSubDir(state, subdir) {
    state.subdir = [...subdir]
  },
  setBasePathError(state, ret_code) {
    state.base_path_error = ret_code
  }
}

const actions = {
  async getGithubVersion({ commit }) {
    const github = 'https://api.github.com'
    const github_path = '/repos/josw123/dart-scraper/releases/latest'
    const github_recv = await request.get(github, github_path)
    commit('setGithubVersion', github_recv.data['tag_name'])
  },
  async getVersion({ commit }) {
    const path = '/version'
    const recv = await request.get(base, path)
    commit('setVersion', recv.data.version)
  },
  async getAPIKey({ commit }) {
    const path = '/key'
    const recv = await request.get(base, path)
    commit('setAPIKey', recv.data['api_key'])
  },
  async setAPIKey({ commit }, api_key) {
    const path = '/key'
    const data = {api_key: api_key}
    const recv = await request.post(base, path, data)
    if (recv.data.ret_code === 'success') {
      commit('setAPIKey', api_key)
    } else {
      commit('setAPIKey', null)
    }
  },
  async getDirectory({commit}, payload) {
    let data = {}
    if (payload !== undefined) {
      const {base_path, new_path} = payload
      data['base_path'] = base_path
      data['new_path'] = new_path
    }
    const path = '/dir'
    const recv = await request.post(base, path, data)
    if (recv.data['ret_code'] === 'success') {
      console.log("success")
      commit('setBasePath', recv.data['base_path'])
      commit('setSubDir', recv.data['subdir'])
      commit('setBasePathError', false)
    } else {
      commit('setBasePathError', true)
    }
  }
}

const store = new Vuex.Store({
  state: state,
  getters: getters,
  mutations: mutations,
  actions: actions
})

export default store;