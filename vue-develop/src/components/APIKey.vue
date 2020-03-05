<template>
  <v-text-field
    v-model="apikey"
    :append-icon="apiKeyShow ? 'mdi-eye' : 'mdi-eye-off'"
    :rules="[apikeyRules.required]"
    :type="apiKeyShow ? 'text' : 'password'"
    name="input"
    label="DART API KEY"
    hint="40 characters"
    counter
    @click:append="apiKeyShow = !apiKeyShow"
    required
  />
</template>

<script>
export default {
  beforeCreate() {
    this.$store.dispatch('getAPIKey')
  },
  data() {
    return {
      apikey: null,
      apiKeyShow: false,
      apikeyRules: {
        required: value => !!value || 'Required.'
      },
    }
  },
  computed: {
    dart_api_key() {
      return this.$store.state.api_key
    }
  },
  watch: {
    dart_api_key(newValue) {
      if (newValue !== null) {
        this.apikey = newValue
      }
    },
    apikey(newValue) {
      if (this.dart_api_key !== newValue) {
        this.$store.commit('setAPIKey', newValue)
      }
    }
  }
}
</script>
