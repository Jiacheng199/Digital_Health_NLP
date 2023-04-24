<template>
  <el-container>
    <!-- Nav bar -->
    <el-header>
      <!-- Menu items -->
      <el-menu
      :default-active="activeIndex"
      mode="horizontal" @select="handleSelect">
      <el-menu-item index="1">Mapping System</el-menu-item>
      <el-menu-item index="2">Mappings</el-menu-item>
      <!-- Display user name in nav bar -->
      <div style="float:right; line-height: 60px; margin-right:20px;">
        <span style="margin-right:10px">{{ "Hi, "+userinfo.username }}</span>
        <!-- Dropdown for sign out and view user profile -->
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
    <!-- Main content includes upload components-->
    <el-main class="main-content" style="margin-top: 20%;">
      <Upload></Upload>
    </el-main>
  </el-container>
</template>

<script scoped>
import axios from 'axios';
// upload component
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
      // menu active display index
      activeIndex: '1',
      // store user info after login success
      userinfo: {}
    };
  },
  methods: {
    // check token and login status if token is expired or not
    // if token is expired, redirect to login page
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
    // handle menu select
    handleSelect(key, keyPath) {
    console.log(key, keyPath);
    if (key == 1) this.$router.push("/home");
    else if (key == 2) this.$router.push("/mapping");
    }
  }
};
</script>
<!-- scoped disable global css -->
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
