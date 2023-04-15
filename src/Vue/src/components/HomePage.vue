<template>
  <el-container>
    <el-header>
      <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal">
      <el-menu-item index="1"><router-link to="/home" style="text-decoration: none;">Mapping System</router-link></el-menu-item>
      <el-menu-item index="2"><router-link to="/home" style="text-decoration: none;">Upload</router-link></el-menu-item>
      <el-menu-item index="3"><router-link to="/mapping" style="text-decoration: none;">Mappings</router-link></el-menu-item>
      <div style="float:right; line-height: 60px; margin-right:20px;">
        <span style="margin-right:10px">{{ "Hi, "+userinfo.username }}</span>
        <el-dropdown>
          <i class="el-icon-setting" style="margin-right: 15px"></i>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item>Profile</el-dropdown-item>
            <el-dropdown-item><div @click="signout">Sign Out</div></el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
      </el-menu>
    </el-header>
    <el-main class="main-content" style="margin-top: 20%;">
      <Upload></Upload>
      <!-- <el-upload
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
      <el-button v-if="!showUpload"  @click="process">Process</el-button> -->
    </el-main>
  </el-container>
</template>

<script scoped>
import axios from 'axios';
import Upload from './Upload.vue'

export default {
  name: "HomePage",
  components: {
    Upload
  },
  created (){
    this.checktoken();
  },
  data() {
    return {
      activeIndex: '2',
      message: "",
      userinfo: {}
    };
  },
  methods: {
    checktoken(event){
      const tokenStr = localStorage.getItem('token');
      if (tokenStr !== null) {
        const tokenObj = JSON.parse(tokenStr);
        const userInfo = tokenObj.userinfo;
        const expireTime = tokenObj.expireTime;
  
        if (new Date().getTime() > expireTime) {
            localStorage.removeItem('tokenObj');
            this.$router.push("/login");
        }
        else this.userinfo = userInfo;
      }
      else{
        this.$router.push("/login");
      }
    },
    // signout
    signout(event){
      localStorage.removeItem('token');
      this.$router.push("/login");
    }
    // getmappinginfo(){
    //     console.log(localStorage.getItem('userid'));
    //     const path = 'http://127.0.0.1:5000/getmaps';
    //     axios.get(path,{
    //         headers:{
    //             'Getmapping': 'Bearer ' + localStorage.getItem('userid')
    //         }
    //     })
    //     .then(response => {
    //         console.log(response.data.map);
    //         this.mappings = response.data.map;
    //     })
    //     .catch(error => {
    //         this.mappings=[];
    //         console.log(error);
    //     });
    // },
    // deleteMapping(id){
    //     const temp = id.toString()
    //     console.log(temp)
    //     const path = 'http://127.0.0.1:5000/deletemap/'+temp;
    //     axios.delete(path)
    //     .then(response => {
    //         console.log(response.message);
    //         this.getmappinginfo();
    //     })
    //     .catch(error => {
    //         console.log(error.message);
    //         console.log(error);
    //     });
    // },
    // viewMapping(id){
    //   localStorage.setItem('mapid', id);
    //   this.$router.push("/viewmapping");
    // }
  }
};
</script>

<style scoped>
.main-content {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  width: 100%;
  height: 100%;
}
</style>
