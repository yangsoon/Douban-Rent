// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import strore from './store'
import 'iview/dist/styles/iview.css'


Vue.config.productionTip = false;


import {Button, Table, Modal, Row, Col, Card, Menu, MenuItem, Layout, Header, Content,
        Breadcrumb, BreadcrumbItem, Sider, Submenu, Footer, BackTop, Message, Page,
        Alert, Form, FormItem, CheckboxGroup, Checkbox, Input, Icon, Notice, Divider,
        RadioGroup, Radio} from 'iview'

Vue.component('Button', Button);
Vue.component('Table', Table);
Vue.component('Modal', Modal);
Vue.component('Row', Row);
Vue.component('Col', Col);
Vue.component('Card', Card);
Vue.component('Menu', Menu);
Vue.component('MenuItem', MenuItem);
Vue.component('Layout', Layout);
Vue.component('Header', Header);
Vue.component('Content', Content);
Vue.component('Breadcrumb', Breadcrumb);
Vue.component('BreadcrumbItem', BreadcrumbItem);
Vue.component('Sider', Sider);
Vue.component('Submenu', Submenu);
Vue.component('Footer', Footer);
Vue.component('BackTop', BackTop);
Vue.component('Message', Message);
Vue.component('Page', Page);
Vue.component('Alert', Alert);
Vue.component('Form', Form);
Vue.component('FormItem', FormItem);
Vue.component('CheckboxGroup', CheckboxGroup);
Vue.component('Checkbox', Checkbox);
Vue.component('Input', Input);
Vue.component('Icon', Icon);
Vue.component('Notice', Notice);
Vue.component('Divider', Divider);
Vue.component('RadioGroup', RadioGroup);
Vue.component('Radio', Radio);

Vue.prototype.$Message = Message;
Vue.prototype.$Notice = Notice;
Vue.prototype.$IVIEW = {transfer: true};

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
