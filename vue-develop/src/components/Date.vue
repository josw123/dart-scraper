<template>
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
          />
        </template>
        <v-date-picker v-model="startdt" no-title scrollable>
          <v-spacer />
          <v-btn text color="primary" @click="startdtMenu = false"
            >Cancel</v-btn
          >
          <v-btn text color="primary" @click="$refs.startdtMenu.save(startdt)"
            >OK</v-btn
          >
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
          />
        </template>
        <v-date-picker v-model="enddt" no-title scrollable>
          <v-spacer />
          <v-btn text color="primary" @click="endMenu = false">Cancel</v-btn>
          <v-btn text color="primary" @click="$refs.endMenu.save(enddt)"
            >OK</v-btn
          >
        </v-date-picker>
      </v-menu>
    </v-col>
  </v-row>
</template>

<script>
export default {
  beforeMount() {
    this.startdt = new Date('2012-01-01').toISOString().substr(0, 10)
    this.enddt = new Date().toISOString().substr(0, 10)
  },
  data() {
    return {
      startdtMenu: false,
      startdt: null,

      endMenu: false,
      enddt: null
    }
  },
  watch: {
    startdt(newValue) {
      const bgn_de = newValue.replace(/-/g, '')
      this.$store.commit('setBgnDe', bgn_de)
    },
    enddt(newValue) {
      const end_de = newValue.replace(/-/g, '')
      this.$store.commit('setEndDe', end_de)
    }
  }
}
</script>
