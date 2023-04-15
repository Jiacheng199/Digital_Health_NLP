<template>
  <!-- <div class = "section">
    <div class="columns">
      <div class="column">
        <Upload/>
      </div>
      <div class="column">
        <multiUploads/>
      </div>
    </div>
    <Dropzone/>
  </div> -->
  <div id="app">
    <!-- <router-view to="/upload">TEMP</router-view> -->
    <router-view to="/home">TEMP</router-view>
  </div>
</template>

<style scoped>
/* @import '../node_modules/bootstrap/dist/css/bootstrap.min.css'; */

</style>

<script >
  import Upload from './components/Upload.vue'
  import multiUploads from './components/MultiUploads.vue'
  import Dropzone from './components/Dropzone.vue'
  
  export default {
    name: 'App',
    components: {
      Upload,multiUploads,Dropzone
    }
  }
</script>