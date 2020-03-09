import Vue from 'vue';
import Vuex from 'vuex';
import { request } from '../utils/requests'

Vue.use(Vuex);

const base = window.location.href
//const base = 'http://localhost:5000/'
export {base}


const state = {
  github_version: null,
  version: null,
  apiKey: null,
  bgn_de: '',
  end_de: '',
  corps: [],
  separate: false,
  report_tp: 'Annual',
  base_path: null,
}

const getters = {}

const mutations = {
  setGithubVersion(state, version) {
    state.github_version = version
  },
  setVersion(state, version) {
    state.version = version
  },
  setAPIKey(state, apiKey) {
    state.apiKey = apiKey
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
  setSeparate(state, separate) {
    state.separate = separate
  },
  setReportTp(state, report_tp) {
    state.report_tp = report_tp
  },
  setBasePath(state, base_path) {
    state.base_path = base_path
  },
}

const actions = {
  async getGithubVersion({ commit }) {
    const github = 'https://api.github.com'
    const github_path = '/repos/josw123/dart-scraper/releases/latest'
    const github_recv = await request.get(github, github_path)
    commit('setGithubVersion', github_recv.data['tag_name'])
  }
}

const store = new Vuex.Store({
  state: state,
  getters: getters,
  mutations: mutations,
  actions: actions
})

export default store;