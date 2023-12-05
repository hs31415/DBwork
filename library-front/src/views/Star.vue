<script>
import {ref} from 'vue'
import router from "@/router"
import { ElMessage } from 'element-plus'
export default {
  methods: {
    goToLogin() {
      // 处理跳转到登录页的逻辑
      router.push({name: 'Login'})
    },
    goToRegister() {
      // 处理跳转到注册页的逻辑
      router.push({name: 'Register'})
    },
    admin(){
      this.formVisible=true
    },
    adLogin(){
      fetch(`http://127.0.0.1:8000/setAdmin/${this.input}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then(response => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('密码错误');
        }
      })
      .then(data => {
        if (data.message === '密码错误') {
          ElMessage.error("密码错误");
          console.log(data)
        } else {
          router.push({name: 'adLogin'})
        }
      })
      .catch(error => {
        ElMessage.error("密码错误")
      });
    },
    adRegister(){
      fetch(`http://127.0.0.1:8000/setAdmin/${this.input}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then(response => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('密码错误');
        }
      })
      .then(data => {
        if (data.message === '密码错误') {
          ElMessage.error("密码错误");
          console.log(data)
        } else {
          router.push({name: 'adRegister'})
        }
      })
      .catch(error => {
        ElMessage.error("密码错误")
      });
    }
  },
  data(){
    return{
      input:ref(),
      formVisible:ref(false)
    }
  }
};
</script>

<template>
  <div class="home">
    <div class="welcome">欢迎使用图书管理系统</div>
    <div class="buttons">
      <el-button type="primary" size="large" @click="goToLogin">登录</el-button>
      <el-button size="large" @click="goToRegister">注册</el-button>
      <el-button class="adLogin" type="info" plain @click="admin" >管理员模式</el-button>
    </div>
  </div>
  <el-dialog v-model="formVisible" title="管理员模式验证" width="10rem" align-center>
    <el-form>
      <el-form-item label="输入密码">
        <el-input
          v-model="input"
          type="password"
          placeholder="Please input password"
          show-password
        />
      </el-form-item>
      <el-button type="primary" plain style="position: relative;left: 55%;" @click="adRegister">
        注册
      </el-button>
      <el-button type="primary" plain style="position: relative;left: 60%;" @click="adLogin">
        登录
      </el-button>
    </el-form>

  </el-dialog>
</template>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position:absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.welcome {
  font-size: 1.5rem;
  padding: 2rem;
  margin-bottom: 20px;
}

.buttons {
  display: flex;
  justify-content: center;
  gap: 100px;
}
.adLogin{
  display: flex;
  position:absolute;
  right: 1rem;
  bottom: 1rem
}
</style>
