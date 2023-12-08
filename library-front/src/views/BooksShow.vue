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
      router.push({name: 'BookDetail',params:{'bookID':index}})
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
      infoList:ref([]),
      searchId:ref(),
      searchTitle:ref(),
      searchAuthor:ref(),
      searchPublisher:ref(),
    }
  },
  computed: {
    filteredInfoList() {
      let filteredData = this.infoList;
      if (this.searchId) {
        filteredData = filteredData.filter(item => item.id.toString().includes(this.searchId));
      }
      if (this.searchTitle) {
        filteredData = filteredData.filter(item => item.title.toLowerCase().includes(this.searchTitle.toLowerCase()));
      }
      if (this.searchAuthor) {
        filteredData = filteredData.filter(item => item.author.toLowerCase().includes(this.searchAuthor.toLowerCase()));
      }
      if (this.searchPublisher) {
        filteredData = filteredData.filter(item => item.publisher.toLowerCase().includes(this.searchPublisher.toLowerCase()));
      }
      return filteredData;
    },
  },

};
</script>

<template>
  <el-row :gutter="20" style="margin-bottom: 1rem;">
    <el-col :span="6">
      <el-input v-model="searchId" placeholder="请输入图书编号"></el-input>
    </el-col>
    <el-col :span="6">
      <el-input v-model="searchTitle" placeholder="请输入书名"></el-input>
    </el-col>
    <el-col :span="6">
      <el-input v-model="searchAuthor" placeholder="请输入作者"></el-input>
    </el-col>
    <el-col :span="6">
      <el-input v-model="searchPublisher" placeholder="请输入出版社"></el-input>
    </el-col>
  </el-row>

  <el-table :data="filteredInfoList" height="70vh" border style="width: 100%" :default-sort="{ prop: 'id', order: 'ascending' }">
    <el-table-column sortable prop="id" label="图书编号" label-align="center" align="center" />
    <el-table-column prop="title" label="书名" label-align="center" align="center" />
    <el-table-column prop="author" label="作者" label-align="center" align="center" />
    <el-table-column prop="publisher" label="出版社" label-align="center" align="center"  />
    <el-table-column prop="count" label="存书量" label-align="center" align="center"  />
    <el-table-column prop="currentNum" label="可借阅数量" label-align="center" align="center"  />
    <el-table-column fixed="right" label="操作" width="120" label-align="center" align="center">
      <template #default="scope">
        <el-button
          link
          type="primary"
          size="small"
          @click.prevent="goDetail(scope.row.id)"
        >
          查看详情
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
