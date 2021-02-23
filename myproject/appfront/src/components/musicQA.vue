<template>
  <div class="hello">
    <img  src="../assets/img/logo.png" id="logo">
    <p>{{ str2 }} </p>
    <search  @searchOk="searchOk" />
    <transition name="el-fade-in">
      <div  v-show="show" class="transition-box">{{answer}}</div>
    </transition>
    <footer>@Luer</footer>
  </div>
</template>


<script>
import search  from "./search";
import axios from "../assets/js/axios";
export default {
  name: 'musicQA',
  components: {search},
  data () {
    return {
      str: '凡音之起，由人心生也，人心之动，物使之然也',
      i: 0,
      timer: 0,
      str2: "",
      result: '',
      answer: '',
      show: false
    }
  },
  created() {
    this.show = false;
  },
  methods: {
    typing() {  //字体输入特效
      console.log(this.str)
      if (this.i <= this.str.length) {
        this.str2 = this.str.slice(0, this.i++) + '_';
        this.timer = setTimeout(() => {
          this.typing();
        }, 200);
      } else {
        clearTimeout(this.timer)
      }
    },
    searchOk(value) {
      console.log(value); //得到 搜索内容
      this.getAnswer(value);
      // 调用你的搜索接口，搜索条件为搜索的类型 + 搜索值
      // yourSearch (this.selectStatus, value)
    },
    getAnswer(value) {//得到 答案
     axios.Get({
       url: 'musicQA',
       params: {
         issue: value
       },
       callback: (res) => {
         console.log(res);
         let data = res.data;
         this.answer = data;
       }
     })
     this.show = true;
    }
  },
  mounted() {
    this.typing();
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  p{
    margin-top: -70px;
    color: black;
  }

  footer{
    color: black;
    width: 100%;
    position: absolute;
    bottom:0;
    left: 0;
  }
  .transition-box{
    margin: -90px auto;
    width: 40%;
    color: black;
    text-align: left;
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
    background-color: rgba(255,255,255,0.7);
    padding: 15px;
    letter-spacing: 1px;
    line-height: 22px;
    overflow:hidden;
  }
  #logo{
    margin-bottom: 10px;
    transform: scale(0.3);
  }
</style>
