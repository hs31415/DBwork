<script>
import {ref} from 'vue'
import router from "@/router"
import { ElMessage } from 'element-plus'
export default {
  created(){
    this.getInfo()
  },
  methods: {
    goBack(){
      router.push({name: 'BooksShow'})
    },
    quit(){
      localStorage.setItem('account','')
      router.push({name: 'Star'})
    },
    getInfo() {
      fetch(`http://127.0.0.1:8000/userInfo/${localStorage.getItem('account')}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then(response => {
        if (!response.ok) {
          throw new Error("Network response was not ok")
        }
        return response.json()
      })
      .then(name => {
        console.log(name) // 输出获取到的信息
        this.username=name
      })
      .catch(error => {
        console.error(`Error fetching book: ${error.message}`)
        // 在这里处理请求出错的情况
      })
    },
    changeName(){
      this.dialogFormVisible=true
    },
    realChange(){
      this.dialogFormVisible=false
      fetch('http://127.0.0.1:8000/changeName', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          account: localStorage.getItem('account'),
          name:this.form.name
        }),
      })
      .then(response => response.json())
      .then(data => {
        // 处理借书成功或失败的情况
        if (data.message === '修改成功') {
          console.log('修改成功');
          ElMessage.success("修改成功");
          // 在这里执行相关操作，例如更新页面状态等
          this.getInfo()
        } else {
          ElMessage.error("修改失败");
          console.log('修改失败');
          // 在这里执行相关操作，例如显示错误信息等
        }
      })
      .catch(error => {
        console.error('修改请求出错', error);
        ElMessage.error("修改失败");
        // 在这里处理请求出错的情况
      });
    }
  },
  data(){
    return{
      username:'',
      dialogFormVisible:ref(false),
      form:ref({
        name:''
      })
    }
  }
};
</script>

<template>
  <el-button @click="goBack">返回</el-button>
  <div class="content">
      <h1>Hello, {{ this.username }}!</h1>
      <div>欢迎使用图书管理系统</div>
  </div>
  <el-button type="primary" @click="changeName">修改用户名</el-button>
  <el-dialog v-model="dialogFormVisible" title="Shipping address">
    <el-form :model="form">
      <el-form-item label="修改后的用户名" :label-width="140">
        <el-input v-model="form.name" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="realChange">
          确认
        </el-button>
      </span>
    </template>
  </el-dialog>
  <el-button size="large" class="quit" @click="quit" type="danger" >退出</el-button>
</template>


<style scoped>
.content{
  text-align: center; /* 文本居中对齐 */
  justify-content: center;
  align-items: center;
}
.quit{
  position: absolute;
  right: 1rem;
  bottom: 1rem;
}

</style>
