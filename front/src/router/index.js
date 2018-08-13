import Vue from 'vue'
import Router from 'vue-router'
import groupContent from '@/components/group-content.vue'
import groupInfo from '@/components/group-info.vue'
import groupFilter from '@/components/group-filter.vue'
import groupAnalysis from '@/components/group-analysis.vue'

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/group',
      component: groupContent,
      children:[
        { path: '/info', name: 'info', component: groupInfo },
        { path: '/filter', name: 'filter', component: groupFilter },
        { path: '/analysis', name: 'analysis', component: groupAnalysis }
      ]
    }
  ]
})
