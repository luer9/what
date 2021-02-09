<template>
  <div class="search">

    <el-input v-model="searchValue" placeholder="请输入内容" class="inputSearch"></el-input>
    <el-button type="primary" icon="el-icon-search" @click="search" class="btn">搜索</el-button>


  </div>

</template>

<script>
    export default {
        name: "search",
      data() {
        return {
          searchValue: '',
          show: false
        }
      },
      methods:{
        search () {
          this.$emit('searchOk', this.searchValue);
        }
      }
    }
</script>

<style scoped>


  .inputSearch{
    margin: 120px auto;
    width: 36%;

  }

</style>
