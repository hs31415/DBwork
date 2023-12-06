<script>
import {ref} from 'vue'
import router from "@/router"
import { ElMessage } from 'element-plus'
export default {
  methods: {
    addBook(){
      console.log(this.form)
    },
    clear(){
      this.form={}
    },
    add() {
      fetch('http://127.0.0.1:8000/addBook', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title:this.form.title,
          author:this.form.author,
          publisher:this.form.publisher,
          description:this.form.description
        }),
      })
      .then(response => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('添加失败');
        }
      })
      .then(data => {
        if (data.message === '已有相同书籍') {
          ElMessage.error("已有相同书籍");
          console.log(data)
        } else {
          ElMessage.success("添加成功");
          console.log(data);
        }
      })
      .catch(error => {
        ElMessage.error("添加失败")
      });
    },
  },
  data(){
    return{
      form:ref({
        title:'',
        author:'',
        publisher:'',
        description:''
      })
    }
  }
};
</script>

<template>
  <el-form label-position="top" :model="form" class="demo-form-inline">
    <el-form-item label="书名">
      <el-input v-model="form.title" clearable />
    </el-form-item>
    <el-form-item label="作者">
      <el-input v-model="form.author" clearable />
    </el-form-item>
    <el-form-item label="出版商">
      <el-input v-model="form.publisher" clearable />
    </el-form-item>
    <el-form-item label="描述">
      <el-input v-model="form.description" type="textarea" placeholder="请输入简要描述(不超过200字)" clearable maxlength="200"/>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="add">确认</el-button>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="clear">清空</el-button>
    </el-form-item>
  </el-form>
</template>

<style scoped>

</style>
