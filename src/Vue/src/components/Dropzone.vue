<template>
    <!-- <div class="temp">
      <vue-dropzone ref="myVueDropzone" :options="dropzoneOptions" :useCustomSlot=true>
        <div class="dropzone-custom-content">
          <h3 class="dropzone-custom-title">Drag and drop to upload content!</h3>
          <div class="subtitle">...or click to select a file from your computer</div>
        </div>
      </vue-dropzone>
    </div> -->
</template>

<script>
import axios from "axios";
/* eslint-disable */
export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: 'Dropzone',
  data() {
    return {
      


    };
  },
  methods: {
    // async dropZone() {
    //   const file = this.$refs.file.files[0];
    //   const formData = new FormData();
    //   formData.append('file', file);
    //   try {
    //     await axios.post('http://127.0.0.1:5000/dropzone',formData);
    //   }
    //   catch (error) {
    //     this.uploadResult = error.response.data;
    //     this.uploadError = true;
    //   }
    // },
    // autoload(){
    //   console.log('page loaded')
    // }
  },
  mounted(){
      // this.autoload();
  }
};
</script>

<style>
/* @import "https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css"; */
</style>