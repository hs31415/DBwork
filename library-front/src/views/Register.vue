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
      router.go(-1);
    },
    register() {
      //输入判断，不能为空且只能含有大小写字母或数字,长度为6-20之间
      const accountRegex = /^[a-zA-Z0-9]+$/;
      const passwordRegex = /^[a-zA-Z0-9]+$/;
      const minLength = 6;
      const maxLength = 20;
      if (!this.form.account) {
        ElMessage.error("账号不能为空");
        return;
      }
      if (!this.form.password) {
        ElMessage.error("密码不能为空");
        return;
      }
      if (this.form.account.length < minLength || this.form.account.length > maxLength) {
        ElMessage.error("账号长度必须在6-20个字符之间");
        return;
      }
      if (this.form.password.length < minLength || this.form.password.length > maxLength) {
        ElMessage.error("密码长度必须在6-20个字符之间");
        return;
      }
      if (!accountRegex.test(this.form.account)) {
        ElMessage.error("账号只能包含数字和大小写字母");
        return;
      }
      if (!passwordRegex.test(this.form.password)) {
        ElMessage.error("密码只能包含数字和大小写字母");
        return;
      }

      fetch('http://127.0.0.1:8000/register', {
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
          throw new Error('注册失败');
        }
      })
      .then(data => {
        if (data.message === '账号已存在') {
          ElMessage.error("注册失败，账号已存在");
        } else {
          ElMessage.success("注册成功");
          console.log(data);
          router.push({name: 'Login'})
        }
      })
      .catch(error => {
        ElMessage.error("注册失败")
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
            <div style="font-size: 0.7rem;"> 用户注册 </div>
          </template>
        </el-page-header>
      </el-header>
      <el-divider />
      <el-main>  
        <div class="register">
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
                <el-button type="primary" @click="register">注册</el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>
      </el-main>
    </el-container>
</template>

<style scoped>
.register {
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