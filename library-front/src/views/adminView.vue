<template>
  <div class="common-layout">
    <el-container>
      <el-aside width="5rem">
          <el-menu
            default-active="1"
          > 
            <RouterLink to="/addBook">
              <el-menu-item index="1" >
                <el-icon></el-icon>
                <span>添加图书</span>
              </el-menu-item>
            </RouterLink>
            <RouterLink to="/editBook">
              <el-menu-item index="2">
                <el-icon></el-icon>
                <span>编辑图书</span>
              </el-menu-item>
            </RouterLink>
          </el-menu>
        </el-aside>
      <el-main>
        <RouterView/>
      </el-main>
    </el-container>
  </div>
</template>
