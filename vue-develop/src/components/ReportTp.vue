<template>
  <v-select
    v-model="report_tp"
    :items="items"
    :attach="true"
    chips
    label="Reporting Period"
    required
  />
</template>

<script>
export default {
  beforeMount() {
    this.report_tp = 'Annual'
  },
  data() {
    return {
      items: ['Annual', 'Half', 'Quarter'],
      report_tp: null
    }
  },
  watch: {
    report_tp(newValue) {
      this.$store.commit('setReportTp', newValue)
    }
  }
}
</script>

<style></style>
