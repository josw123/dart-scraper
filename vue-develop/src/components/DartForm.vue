<template>
  <v-container fluid>
    <v-form
      ref="form"
      v-model="valid"
      lazy-validation
      >
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
            <v-text-field
                    v-model="apikey"
                    :append-icon="apiKeyShow ? 'mdi-eye' : 'mdi-eye-off'"
                    :rules="[apikeyRules.required, apikeyRules.min]"
                    :type="apiKeyShow ? 'text' : 'password'"
                    name="input"
                    label="DART API KEY"
                    hint="40 characters"
                    counter
                    @click:append="apiKeyShow = !apiKeyShow"
                    required
            ></v-text-field>
            <v-autocomplete
                    ref="cpAutocomplete"
                    v-model="cpList"
                    :items="companyItems"
                    :rules="[cpRules.required]"
                    :filter="customFilter"
                    label="Company Name or Code"
                    item-text="name"
                    chips
                    multiple
                    required
            ></v-autocomplete>
            <v-select
                    v-model="cpTpList"
                    :items="cpTpItems"
                    :rules="[cpTpRules.required]"
                    chips
                    label="Report Types"
                    multiple
                    required
            ></v-select>
            <v-select
                    v-model="reportTpList"
                    :items="reportTpItems"
                    attach
                    chips
                    label="Reporting Period"
                    required
            ></v-select>
            <v-row>
              <v-col cols="6">
                <v-menu
                        ref="startdtMenu"
                        v-model="startdtMenu"
                        :close-on-content-click="false"
                        :return-value.sync="startdt"
                        transition="scale-transition"
                        offset-y
                        min-width="290px"
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                            v-model="startdt"
                            label="Start Date"
                            v-on="on"
                            readonly
                    ></v-text-field>
                  </template>
                  <v-date-picker v-model="startdt" no-title scrollable>
                    <v-spacer></v-spacer>
                    <v-btn text color="primary" @click="startdtMenu = false">Cancel</v-btn>
                    <v-btn text color="primary" @click="$refs.startdtMenu.save(startdt)">OK</v-btn>
                  </v-date-picker>
                </v-menu>
              </v-col>
              <v-col cols="6">
                <v-menu
                        ref="endMenu"
                        v-model="endMenu"
                        :close-on-content-click="false"
                        :return-value.sync="enddt"
                        transition="scale-transition"
                        offset-y
                        min-width="290px"
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                            v-model="enddt"
                            label="End Date"
                            v-on="on"
                            readonly
                    ></v-text-field>
                  </template>
                  <v-date-picker v-model="enddt" no-title scrollable>
                    <v-spacer></v-spacer>
                    <v-btn text color="primary" @click="endMenu = false">Cancel</v-btn>
                    <v-btn text color="primary" @click="$refs.endMenu.save(enddt)">OK</v-btn>
                  </v-date-picker>
                </v-menu>
              </v-col>
            </v-row>
            <v-text-field
                    v-model="folder"
                    :rules="[folderRules.required]"
                    label="Download Folder"
                    required
            ></v-text-field>
          </v-card-text>
          <v-alert
                  v-if="showError"
                  dense
                  outlined
                  type="error"
          >
            {{showErrorMsg}}
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
import axios from 'axios';
var url_base = window.location.href;
export default {
  name: 'HelloWorld',

  data: () => {
    return {
      valid: false,
      apiKeyShow: false,
      apikey: '',
      apikeyRules: {
        required: value => !!value || 'Required.',
        min: v => v.length === 40 || '40 characters',
      },
      companyItems: null,
      cpList: [],
      cpRules: {
        required: value => value.length !== 0 || 'Required.'
      },
      cpTpItems: ['Consolidated', 'Separate'],
      cpTpList: ['Consolidated'],
      cpTpRules: {
        required: value => value.length !== 0 || 'Required.'
      },
      reportTpItems: ['Annual', 'Half', 'Quarter'],
      reportTpList: 'Annual',

      startdtMenu: false,
      startdt: new Date('2012-01-01').toISOString().substr(0, 10),

      endMenu: false,
      enddt: new Date().toISOString().substr(0, 10),

      folder: '',
      folderRules: {
        required: value => !!value || 'Required.'
      },
      showError: false,
      showErrorMsg: '',
      showProgressbar: false,
      progressbarValue: 0.0,
      downloadIndex: -1,
      downloadTotal: 0,
      downloadList: [],
  }},
  methods: {
    customFilter (item, queryText) {
      const textOne = item.name.toLowerCase()
      const textTwo = item.code.toLowerCase()
      const searchText = queryText.toLowerCase()
      return textOne.indexOf(searchText) > -1 ||
              textTwo.indexOf(searchText) > -1
    },
    submit() {
      if (this.$refs.form.validate()) {

        let body = {
          'api_key': this.apikey
        };

        axios.post(url_base + 'apikey', body).then(res => {
          let data = res.data
          if ((data['ret_code'] !== 'success')) {
            this.apikey = '';
            this.showError = true;
            this.showErrorMsg = 'The provided API key is invalid.'
            this.showProgressbar = false
          } else {
            this.showError = false;
            this.showErrorMsg = ''
            this.showProgressbar=true

            this.downloadTotal = this.cpList.length * this.cpTpList.length

            this.progressbarValue = this.downloadIndex / this.downloadTotal

            let startdt = this.startdt.replace(/-/g,'')
            let enddt = this.enddt.replace(/-/g,'')

            let cpList = this.companyItems.filter(e => {
              if (this.cpList.includes(e['name'])){
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
                  'api_key': this.apikey,
                  'crp_cd': cpList[idx]['code'],
                  'start_dt': startdt,
                  'end_dt': enddt,
                  'report_tp': this.reportTpList,
                  'separate': separate,
                };
                this.downloadList.push(body)
              }
            }
            this.downloadIndex = 0
          }
        }).catch(() => {
          this.showError = true;
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
      this.progressbarValue = newValue / this.downloadTotal * 100
    }
  }
};
</script>
<style scoped>
</style>