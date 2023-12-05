<script>
import {ref} from 'vue'
import router from "@/router"
import { ElMessage } from 'element-plus'
export default {
  created(){
    this.getInfo()
  },
  methods: {
    formatId(row) {
      return row.id.toString().padStart(9, '0');
    },
    getInfo() {
      fetch(`http://127.0.0.1:8000/borrowRecord/${localStorage.getItem('account')}`, {
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
      .then(borrowRecords => {
        console.log(borrowRecords) // 输出获取到的信息
        this.borrowRecord=borrowRecords
      })
      .catch(error => {
        console.error(`Error fetching book: ${error.message}`)
        // 在这里处理请求出错的情况
      })
    },
    returnBook(id){
      fetch('http://127.0.0.1:8000/returnBook', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          book_id: id,
          account: localStorage.getItem('account')
        }),
      })
      .then(response => response.json())
      .then(data => {
        // 处理借书成功或失败的情况
        if (data.message === '归还成功') {
          console.log('还书成功');
          ElMessage.success("还书成功");
          // 在这里执行相关操作，例如更新页面状态等
          this.getInfo()
        } else {
          ElMessage.error("归还失败");
          console.log('还书失败');
          // 在这里执行相关操作，例如显示错误信息等
        }
      })
      .catch(error => {
        console.error('还书请求出错', error);
        ElMessage.error("还书失败");
        // 在这里处理请求出错的情况
      });
    }
  },
  data(){
    return{
      borrowRecord:ref[
        {
          id:'0',
          title:'0'
        }
      ],
    }
  }
};
</script>

<template>
  <el-table :data="borrowRecord" height="500" border style="width: 100%" :default-sort="{ prop: 'id', order: 'ascending' }">
    <el-table-column 
      sortable 
      prop="id" 
      label="图书编号" 
      label-align="center" 
      align="center" 
      :formatter="formatId"
    />
    <el-table-column
      prop="title" 
      label="书名" 
      label-align="center" 
      align="center" 
    />
    <el-table-column fixed="right" label="操作" width="120" label-align="center" align="center">
      <template #default="scope">
        <el-button
          link
          type="primary"
          size="small"
          @click.prevent="returnBook(scope.row.id)"
        >
          还书
        </el-button>
      </template>
    </el-table-column>
  </el-table>
</template>


<style scoped>

</style>
