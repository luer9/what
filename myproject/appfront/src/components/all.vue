<template>

  <transition name="el-fade-in">

    <div id="chart" class="transition-box"></div>
  </transition>
</template>
<script>
  import '../assets/js/jquery-3.4.1.min'
  import {initKG} from '../assets/js/kg.js'
  import axios from '../assets/js/axios'

  var mapid = new Map();

  //节点格式整理:
  function nodeformat(datas){
    let nodesdata = {};
    for(var i = 0; i < datas.length; i++) {
      let temp = {};
      temp['name'] = datas[i].name;
      temp['type'] = datas[i].type[0];
      nodesdata[(i+1)] = temp;
      mapid.set(datas[i].name, i + 1);
    }
    return nodesdata;
  }

  //relsformat 关系格式整理
  function relsformat (datas) {
    let relsdata = [];
    for(var i = 0; i < datas.length; i++) {
      let temp = {};
      temp['source'] = mapid.get(datas[i].source);
      temp['target'] = mapid.get(datas[i].target);
      temp['rela'] = datas[i].rela;
      temp['type'] = datas[i].rela;  // 关系的类型 其实就是 关系的名称
      relsdata.push(temp);
    }
    return relsdata;
  }
export default {
  name: "charts",
  data(){
    return {
      // 初始化数据
      datas: {
        nodes:  {
          1: {
            name: "数据结构",
            type: "学科"
          },
          2: {
            name: "二叉树",
            type: "知识点"
          },
          3: {
            name: "链表",
            type: "知识点"
          }
        },
        links: [
          { source: 1, target: 2, rela: "包含", type: "包含关系" },
          { source: 1, target: 3, rela: "包含", type: "包含关系" }
        ]
      },


      config: {
        content: '<h3>hello world</h3>',
        contentHook: null,  // 没什么用
        nodeColor:null,
        linkColor: null,
        width: 1980,
        height: 1040
      },
      //节点配色
      defaultNodeColor:  [
        //粉红
        { fill: "rgb(249, 235, 249)", stroke: "rgb(162, 84, 162)", text: "rgb(162, 84, 162)" },
        //灰色
        { fill: "#ccc", stroke: "rgb(145, 138, 138)", text: "#333" },
        { fill: "rgb(112, 202, 225)", stroke: "#23b3d7", text: "rgb(93, 76, 93)" },
        { fill: "#D9C8AE", stroke: "#c0a378", text: "rgb(60, 60, 60)" },
        { fill: "rgb(178, 229, 183)", stroke: "rgb(98, 182, 105)", text: "rgb(60, 60, 60)" },
        //红
        { fill: "rgb(248, 152, 152)", stroke: "rgb(233, 115, 116)", text: "rgb(60, 60, 60)" }
      ],
      // 关系配色
      defaultLinkColor: [
        { color: "rgb(162, 84, 162)" },
        { color: "rgb(145, 138, 138)" },
        { color: "#23b3d7" },
        { color: "#c0a378" },
        { color: "rgb(98, 182, 105)" },
        { color: "rgb(233, 115, 116)" }
      ]
    }
  },
  created () {

  },
  mounted: function(){
    console.log("--------------==========")
    console.log("===mounted===")
    this.getNodes();
    this.getRels();

  },
  methods:{
    // 初始化配置
    /*
    contentHook(item){
      return "<div>"+item.name+"</div>"
    }

     */
    Init(){
      console.log("---->", this.datas)
      initKG(this.datas, this.config, "#chart");
    },
    getNodes() {//得到所有的结点
      axios.Get({
        url: 'getnodes',
        params: {

        },
        callback: (res) => {
          console.log(res.data);
          let data = res.data;
          let nodesdata = nodeformat(data);
          this.datas.nodes = nodesdata;
          console.log(nodesdata);

        }
      })
    },
    getRels(){  //得到所有的关系
      axios.Get({
        url: 'getrels',
        params: {

        },
        callback: (res) => {
          console.log(res.data);
          let data = res.data;
          let relsdata = relsformat(data);
          this.datas.links = relsdata;
          console.log("rels---->", relsdata);
          this.Init();
        }
      })
    }
  }
}

  /*

  */

  //https://github.com/Jeff-Bee/knowledgeGraph/blob/master/src/components/Charts.vue
   // https://www.it610.com/article/1294827465092440064.htm  !
</script>
<style scoped>
  @import '../assets/css/kg.css';

  .transition-box{


    width: 100%;
    height: 100%;
    margin: 50px auto;
    padding: 50px;
    color: black;
    text-align: left;
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
    background-color: rgba(255,255,255,0.7);

    letter-spacing: 1px;
    line-height: 22px;
    overflow:hidden;
  }
</style>
