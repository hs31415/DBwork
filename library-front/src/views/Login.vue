<script>
import { ref } from 'vue'
import router from "@/router"
import { ElMessage } from 'element-plus'
export default {
  data() {
    return {
      form: {
        account: '',
        password: '',
      },
    }
  },
  methods: {
    goBack() {
      // 处理返回按钮点击事件，例如跳转到 home 页面
      router.push({name: 'Star'})
    },
    Login() {
      fetch('http://127.0.0.1:8000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          account: this.form.account,
          password: this.form.password,
        }),
      })
      .then(response => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('登录失败');
        }
      })
      .then(data => {
        if (data.message === '账号或密码错误') {
          ElMessage.error("登录失败，账号或密码错误");
          console.log(data)
        } else {
          ElMessage.success("登录成功");
          localStorage.setItem("account",this.form.account)
          console.log(data);
          router.push({name: 'BooksShow'})
        }
      })
      .catch(error => {
        ElMessage.error("登录失败")
      });
    },
  },
}
</script>

<template>
  <el-container>
    <el-header>
      <el-page-header :icon="ArrowLeft" @click="goBack">
        <template #title>
          <div style="font-size: 0.7rem;">返回</div>
        </template>
        <template #content>
          <div style="font-size: 0.7rem;"> 用户登录 </div>
        </template>
      </el-page-header>
    </el-header>
    <el-divider />
    <el-main>  
      <div class="login">
        <div class="content">
          <el-form :model="form" label-position="left" label-width="80px" ref="form">
            <el-form-item label="账号" prop="account">
              <el-input v-model="form.account" placeholder="请输入账号" clearable></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input
                type="password"
                v-model="form.password"
                placeholder="请输入密码"
                show-password
                clearable
              ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="Login">登录</el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </el-main>
  </el-container>
</template>

<style scoped>
.login {
  padding-top: 3rem;
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.title {
  font-size: 24px;
  margin-left: 20px;
}

.content {
  max-width: 400px;
  margin: 0 auto;
}
</style>