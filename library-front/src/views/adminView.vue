<script>
import {ref} from 'vue'
import router from "@/router"
import { ElMessage } from 'element-plus'
export default {
  methods: {
    exit(){
      router.push({name: 'Star'})
    }
  },
};
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-aside width="20vw" >
          <el-menu > 
          <RouterLink to="/editBook">
              <el-menu-item index="1">
                <el-icon></el-icon>
                <span>编辑图书</span>
              </el-menu-item>
            </RouterLink>
            <RouterLink to="/addBook">
              <el-menu-item index="2" >
                <el-icon></el-icon>
                <span>添加图书</span>
              </el-menu-item>
            </RouterLink>
          </el-menu>
          <el-button class="exit" type="danger" @click="exit">
            退出
          </el-button>
        </el-aside>
      <el-main>
        <RouterView/>
      </el-main>
    </el-container>
  </div>
</template>

<style scoped>
.exit{
  position:fixed;
  bottom: 20vh;
  left: 10vw;
}
</style>
