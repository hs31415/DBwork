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
    editNum(){
      this.dialogTableVisible=true
    },
    confirm(){
      console.log(this.number)
      if(this.number<0){
        ElMessage.error("最低数量不可低于零");
      }else{
        fetch('http://127.0.0.1:8000/addNum', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            id: this.infoList.id,
            number: this.number
          }),
        })
        .then(response => response.json())
        .then(data => {
          // 处理成功或失败的情况
          if (data.message === '添加图书成功') {
            console.log('添加图书成功');
            ElMessage.success("添加图书成功");
            // 在这里执行相关操作，例如更新页面状态等
            this.getInfo()
          } else {
            ElMessage.error("添加图书失败");
            console.log('添加图书失败');
            // 在这里执行相关操作，例如显示错误信息等
          }
        })
        .catch(error => {
          console.error('添加图书请求出错', error);
          ElMessage.error("添加图书失败");
          // 在这里处理请求出错的情况
        });
        this.dialogTableVisible=false
      }
 
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
      infoList:ref([
        {
          id:'0', 
          title:'0', 
          author:'0', 
          publisher:'0', 
          count:'0',
          currentNum:'0',
          description: '0'
        }
      ]),
      number:ref(),
      dialogTableVisible:ref(false)
    }
  },
};
</script>

<template>
  <el-button style="margin: 1rem;" @click="goBack">返回</el-button>

  <el-descriptions title="图书信息" :column="2" border>
    <el-descriptions-item label="书名" width="10%" label-align="center" align="center">
      {{ this.infoList.title }}
    </el-descriptions-item>

    <el-descriptions-item label="图书编号" width="10%" label-align="center" align="center">
      {{ this.infoList.id }}
    </el-descriptions-item>

    <el-descriptions-item label="存书量" label-align="center" align="center">
      {{ this.infoList.count }}
      </el-descriptions-item>

    <el-descriptions-item label="可借阅数量" label-align="center" align="center">
      {{ this.infoList.currentNum }}
    </el-descriptions-item>

    <el-descriptions-item label="描述" label-align="center" align="center">
      <div class="description">
        {{ this.infoList.description }}
      </div>
    </el-descriptions-item>

  </el-descriptions>

  <el-button class="showBorrow" type="primary" plain @click="editNum">
    添加图书
  </el-button>

  <el-dialog style="max-width: 500px;margin-top: 30vh;" v-model="dialogTableVisible">
    <el-form>
      <el-form-item label="请输入要添加的数量">
        <el-input v-model="this.number"/>
      </el-form-item>
      <el-button style="margin-left: 80%;" @click="confirm">
        确认
      </el-button>
    </el-form>
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

