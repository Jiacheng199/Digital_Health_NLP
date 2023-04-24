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
    :on-exceed="handleExceed"
    :on-success="handleSuccess"
    :file-list="fileList"
    multiple>
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
    // after clicking process button, send request to server for processing
    process(){
      console.log(JSON.parse(localStorage.getItem('file'))[0]);
      console.log(JSON.parse(localStorage.getItem('token')).userinfo.userid);
      try {
        const response = axios.post('http://127.0.0.1:5000/process',{
          file_id: JSON.parse(localStorage.getItem('file')),
          userid: JSON.parse(localStorage.getItem('token')).userinfo
        });
        console.log(response);
        this.$router.push("/mapping");
        // if (response.status === 200) {
        //   this.showProcess = false;
        //   this.showDownload = true;
        // }
      }
      catch (error) {
        console.log(error);
      }
    },
    // after clicking download button, send request to server for downloading
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
    // submit the file to server
    submitUpload() {
      localStorage.setItem('file', '[]');
      this.$refs.upload.submit();
    },
    // handle the file list change after uploading
    handleChange(file, fileList) {
      console.log(file);
      this.fileList = fileList;
    },
    // before removing the file, ask for confirmation
    beforeRemove(file, fileList) {
      return this.$confirm(`Cancel the transfert of ${ file.name } ?`);
    },
    // handle the file list change after removing
    handleRemove(file, fileList) {
      console.log(file, fileList);
      this.fileList = fileList;
    },
    // handle the file list change after exceeding the limit
    // can delete
    handleExceed(files, fileList) {
      this.$message.warning(`Only 1 file can be uploaded at a time.`);
    },
    // handle the file list change after uploading successfully
    handleSuccess(response, file, fileList) {
      console.log(response);
      this.file_id = response.file_id;
      let file_ids = JSON.parse(localStorage.getItem('file'));
      file_ids.push(response.file_id);
      localStorage.setItem('file', JSON.stringify(file_ids));
      this.showUpload = false;
      this.showProcess = true;
    }
  }
};
</script>
<style>
</style>