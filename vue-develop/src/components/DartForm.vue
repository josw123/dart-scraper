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
              />
            </v-flex>
            <v-card-text>
              <APIKey />
              <Company />
              <Separate />
              <ReportTp />
              <Date />
              <Directory />
            </v-card-text>
            <ProgressBar />
            <v-divider class="mt-12" />
            <v-card-actions>
              <v-spacer />
              <v-btn color="primary" text @click="submit">Download</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
import APIKey from './APIKey'
import Separate from './Separate'
import ReportTp from './ReportTp'
import Date from './Date'
import Company from './Company'
import Directory from './Directory'
import ProgressBar from './ProgressBar'

export default {
  name: 'DartScraper',
  components: {
    APIKey,
    Separate,
    ReportTp,
    Date,
    Company,
    Directory,
    ProgressBar,
  },
  data: () => {
    return {
      valid: false,
    }
  },
  methods: {
    submit() {
      if (this.$refs.form.validate()) {
        const payload = {
          api_key: this.$store.state.api_key,
          bgn_de: this.$store.state.bgn_de,
          corps: this.$store.state.corps.map(v => v.corp_code),
          path: this.$store.state.base_path,
          separate: this.$store.state.separate,
          report_tp: this.$store.state.report_tp
        }
        this.$socket.emit('download', payload)
      }
    }
  },
}
</script>