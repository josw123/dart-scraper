<template>
  <v-container fluid>
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-row justify="center">
        <v-col cols="12" sm="10" md="10" lg="10">
          <v-card ref="form">
            <v-flex xs12>
              <v-img
                :src="require('../assets/logo.png')"
                class="my-3"
                contain
                height="300"
              ></v-img>
            </v-flex>
            <v-card-text>
              <APIKey />
              <Company />
              <Separate />
              <ReportTp />
              <Date />
      
              <Directory />
            </v-card-text>
            <v-alert v-if="showError" dense outlined type="error">
              {{ showErrorMsg }}
            </v-alert>
            <v-progress-linear
              v-if="showProgressbar"
              :value="progressbarValue"
              height="25"
              striped
            >
              <strong>{{ Math.ceil(progressbarValue) }}%</strong>
            </v-progress-linear>
            <v-divider class="mt-12"></v-divider>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" text @click="submit">Download</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
import axios from 'axios'
import APIKey from './APIKey'
import Separate from './Separate'
import ReportTp from './ReportTp'
import Date from './Date'
import Company from './Company'
import Directory from './Directory'

var url_base = window.location.href
export default {
  name: 'DartScraper',
  components: {
    APIKey,
    Separate,
    ReportTp,
    Date,
    Company,
    Directory,
  },
  data: () => {
    return {
      valid: false,
      showError: false,
      showErrorMsg: '',
      showProgressbar: false,
      progressbarValue: 0.0,
      downloadIndex: -1,
      downloadTotal: 0,
      downloadList: []
    }
  },
  methods: {
    customFilter(item, queryText) {
      const textOne = item.name.toLowerCase()
      const textTwo = item.code.toLowerCase()
      const searchText = queryText.toLowerCase()
      return (
        textOne.indexOf(searchText) > -1 || textTwo.indexOf(searchText) > -1
      )
    },
    submit() {
      if (this.$refs.form.validate()) {
        let body = {
          api_key: this.apikey
        }

        axios
          .post(url_base + 'apikey', body)
          .then(res => {
            let data = res.data
            if (data['ret_code'] !== 'success') {
              this.apikey = ''
              this.showError = true
              this.showErrorMsg = 'The provided API key is invalid.'
              this.showProgressbar = false
            } else {
              this.showError = false
              this.showErrorMsg = ''
              this.showProgressbar = true

              this.downloadTotal = this.cpList.length * this.cpTpList.length

              this.progressbarValue = this.downloadIndex / this.downloadTotal

              let startdt = this.startdt.replace(/-/g, '')
              let enddt = this.enddt.replace(/-/g, '')

              let cpList = this.companyItems.filter(e => {
                if (this.cpList.includes(e['name'])) {
                  return true
                }
                return false
              })

              for (let idx in cpList) {
                for (let jdx in this.cpTpList) {
                  var separate = false
                  if (this.cpTpList[jdx] === 'Separate') {
                    separate = true
                  }

                  let body = {
                    api_key: this.apikey,
                    crp_cd: cpList[idx]['code'],
                    start_dt: startdt,
                    end_dt: enddt,
                    report_tp: this.reportTpList,
                    separate: separate,
                    path: this.folder
                  }
                  this.downloadList.push(body)
                }
              }
              this.downloadIndex = 0
            }
          })
          .catch(() => {
            this.showError = true
            this.showErrorMsg = 'Server is not responding.'
            this.showProgressbar = false
          })
      }
    }
  },
  mounted() {
    let url = url_base + 'company'
    axios.get(url).then(res => {
      this.companyItems = res.data['crp_list']
    })

    url = url_base + 'apikey'
    axios.get(url).then(res => {
      this.apikey = res.data['api_key']
    })

    url = url_base + 'path'
    axios.get(url).then(res => {
      this.folder = res.data['path']
    })
  },
  watch: {
    downloadIndex: function(newValue, oldValaue) {
      if (newValue !== oldValaue) {
        if (newValue < this.downloadTotal) {
          let body = this.downloadList[newValue]
          axios.post(url_base + 'download', body).then(res => {
            let data = res.data
            if (data['ret_code'] === 'success') {
              this.downloadIndex = this.downloadIndex + 1
            }
          })
        }
      }
      this.progressbarValue = (newValue / this.downloadTotal) * 100
    }
  }
}
</script>
<style scoped></style>
