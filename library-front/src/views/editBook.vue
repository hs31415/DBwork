<script>
import {ref} from 'vue'
import router from "@/router"
import { ElMessage } from 'element-plus'
export default {
  created() {
    this.getBooksInfo();
  },
  methods: {
    goDetail(index){
      router.push({name: 'editDetail',params:{'bookID':index}})
    },
    getBooksInfo() {
      fetch('http://127.0.0.1:8000/get_books', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then(response => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('失败');
        }
      })
      .then(data => {
        console.log(data)
        this.infoList=data
      })
      .catch(error => {
        ElMessage.error("失败")
      });
    },
  },
  data(){
    return{
      infoList:[],
    }
  }
};
</script>

<template>
  <el-table :data="infoList" height="70vh" border style="width: 100%" :default-sort="{ prop: 'id', order: 'ascending' }">
    <el-table-column sortable prop="id" label="图书编号" label-align="center" align="center" />
    <el-table-column prop="title" label="书名" label-align="center" align="center" />
    <el-table-column prop="author" label="作者" label-align="center" align="center" />
    <el-table-column prop="publisher" label="出版社" label-align="center" align="center"  />
    <el-table-column prop="currentNum" label="数量" label-align="center" align="center"  />
    <el-table-column fixed="right" label="操作" width="120" label-align="center" align="center">
      <template #default="scope">
        <el-button
          link
          type="primary"
          size="small"
          @click.prevent="goDetail(scope.row.id)"
        >
          编辑图书信息
        </el-button>
      </template>
    </el-table-column>
  </el-table>
</template>
<style scoped>
.list{
  margin-bottom: 0.5rem;
  list-style-type: none;
}
</style>



<style scoped>

</style>
