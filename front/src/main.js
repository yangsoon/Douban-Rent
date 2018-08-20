// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import strore from './store'
import iView from 'iview'
import 'iview/dist/styles/iview.css'

Vue.use(iView);

Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store: strore,
  components: { App },
  template: '<App/>',
  mounted(){
      this.$Notice.config({
          top: 120,
          duration: 5
      });
      this.$Message.config({
          top: 100,
          duration: 3
      });
  }
});
