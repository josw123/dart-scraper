<template>
    <v-snackbar v-model="error" dark color="black">
       {{msg}}
        <v-btn
            color="pink"
            text
            @click="error = false"
        >
        Close
      </v-btn>
    </v-snackbar>
</template>

<script>
export default {
    name: 'Alert',
    data() {
        return {
            error: false,
            title: null,
            msg: null,
        }
    },
    sockets: {
        errors({type, data}) {
            this.error = true
            this.title = type
            this.msg = data
        },
        connect_error(){
            this.error = true
            this.title = 'Connection Error'
            this.msg = 'The connection with the Dart-Scraper has been terminated'
        },
    }
}
</script>