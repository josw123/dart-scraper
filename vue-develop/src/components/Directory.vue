<template>
  <div style="width:100%" >
    <v-snackbar v-model="error" color="error">
      Invalid Dictionary Path
    </v-snackbar>
    <v-dialog
      v-model="dialog"
      width="500"
    >
    <v-card class="mx-auto" max-width="500">
      <v-sheet class="pa-4 primary lighten-2">
        <v-text-field
          v-model="path"
          label="Current Directory"
          prepend-icon="mdi-arrow-up-bold"
          dark
          flat
          solo-inverted
          hide-details
          @click:prepend="parentFolder"
          @keydown.enter="itemClick(path)"
        />
      </v-sheet>
      <v-card-text style="height:400px;overflow-y:auto">
        <v-list-item-group
          v-if="subDirItems.length > 0"
          v-model="selectedItem"
          color="primary"
        >
          <v-list-item
            v-for="(item, i) in subDirItems"
            :key="i"
            @click="itemClick(subDirItems[i].path)"
          >
            <v-list-item-icon>
              <v-icon>mdi-folder</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title v-text="item.dirName"></v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
        <div v-if="subDirItems.length === 0" style="height:100%;margin:auto;text-align: center;">There is no subdirectory</div>
      </v-card-text>
      <v-card-actions>
        <v-btn text @click="select">Select</v-btn>
        <v-btn text @click="cancel">Reset</v-btn>
      </v-card-actions>
    </v-card>
    </v-dialog>
    <v-text-field
      v-model="path"
      :rules="[folderRules.required]"
      append-outer-icon="mdi-folder"
      label="Download Folder"
      @keydown.enter="setStartPath(path)"
      @click="()=>{dialog=true}"
      @click:append-outer="()=>{dialog=true}"
      required
    />
  </div>
</template>

<script>
export default {
  beforeCreate() {},
  data() {
    return {
      dialog: false,
      start_path: null,
      path: null,
      selectedItem: 1,
      subDirItems: [],
      error: false,
      folderRules: {
        required: value => !!value || 'Required.'
      }
    }
  },
  methods: {
    parentFolder() {
      const payload = { base_path: this.path, new_path: '..' }
      this.$store.dispatch('getDirectory', payload)
    },
    itemClick(path) {
      const payload = { base_path: path, new_path: null }
      this.$store.dispatch('getDirectory', payload)
    },
    setStartPath(path) {
      this.itemClick(path)
    },
    select() {
      this.dialog = false
    },
    cancel() {
      this.itemClick(this.start_path)
    }
  },
  computed: {
    basePath() {
      return this.$store.state.base_path
    },
    basePathError() {
      return this.$store.state.base_path_error
    },
    subdir() {
      return this.$store.state.subdir
    }
  },
  watch: {
    basePath(newValue) {
      this.path = newValue
      if (this.start_path === null) {
        this.start_path = newValue
      }
    },
    basePathError(newValue) {
      if (newValue) {
        this.path = this.basePath
        this.error = true
        this.$store.commit('setBasePathError', false)
      }
    },
    subdir(newValue) {
      this.subDirItems = newValue.map(v => {
        const dirNames = v.split(/\\|\//)
        const dirName =
          dirNames[dirNames.length - 1] !== ''
            ? dirNames[dirNames.length - 1]
            : dirNames[dirNames.length - 2]
        return {
          dirName: dirName,
          path: v
        }
      })
      this.selectedItem = null
    }
  }
}
</script>