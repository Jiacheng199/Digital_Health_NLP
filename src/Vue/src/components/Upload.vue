<template>
  <div>
    <el-upload
    v-if="showUpload"
    ref="upload"
    action = "http://127.0.0.1:5000/upload"
    :headers="{'Authorization':'Barer '+userid}"
    :auto-upload="false"
    :on-preview="handlePreview"
    :on-change="handleChange"
    :before-remove="beforeRemove"
    :on-remove="handleRemove"
    :limit="1"
    :on-exceed="handleExceed"
    :on-success="handleSuccess"
    :file-list="fileList">
      <el-button slot="trigger" type="primary">select file</el-button>
      <el-button style="margin-left: 10px;" type="success" @click="submitUpload">upload to server</el-button>
      <div class="el-upload__tip" slot="tip" style="font-size: 15px;">txt file with a size less than 200Mb</div>
    </el-upload>
    <el-button v-if="showProcess"  @click="process">Process</el-button>
    <el-button v-if="showDownload" @click="downloadFile()">Download</el-button>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: 'Upload',
  created() {
    this.showUpload=true;
    this.showDownload=false;
    this.showProcess=false;
  },
  data() {
    return {
      showUpload: true,
      showProcess: false,
      showDownload: false,
      file:"",
      fileList: [],
      userid: JSON.parse(localStorage.getItem('token')).userinfo.userid,
      file_id: "",
    };
  },
  methods: {
    process(){
      console.log(localStorage.getItem('file'));
      console.log(JSON.parse(localStorage.getItem('token')).userinfo.userid);
      try {
        const response = axios.post('http://127.0.0.1:5000/process',{
          file_id: this.file_id,
          userid: JSON.parse(localStorage.getItem('token')).userinfo.userid
        });
        console.log(response);
        

        setTimeout(() => {
          this.showProcess = false;
          this.showDownload = true;
        }, 23000);
        // if (response.status === 200) {
        //   this.showProcess = false;
        //   this.showDownload = true;
        // }
      }
      catch (error) {
        console.log(error);
      }
    },
    downloadFile(event) {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:5000/download',
        data: {
          file_id: this.file_id,
          userid: JSON.parse(localStorage.getItem('token')).userinfo.userid
        },
        responseType: 'blob'
      })
      .then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', this.file_id+'.csv')
        document.body.appendChild(link)
        link.click()
      })

    },
    handlePreview(file) {
      console.log(file);
    },
    submitUpload() {
      this.$refs.upload.submit();
    },
    handleChange(file, fileList) {
      console.log(file);
      this.fileList = fileList;
    },
    beforeRemove(file, fileList) {
      return this.$confirm(`Cancel the transfert of ${ file.name } ?`);
    },
    handleRemove(file, fileList) {
      console.log(file, fileList);
      this.fileList = [];
    },
    handleExceed(files, fileList) {
      this.$message.warning(`Only 1 file can be uploaded at a time.`);
    },
    handleSuccess(response, file, fileList) {
      console.log(response);
      this.file_id = response.file_id;
      localStorage.setItem('file', JSON.stringify(response.file_id));
      this.showUpload = false;
      this.showProcess = true;
    }
  }
};
</script>

<style>
</style>