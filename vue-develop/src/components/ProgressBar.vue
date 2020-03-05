<template>
  <div style="width:100%">
    <v-alert v-if="showError" dense outlined type="error">
      {{ showErrorMsg }}
    </v-alert>
    <v-dialog v-model="showProgressbar" persistent width="800">
      <v-card dark>
        <v-card-text>
          Extract Financial Statements
          <v-progress-linear
            v-if="showProgressbar"
            :value="totalProgress"
            height="25"
            striped
          >
            <strong>{{ 'Total ' + Math.ceil(totalProgress) }}%</strong>
          </v-progress-linear>
          <v-progress-linear
            v-if="showProgressbar"
            :value="corpProgress"
            color="light-blue"
            height="25"
            striped
          >
            <strong>{{ barTitle }}%</strong>
          </v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  name: 'ProgressBar',
  data() {
    return {
      showError: false,
      showErrorMsg: '',
      showProgressbar: false,
      totalProgress: 0,
      corpProgress: 0,
      corp: null,
      report_tp: null
    }
  },
  sockets: {
    download(data) {
      const tp = data['type']
      const payload = data['data']
      let corp_name = payload['name']
      let state = payload['state']
      let total = payload['total']
      let index = payload['index']

      let report_tp = payload['report_tp']
      let progress = payload['progress']
      switch (tp) {
        case 'total':
          if (payload === 'start') {
            this.showError = false
            this.showProgressbar = true
          } else {
            this.showProgressbar = false
          }
          break
        case 'error':
          this.showError = true
          this.showErrorMsg = payload
          break
        case 'download':
          this.showProgressbar = true
          if (state === 'start') {
            this.corpProgress = 0
            this.totalProgress = ((index - 1) / total) * 100
          } else {
            this.corpProgress = 100
            this.totalProgress = (index / total) * 100
          }
          this.corp_name = corp_name
          break
        case 'progress':
          this.showProgressbar = true
          this.corp_name = corp_name
          this.corpProgress = progress
          this.report_tp = report_tp
          break
        default:
          break
      }
    }
  },
  computed: {
    barTitle() {
      if (this.corp_name !== null) {
        return `${this.corp_name}(${this.report_tp}) : ${Math.ceil(
          this.corpProgress
        )}`
      } else {
        return ``
      }
    }
  }
}
</script>

<style scoped></style>
