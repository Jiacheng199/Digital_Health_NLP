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
    <Upload></Upload>
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
      userinfo: {},
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
  }
};
</script>

<style scoped>
.main-content {
  /* display: flex; */
  justify-content: center;
  align-items: center;
  position: relative;
  width: 100%;
  height: 100%;
}
</style>
