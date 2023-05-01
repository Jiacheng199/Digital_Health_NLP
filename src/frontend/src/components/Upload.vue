<template>
  <el-main class="main-content" style="margin-top: 5%; padding-left: 20%; padding-right: 20%;">
    <el-row>
      <el-col>
        <div class="grid-content">
          <el-steps :active="active" finish-status="success" simple>
            <el-step title="Upload files" icon="el-icon-upload"></el-step>
            <el-step title="Add Comment" icon="el-icon-edit"></el-step>
            <el-step title="Process"></el-step>
          </el-steps>
        </div>
      </el-col>
    </el-row>
    <el-row>
      <el-col>
        <div class="grid-content" style="margin-left: 42%; margin-top: 5%;">
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
          <el-button style="margin-left: 10px;" type="success" @click="submitUpload(),next()">upload to server</el-button>
          <div class="el-upload__tip" slot="tip" style="font-size: 15px;">txt file with a size less than 200Mb</div>
        </el-upload>
        <el-button v-if="showProcess"  @click="process(),next()">Process</el-button>
        <el-button v-if="showDownload" @click="downloadFile()">Download</el-button>
      </div>
      </el-col>
    </el-row>
    <el-row v-if="showComment">
      <el-col style="margin-top: 5%; padding-left:30%; padding-right:30%">
        <el-form ref="form" :model="form" label-width="120px">
          <el-form-item label="Comment">
            <el-input v-model="comment"></el-input>
          </el-form-item>
          <el-form-item style="padding-left: 30%;">
            <el-button type="primary" @click="next(),toProcess()">Next</el-button>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
  </el-main>
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
      showComment: false,
      showProcess: false,
      showDownload: false,
      file:"",
      fileList: [],
      userid: JSON.parse(localStorage.getItem('token')).userinfo.userid,
      file_id: "",
      active: 0,
      comment:""
    };
  },
  methods: {
    process(){
      console.log(JSON.parse(localStorage.getItem('file'))[0]);
      console.log(JSON.parse(localStorage.getItem('token')).userinfo.userid);
      this.fileList = [];
      this.showProcess = false;
      this.showUpload = true;
      try {
        const response = axios.post('http://127.0.0.1:5000/process',{
          file_id: JSON.parse(localStorage.getItem('file')),
          userid: JSON.parse(localStorage.getItem('token')).userinfo,
          comment: this.comment
        });
        console.log(response);
        
        
        // this.$router.go(0);
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
      localStorage.setItem('file', '[]');
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
      this.fileList = fileList;
    },
    handleExceed(files, fileList) {
      this.$message.warning(`Only 1 file can be uploaded at a time.`);
    },
    handleSuccess(response, file, fileList) {
      console.log(response);
      this.file_id = response.file_id;
      let file_ids = JSON.parse(localStorage.getItem('file'));
      file_ids.push(response.file_id);
      localStorage.setItem('file', JSON.stringify(file_ids));
      this.showUpload = false;
      this.showComment = true;
    },
    next() {
      if (this.active++ > 1) this.active = 0;
    },
    toProcess(){
      this.showComment = false;
      this.showProcess = true;
    }
  }
};
</script>

<style>
</style>