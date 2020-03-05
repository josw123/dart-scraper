<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <H2>Dart-Scraper {{ version }}</H2>
      </div>
      <v-spacer />
      <v-btn
        href="https://github.com/josw123/dart-scraper/releases/latest"
        target="_blank"
        text
      >
        <span class="mr-2">Latest Release</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>
    <v-content>
       <v-dialog v-model="error" persistent max-width="450">
         <v-card>
           <v-card-title>
             Error
           </v-card-title>
           <v-card-text>
             {{ error }}
           </v-card-text>
         </v-card>
       </v-dialog>
      <v-banner v-if="newVersion" single-line>
        <v-icon slot="icon" color="warning" size="36">
          mdi-open-in-new
        </v-icon>
        New Version Released!
        <template v-slot:actions>
          <v-btn
            color="primary"
            text
            href="https://github.com/josw123/dart-scraper/releases/latest"
          >
            Download
          </v-btn>
        </template>
      </v-banner>
      <DartForm />
    </v-content>
  </v-app>
</template>

<script>
import DartForm from './components/DartForm'

export default {
  name: 'App',
  components: {
    DartForm
  },

  beforeCreate() {
    this.$store.dispatch('getGithubVersion')
    this.$store.dispatch('getVersion')
    this.$store.dispatch('getDirectory')
  },
  computed: {
    github_version() {
      return this.$store.state.github_version
    },
    version() {
      return this.$store.state.version
    },
    newVersion() {
      let newVersion = false
      if (this.github_version !== null && this.version !== null) {
        const re = /(\d).(\d).(\d)/
        let vg = re.exec(this.github_version)
        let vl = re.exec(this.version)
        for (let i = 1; i < 4; i++) {
          let vg_i = parseInt(vg[i])
          let vl_i = parseInt(vl[i])
          if (vg_i > vl_i) {
            newVersion = true
            break
          } else if (vg_i < vl_i) {
            break
          }
        }
      }
      return newVersion
    },
    error() {
      return this.$store.state.error
    }
  }
}
</script>

<style></style>
