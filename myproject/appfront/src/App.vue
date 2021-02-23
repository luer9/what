<template>

  <div id="app">

      <!--导航区域-->
        <v-nav></v-nav>
    <router-view></router-view>
<!--

-->



  </div>
</template>

<script>
import nav from './components/nav'
export default {
  components: { 'v-nav': nav },
  name: 'App'
}
</script>

<style>
  @import "./assets/css/base.css";
  @import "./assets/css/normalize.css";
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: black;
  /*margin-top: 60px;*/
  background:url("./assets/img/background.jpg");
  width:100%;
  height:100%;
  position:fixed;
  background-size:100% 100%;
}

</style>



# https://www.cnblogs.com/xujunkai/p/12266205.html  解决跨域问题
