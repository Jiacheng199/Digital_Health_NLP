<template>
  <div class="login-container">
    <div class="login-box">
      <a href="/home">
        <img src="../img/unimelb-logo.png"  alt="LOGO" class="uni-logo">
      </a>
      <h3 class="title">Register</h3>
      <el-form class="register-form" ref="registerForm" :model="registerForm" :rules="registerFormRules">
        <el-form-item label="Username" prop="username">
          <el-input v-model="registerForm.username"></el-input>
        </el-form-item>
        <el-form-item label="Email" prop="email">
          <el-input v-model="registerForm.email"></el-input>
        </el-form-item>
        <el-form-item label="Password" prop="password">
          <el-input type="password" v-model="registerForm.password"></el-input>
        </el-form-item>
        <el-form-item label="Confirm Password" prop="confirmPassword">
          <el-input type="password" v-model="registerForm.confirmPassword"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button class="login-button" @click="submitForm">Register</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>
    
<script>
import axios from 'axios';
export default {
  name: "RegisterPage",
  data() {
    return {
      registerMessage: "",
      registerError: false,

      registerForm: {
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
      },
      registerFormRules: {
        username: [{ required: true, message: 'Please enter username', trigger: 'blur' }],
        email: [
          { required: true, message: 'Please enter email', trigger: 'blur' },
          { type: 'email', message: 'Please enter a valid email address', trigger: ['blur', 'change'] }
        ],
        password: [{ required: true, message: 'Please enter password', trigger: 'blur' }],
        confirmPassword: [
          { required: true, message: 'Please enter confirm password', trigger: 'blur' },
          {
            validator: (rule, value, callback) => {
              if (value !== this.registerForm.password) {
                callback(new Error('The two passwords do not match'));
              } else {
                callback();
              }
            },
            trigger: 'blur'
          }
        ]
      }
    };
  },
  methods: {
    async submitForm (event) {
      if (this.registerForm.password != this.registerForm.confirmPassword) {
        alert("Passwords do not match!");
        return;
      }
      try
      {
        const response = await axios.post('http://127.0.0.1:5000/register', {
        username: this.registerForm.username,
        password: this.registerForm.password,
        email: this.registerForm.email
        })
        this.registerError = false;
        this.registerMessage = response.data.message;
        setTimeout(() => {
          this.$router.push('/login')
        }, 2000)
      }catch (error) {
        this.registerError = true;
        this.registerMessage = error.response.data.message;
        setTimeout(() => {
          this.registerMessage = "";
        }, 2000)
      }
    }
  }
};
</script>
<style scoped>
.register-form {
  max-width: 400px;
  margin: 0 auto;
}

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
</style>
  