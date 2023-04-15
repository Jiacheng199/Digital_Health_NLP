<template>
  <form enctype="multipart/form-data" @submit.prevent="uploadFile()">
    <div v-if="uploadResult" :class="`message ${uploadError ? 'is-danger':'is-success'}`">
      <div class="message-body">{{ uploadResult }}</div>
    </div>
    <div class="field">
      <div class="file is-boxed is-primary">
        <label class="file-label">
          <input multiple type="file" ref="files" @change="selectFile()" class="file-input"/>
          <span class="file-cta">
            <span class="span file-cta">
              <i class="fas fa-upload"></i>
            </span>
            <span class="file-label">
              Choose a file…
            </span>
          </span>
        </label>
      </div>
    </div>
    <div class="field">
        <div v-for="(file,index) in files" :class="`level ${file.invalidMessage && 'has-text-danger'}`">
            <div class="level-left">
                <div class="level-item">
                    {{ file.name }}
                    <span v-if="file.invalidMessage">&nbsp;- {{ file.invalidMessage }}</span>
                </div>
            </div>
            <div class="level-right">
                <div class="level-item">
                    <a @click.prevent="files.splice(index,1); uploadFiles.splice(index,1)" class="delete"></a>
                </div>
            </div>
        </div>
    </div>
    <div class="field">
      <button class="button is-info">Send</button>
    </div>
  </form>
</template>

<script>
import axios from "axios";
import _ from 'lodash';
/* eslint-disable */
export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: 'MultiUploads',
  data() {
    return {
      msg: "NMSL",
      showUpload: false,
      files: [],
      uploadResult: "",
      uploadError: false,
      uploadFiles: [],
      temp:0,
    };
  },
  methods: {
    selectFile(event) {
        const files = this.$refs.files.files;
        this.uploadFiles = [ ...this.uploadFiles, ...files]
        this.files = [ ...this.files, ..._.map(files,file =>({
        name: file.name,
        size: file.size,
        type: file.type,
        invalidMessage: this.validate(file),
        lastModified: file.lastModified,
        lastModifiedDate: file.lastModifiedDate,
        webkitRelativePath: file.webkitRelativePath,
      }))];
    },
    validate(file){
      const allowedTypes = ['text/csv', 'text/plain', 'application/json'];
      const MAX_SIZE = 1024*1024*100;
      if (file.size > MAX_SIZE) {
        return `File size is too large. Maximum size is ${MAX_SIZE} bytes.`;
      }
      if (!allowedTypes.includes(file.type)) {
        return `File type is not allowed. Allowed types are ${allowedTypes.join(', ')}`;
      }
      return "";
    },
    upload() {
      this.showUpload = true;
      axios.get('http://127.0.0.1:5000/upload')
      .then (response => {
        this.msg = response.data;
      })
      .catch(error => {
        console.log(error);
      });
    },
    async uploadFile() {
      const formData = new FormData();
      _.forEach(this.uploadFiles,file => {
        if (this.validate(file) === "") {
            formData.append('files'+String(this.temp), file);
            console.log(formData['files'])
            this.temp = this.temp + 1;
        }
      });
      try {
        await axios.post('http://127.0.0.1:5000/upload',formData);
        this.uploadError = false;
        this.uploadResult = "Upload successful";
        this.files = []
        this.uploadFiles = []
        this.temp = 0;
      }catch (error) {
        this.uploadError = true;
        this.uploadResult = error.response.data;
        this.temp = 0;
      }
    },
    autoload(){
      console.log('page loaded')
    }
  },
  mounted(){
      this.autoload();
  }
};
</script>

<style>
#fileList {
    margin-top: 20px;
}
</style>