<script>
import {ref} from 'vue'
import router from "@/router"
export default {
  methods: {
    goBack(){
      router.push({name: 'BooksShow'})
    }
  },
};
</script>

<template>
  <el-button @click="goBack">返回</el-button>
  <div>这是用户信息界面</div>
</template>


<style scoped>

</style>
