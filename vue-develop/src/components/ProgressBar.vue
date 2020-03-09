<template>
  <div style="width:100%">
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
  const DOWNLOAD = 'DOWNLOAD'
export default {
  name: 'ProgressBar',
  data() {
    return {
      showProgressbar: false,
      totalProgress: 0,
      corpProgress: 0,
      corp_name: null,
      report_tp: null
    }
  },
  methods: {
    hideProgressBar() {
      this.showProgressbar = false
    }
  },
  sockets: {
    [DOWNLOAD]({type, data}) {
      const {progress, corp_name, total, index, report_tp} = data
      switch(type) {
        case 'loading':
          if (data === 'start') {
            this.showError = false
            this.showProgressbar = true
          } else {
            this.totalProgress = 100
            setTimeout(this.hideProgressBar, 3000)
          }
          break
        case 'data':
          this.showProgressbar = true
          this.totalProgress = ((index) / total) * 100
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