<template>
  <div id="app">
    <dart-logo></dart-logo>
    <dart-form></dart-form>
  </div>
</template>

<script>
import DartLogo from "./components/DartLogo.vue"
import DartForm from './components/DartForm.vue'
export default {
  name: 'app',
  components: {
    DartLogo,
    DartForm
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}
</style>
