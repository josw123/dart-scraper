<template>
     <v-textarea
          outlined
          name="log"
          label="Error Log"
          :value="log"
          readonly
        />
</template>
<script>
export default {
    data() {
        return {
            log: ''
        }
    },
    sockets: {
        errors({type, data}) {
            this.log += `${type}: ${data}\n`
        },
    }
}
</script>