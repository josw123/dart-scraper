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
          v-model="base_path"
          label="Current Directory"
          prepend-icon="mdi-arrow-up-bold"
          dark
          flat
          solo-inverted
          hide-details
          @click:prepend="parentFolder"
          @keydown.enter="itemClick(base_path)"
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
      v-model="base_path"
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
const DIRECTORY = 'DIRECTORY'
export default {
  beforeCreate() {
    this.$socket.emit(DIRECTORY,{})
  },
  sockets: {
    [DIRECTORY]({data}) {
      const  { base_path, subdir} = data
      this.base_path = base_path
      this.subdir = subdir
      this.$store.commit('setBasePath', base_path)
      if (this.start_path === null) {
        this.start_path = base_path
      }
    },
    errors({type}) {
      if (type === DIRECTORY) {
        this.base_path = this.start_path
      }
    }
  },
  data() {
    return {
      dialog: false,
      start_path: null,
      base_path: null,
      subdir: null,
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
      const payload = { base_path: this.base_path, new_path: '..' }
      this.$socket.emit(DIRECTORY, payload)
    },
    itemClick(path) {
      const payload = { base_path: path, new_path: null }
      this.$socket.emit(DIRECTORY, payload)
    },
    setStartPath(path) {
      this.itemClick(path)
    },
    select() {
      this.itemClick(this.base_path)
      this.dialog = false
    },
    cancel() {
      this.itemClick(this.start_path)
    }
  },
  watch: {
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