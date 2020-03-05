<template>
  <v-select
    v-model="separate"
    :items="items"
    :rules="[rules.required]"
    chips
    label="Report Types"
    required
  />
</template>

<script>
export default {
  beforeMount() {
      this.separate = 'Consolidated'
  },
  data() {
    return {
      items: ['Consolidated', 'Separate'],
      separate: null,
      rules: {
        required: value => value.length !== 0 || 'Required.'
      }
    }
  },
  watch: {
    separate(newValue) {
      const separate = newValue === 'Separate'
      this.$store.commit('setSeparate', separate)
    }
  }
}
</script>
