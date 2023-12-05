<script>
import {ref} from 'vue'
import router from "@/router"
import { ElMessage } from 'element-plus'
export default {
  created(){
    this.getInfo()
  },
  methods: {
    showID(){
      console.log(this.$route.params.bookID)
    },
    getInfo() {
      fetch(`http://127.0.0.1:8000/get_book_by_id/${this.$route.params.bookID}`, {
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
      .then(book => {
        console.log(book) // 输出获取到的书籍信息
        this.infoList=book
      })
      .catch(error => {
        console.error(`Error fetching book: ${error.message}`)
        // 在这里处理请求出错的情况
      })
    },
    showBorrow(){
      this.dialogTableVisible=true
      fetch(`http://127.0.0.1:8000/borrowInfo/${this.$route.params.bookID}`, {
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
      .then(data => {
        console.log(data) // 输出获取到的书籍信息
        this.borrowList=data
      })
      .catch(error => {
        console.error(`Error fetching book: ${error.message}`)
        // 在这里处理请求出错的情况
      })
    },
    borrow(id){
      console.log(id)
      fetch('http://127.0.0.1:8000/borrow', {
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
        if (data.message === '借阅成功') {
          console.log('借书成功');
          ElMessage.success("借书成功");
          // 在这里执行相关操作，例如更新页面状态等
        } else {
          ElMessage.error("借书失败");
          console.log('借书失败');
          // 在这里执行相关操作，例如显示错误信息等
        }
      })
      .catch(error => {
        console.error('借书请求出错', error);
        ElMessage.error("借书失败");
        // 在这里处理请求出错的情况
      });
      this.dialogTableVisible=false
    },
    goBack() {
      this.$router.go(-1);
    },
    formatId(row) {
      return row.id.toString().padStart(9, '0');
    }

  },
  data(){
    return{
      infoList:[
        {
          id:'0', 
          title:'0', 
          author:'0', 
          publisher:'0', 
          currentNum:'0',
          description: '0'
        }
      ],
      borrowList:[
        {
          id:'0',
          isborrow:'0'
        }
      ],
      dialogTableVisible:ref(false)
    }
  },
};
</script>

<template>
  <el-button style="margin: 1rem;" @click="goBack">返回</el-button>

  <el-descriptions title="图书信息" :column="2" border>
    <el-descriptions-item label="书名" label-align="center" align="center">
      {{ this.infoList.title }}
    </el-descriptions-item>

    <el-descriptions-item label="图书编号" label-align="center" align="center">
      {{ this.infoList.id }}
    </el-descriptions-item>

    <el-descriptions-item label="作者" label-align="center" align="center">
      {{ this.infoList.author }}
      </el-descriptions-item>

    <el-descriptions-item label="出版社" label-align="center" align="center">
      {{ this.infoList.publisher }}
    </el-descriptions-item>

    <el-descriptions-item label="描述" label-align="center" align="center">
      <div class="description">
        {{ this.infoList.description }}
      </div>
    </el-descriptions-item>

  </el-descriptions>

  <el-button class="showBorrow" type="primary" plain @click="showBorrow">
    查看当前图书借阅情况
  </el-button>

  <el-dialog v-model="dialogTableVisible" title="当前图书借阅情况">
    <el-table :data="borrowList">
      <el-table-column prop="id" label="图书id" label-align="center" align="center" :formatter="formatId"/>
      <el-table-column prop="isborrow" label="是否借出" label-align="center" align="center">
        <template #default="scope">
          <div v-if="scope.row.isborrow">是</div>
          <div v-if="!scope.row.isborrow">否</div>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label-align="center" align="center" label="操作">
        <template #default="scope">
          <el-button
            v-if="!scope.row.isborrow"
            type="primary"
            size="small"
            @click.prevent="borrow(scope.row.id)"
          >
            借阅
          </el-button>
          <el-button
            v-if="scope.row.isborrow"
            type="info" 
            disabled
            size="small"
          >
            借阅
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-dialog>

</template>



<style scoped>
.description{
  word-wrap: break-word;
  text-align:left;
}
.showBorrow{
  position: absolute;
  margin: 1rem;
  right: 0;
}
</style>

