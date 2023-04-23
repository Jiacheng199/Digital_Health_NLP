<template>
  <el-container>
    <el-header>
      <el-menu
      :default-active="activeIndex"
      mode="horizontal" @select="handleSelect">
      <el-menu-item index="1">Mapping System</el-menu-item>
      <el-menu-item index="2">Mappings</el-menu-item>
      <div style="float:right; line-height: 60px; margin-right:20px;">
        <span style="margin-right:10px">{{ "Hi, "+userinfo.username }}</span>
        <el-dropdown>
          <i class="el-icon-user" style="margin-right: 15px"></i>
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
      activeIndex: '1',
      message: "",
      userinfo: {}
    };
  },
  methods: {
    checktoken(event){
      const tokenStr = localStorage.getItem('token');
      localStorage.removeItem('file');
      localStorage.setItem('file', '[]');
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
    },
    handleSelect(key, keyPath) {
    console.log(key, keyPath);
    if (key == 1) this.$router.push("/home");
    else if (key == 2) this.$router.push("/mapping");
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
