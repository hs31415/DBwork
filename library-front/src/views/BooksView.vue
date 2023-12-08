<script>
import {ref} from 'vue'
import router from "@/router"
import {User} from '@element-plus/icons-vue'
export default {
  methods: {
    goBack(){
      router.push({name: 'UserInfo'})
    }
  },
};
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <el-page-header :icon="null">
          <template #title>
            <div class="head-title" @click="goBack">
              <User style="width: 1.3rem;"/>
              个人中心
            </div>
          </template>
          <template #content>
            <div style="font-size: 1rem;width: 12rem;"> 欢迎使用图书管理系统 </div>
          </template>
        </el-page-header>
      </el-header>
      <el-container>
        <el-aside width="20vw">
          <el-menu
            default-active="1"
            class="el-menu-vertical-demo"
          > 
            <RouterLink to="/BooksShow">
              <el-menu-item index="1" >
                <el-icon></el-icon>
                <span>图书预览</span>
              </el-menu-item>
            </RouterLink>
            <RouterLink to="/BorrowingRecord">
              <el-menu-item index="2">
                <el-icon></el-icon>
                <span>查看借书记录</span>
              </el-menu-item>
            </RouterLink>
          </el-menu>
        </el-aside>
        <el-main>
          <RouterView/>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>


<style scoped>

.head-title{
  display: flex;
  font-size: 0.7rem;
  align-items: center;
  justify-content: center;
  width: 7rem;
}

</style>
