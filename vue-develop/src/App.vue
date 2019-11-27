<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <H2>Dart-Scraper {{current_version}}</H2>
      </div>
      <v-spacer></v-spacer>
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
      <v-banner v-if="newVersion" single-line >
        <v-icon
                slot="icon"
                color="warning"
                size="36"
        >
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
      <DartForm/>
    </v-content>
  </v-app>
</template>

<script>
import DartForm from './components/DartForm';
import axios from 'axios';

export default {
  name: 'App',
  components: {
    DartForm,
  },

  data: () => {
    return {
      company: null,
      newVersion: false,
      current_version: null,
    }
  },
  mounted() {
    let url_base = window.location.href
    axios.get(url_base + "company").then( res => {this.company = res.data})
    axios.get('https://api.github.com/repos/josw123/dart-scraper/releases/latest').then(res1 => {
      axios.get(url_base + "version").then(res2 => {
        let re = /(\d).(\d).(\d)/
        let version = res2.data['version']
        let github_version = res1.data['tag_name']
        
        this.current_version = version
        
        let vg = re.exec(github_version)
        let vl = re.exec(version)
      
        for (let i=1; i < 4; i++) {
          let vg_i = parseInt(vg[i])
          let vl_i = parseInt((vl[i]))
          if (vg_i > vl_i) {
            this.newVersion = true
            break
          } else if (vg_i < vl_i) {
            break
          }
        }
      })
    })

  }
};
</script>

<style>
</style>
