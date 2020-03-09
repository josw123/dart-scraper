<template>
  <v-text-field
    v-model="apiKey"
    :append-icon="apiKeyShow ? 'mdi-eye' : 'mdi-eye-off'"
    :rules="[apiKeyRules.required]"
    :type="apiKeyShow ? 'text' : 'password'"
    name="input"
    label="DART API KEY"
    hint="40 characters"
    counter
    @click:append="apiKeyShow = !apiKeyShow"
    @keydown.enter="setAPIKey"
    @blur="setAPIKey"
    required
  />
</template>

<script>
const DART_API_KEY = 'DART_API_KEY'
export default {
  sockets: {
    [DART_API_KEY]({data}){
      this.setLocalAPIKey(data.DART_API_KEY)
    }
  },
  beforeCreate() {
    const payload = {
      type: 'GET'
    }
    this.$socket.emit(DART_API_KEY, payload)
  },
  data() {
    return {
      apiKey: null,
      apiKeyShow: false,
      apiKeyRules: {
        required: value => !!value || 'Required.'
      },
    }
  },
  methods: {
    setAPIKey() {
      if (this.apiKey && this.apiKey.length > 0) {
        const payload = {
          type: 'SET',
          DART_API_KEY: this.apiKey,
        }
        this.$socket.emit(DART_API_KEY, payload)
      }
    },
    setLocalAPIKey(apiKey) {
      this.apiKey = apiKey
      this.$store.commit('setAPIKey', apiKey)
    }
  }
}
</script>
