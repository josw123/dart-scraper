<template>
  <v-autocomplete
    ref="cpAutocomplete"
    v-model="cpList"
    :items="companyItems"
    :rules="[cpRules.required]"
    :search-input.sync="search"
    :loading="loading"
    :disabled="apiKey === null"
    label="Company Name"
    item-text="corp_name"
    item-value="corp_code"
    clearable
    chips
    no-filter
    return-object
    required
    multiple
  />
</template>

<script>
const CORP_LIST = 'CORP_LIST'
export default {
  sockets: {
    [CORP_LIST]({type, data}) {
      switch(type.toLowerCase()) {
        case 'loading':
          if (data.toLowerCase() === 'start') {
            this.loading = true
          } else {
            this.loading = false
          }
          break
        case 'data':
          this.companyItems = [...this.cpList, ...data]
          break
        default:
          break
      }

    },
  },
  data() {
    return {
      loading: false,
      search: '',
      companyItems: null,
      cpList: [],
      cpRules: {
        required: value => value.length !== 0 || 'Required.'
      },
      timer: null
    }
  },
  methods: {
    requestList() {
      if (this.search.length > 1) {
        const payload = { corp_name: this.search}
        this.$socket.emit(CORP_LIST, payload)
      }
    }
  },
  computed:{
    apiKey(){
      return this.$store.state.apiKey
    }
  },
  watch: {
    search(newValue) {
      if (newValue && newValue.length > 1) {
        if (this.timer !== null) {
          clearTimeout(this.timer)  
          this.timer = null 
        }
        this.timer = setTimeout(this.requestList, 200)
      }
    },
    cpList(newValue){
      this.$store.commit('setCorps', newValue)
    }
  }
}
</script>

<style>
</style>