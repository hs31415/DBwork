<script>
import {ref} from 'vue'
import router from "@/router"
export default {
  created(){
    this.getInfo()
  },
  methods: {
    showID(){
      console.log(this.$route.params.bookID)
    },
    getInfo() {
      fetch(`http://127.0.0.1:8000/book/${this.$route.params.bookID}`)
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
    goBack() {
      this.$router.go(-1);
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

  <el-button >借阅</el-button>
</template>



<style scoped>
.description{
  width:80vw;
  word-wrap: break-word;
  text-align:left;
}

.cell-item{
  width: 2rem;
  font-size: 0.7rem;
}
</style>

