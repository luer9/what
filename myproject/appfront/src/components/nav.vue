<template>
  <div id="navMenu">

    <el-menu :default-active="this.$router.path" class="el-menu-demo" mode="horizontal" @select="handleSelect" router>

      <template v-for = "item in navManuDate">
        <el-menu-item :index="item.index">{{item.name}}</el-menu-item>
      </template>

    </el-menu>
  </div>

</template>

<script>
  export default {
    data() {
      return {

        navManuDate: [
          {
            index: "/", name: "主页"
          },
          {
            index: "/all", name: "图谱全览"
          }
        ]
      };
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log("--->")
        console.log(key, keyPath);
        this.$router.push(keyPath)
      }
    },
    mounted(){
      console.log(this.$route.path)
      // this.activeIndex = this.$route.path.substring(1,this.$route.path.length);

    }
  }
</script>

<style scoped>
  img{
    border: 1px solid red;

  }

</style>
