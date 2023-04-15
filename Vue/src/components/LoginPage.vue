<template>
  <div class="login-container">
    <div class="login-box">
      <a href="/home">
        <img src="../img/unimelb-logo.png"  alt="LOGO" class="uni-logo">
      </a>
      <h3 class="title">Login</h3>
      <el-form ref="loginForm" :model="loginForm" class="login-form">
        <el-form-item label="User Name" prop="username">
          <el-input v-model="loginForm.username" placeholder="Please Enter Username"></el-input>
        </el-form-item>
        <el-form-item label="Password" prop="password">
          <el-input type="password" v-model="loginForm.password" placeholder="Please Enter Password"></el-input>
        </el-form-item>
        <el-form-item>
          <div>
            <label style="vertical-align: middle;" :class="`checkbox ${remeberMe ? 'checked':''}`" >
              <input type="checkbox" v-model="remeberMe">
            </label>
            <span style="vertical-align: middle;">Remeber Me</span>
          </div>
        </el-form-item>
        <el-form-item>
          <el-button class="login-button" @click="submitForm">Login</el-button>
        </el-form-item>
        <el-form-item>
          <p>Don't have an account?<router-link to="/register">Sign Up</router-link></p>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>
  
<script>
import axios from 'axios';
export default {
  name: "LoginPage",
  created (){
    this.getinfo();
  },
  data() {
    return {
      loginMessage: "",
      username: "",
      password: "",
      remeberMe: false,
      loginError: false,
      //
      loginForm: {
        username: '',
        password: ''
      }
    };
  },
  methods: {
    async submitForm (event) {
      try {
        const response = await axios.post('http://127.0.0.1:5000/login', {
          username: this.loginForm.username,
          password: this.loginForm.password
        })
        if (this.remeberMe) {
          localStorage.setItem('remeberuser', JSON.stringify(this.loginForm.username));
        }
        
        this.loginError = false
        this.loginMessage = response.data.message
        const expireTime = new Date().getTime() + 3600 * 1000*3;
        const tokenObj = {
          userinfo: response.data.userinfo,
          expireTime: expireTime
        };
        localStorage.setItem('token', JSON.stringify(tokenObj));
        console.log(JSON.parse(localStorage.getItem('token')).userinfo)
        setTimeout(() => {
          this.$router.push("/home");
        }, 2000);
      } catch (error) {
        this.loginError = true
        this.loginMessage= error.response.data.message
        setTimeout(() => {
        this.loginMessage = "";
        }, 2000);
      }
    },
    getinfo(){
      const userInfo = localStorage.getItem('remeberuser');
      if (userInfo) {
        this.loginForm.username = JSON.parse(userInfo);
        this.remeberMe = true;
      }
    },
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          // 登录逻辑
        } else {
          return false;
        }
      });
    }
  }
};
</script>
<style scoped>
h3 {
    text-align: center;
    margin-bottom: 20px;
}

.uni-logo {
    display: block;
    width: 100px;
    height: auto;
    margin: 0 auto 20px;
}
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.login-box {
  width: 400px;
  padding: 20px;
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 24px;
  margin-bottom: 20px;
}

.login-form {
  width: 100%;
}

.el-form-item__label {
  font-size: 14px;
}

.el-input__inner {
  height: 36px;
  font-size: 14px;
}

.el-button {
  width: 100%;
}

.el-button.login-button {
  background-color: #0d3978;
  border-color: #0d3978;
  color: #ffffff;
}
.el-button.login-button:hover {
  background-color: #061d3c;
  border-color: #061d3c;
  color: #ffffff;
}


/* checkbox */
.checkbox {
  display: inline-block;
  position: relative;
  width: 18px;
  height: 18px;
  background-color: #fff;
  border: 1px solid #dcdfe6;
  border-radius: 2px;
  cursor: pointer;
  margin-right: 10px;
}
.checkbox.checked {
  background-color: #0d3978;
  border-color: #0d3978;
}
.checkbox.checked::after {
  content: "";
  position: absolute;
  left: 5px;
  top: 1px;
  width: 5px;
  height: 10px;
  border: solid #fff;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}
.checkbox:hover {
  border-color: #409eff;
}
.checkbox input[type="checkbox"] {
  display: none;
}
</style>
