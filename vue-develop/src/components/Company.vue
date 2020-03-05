<template>
  <v-autocomplete
    ref="cpAutocomplete"
    v-model="cpList"
    :items="companyItems"
    :rules="[cpRules.required]"
    label="Company Name or Code"
    item-text="name"
    chips
    no-filter
    required
  />
</template>

<script>
export default {
  data() {
    return {
      companyItems: null,
      cpList: [],
      cpRules: {
        required: value => value.length !== 0 || 'Required.'
      }
    }
  }
}
</script>

<style>
</style>