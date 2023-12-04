<script>
import {ref} from 'vue'
import router from "@/router"
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
  },
};
</script>

<template>
  <div class="home">
    <div class="welcome">欢迎使用图书管理系统</div>
    <div class="buttons">
      <el-button type="primary" size="large" @click="goToLogin">登录</el-button>
      <el-button size="large" @click="goToRegister">注册</el-button>
    </div>
  </div>
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
</style>
