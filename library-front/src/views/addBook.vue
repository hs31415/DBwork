<script>
import {ref} from 'vue'
import router from "@/router"
export default {
  methods: {
  },
  data(){
    return{
      form:ref({
        id:'',
        title:'',
        author:'',
        publisher:'',
        count:'',
        description:''
      })
    }
  }
};
</script>

<template>
  <el-form :inline="true" :model="form" class="demo-form-inline">
    <el-form-item label="图书编号">
      <el-input v-model="form.id" placeholder="Approved by" clearable />
    </el-form-item>
    <el-form-item label="Activity zone">
      <el-select
        v-model="form.region"
        placeholder="Activity zone"
        clearable
      >
        <el-option label="Zone one" value="shanghai" />
        <el-option label="Zone two" value="beijing" />
      </el-select>
    </el-form-item>
    <el-form-item label="Activity time">
      <el-date-picker
        v-model="form.date"
        type="date"
        placeholder="Pick a date"
        clearable
      />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSubmit">Query</el-button>
    </el-form-item>
  </el-form>
</template>

<style scoped>

</style>
