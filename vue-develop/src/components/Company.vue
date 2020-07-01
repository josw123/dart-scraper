<template>
  <div style="text-align: center">
    <v-btn-toggle
        v-model="market"
        multiple
    >
      <v-btn width="120px">
        코스피
      </v-btn>
      <v-btn width="120px">
        코스닥
      </v-btn>
      <v-btn width="120px">
        코넥스
      </v-btn>
      <v-btn width="120px">
        기타
      </v-btn>
    </v-btn-toggle>
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

  </div>
</template>

<script>
const CORP_LIST = 'CORP_LIST'
export default {
  sockets: {
    [CORP_LIST]({type, data}) {
      switch(type.toLowerCase()) {
        case 'loading':
          this.loading = data.toLowerCase() === 'start';
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
      market:[0, 1,],
      timer: null
    }
  },
  methods: {
    requestList() {
      if (this.search.length > 1) {
        const market = this.market.map(v => {
          const string = 'YKNE'
          return string[v]
        }).join('')


        const payload = { corp_name: this.search, market: market}
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