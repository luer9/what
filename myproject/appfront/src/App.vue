<template>

  <div id="app">
    <img src="./assets/img/logo.png" id="logo">

    <router-view/>
  </div>
</template>

<script>
export default {
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
  #logo{
    margin-bottom: 10px;
    transform: scale(0.3);
  }
</style>



# https://www.cnblogs.com/xujunkai/p/12266205.html  解决跨域问题
