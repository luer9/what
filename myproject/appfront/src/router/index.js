import Vue from 'vue'
import Router from 'vue-router'
import musicQA from "../components/musicQA";
import charts from "../components/all"

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'musicQA',
      component: musicQA
    },
    {
      path: '/all',
      component: charts
    }

  ]
})

const originalPush = Router.prototype.push
Router.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}
