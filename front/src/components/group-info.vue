<template>
  <div>
    <div class="datalist"  v-if="rent">
      <Table border :columns="column" :data="rent" :loading="loading"></Table>
    </div>
    <div v-if="number">
      <Page id="page" :current.sync="current" :total="number" :page-size="25" @on-change="changePage"/>
    </div>
    <BackTop></BackTop>
  </div>
</template>
<script>
    import ajax from '@/ajax'
    import { mapState } from 'vuex'
    export default {
        data () {
            return {
                column: [
                    { title: '讨论', width: 450,
                        render: (h, params) => {
                            return h('strong', params.row.title_text);
                          }
                    },
                    { title: '作者', width: 110, align: 'center' ,
                        render: (h, params) => {
                            return h('a', {
                                attrs:{
                                  href: params.row.author_link,
                                  target: '_blank'
                                },
                            }, params.row.author_name);
                          }
                    },
                    { title: '发帖时间', key: 'add_time', width: 180, align: 'center'},
                    { title: '回应数', key: 'comment_num',align: 'center'},
                    { title: '最后回应', key: 'recent', width: 110, align: 'center'},
                    { title: '详情', width: 150, align: 'center',
                        render: (h, params) => {
                            return h('div', [
                                h('Button', {
                                    props: { type: 'primary', size: 'small'},
                                    style: { marginRight: '5px'},
                                    on: {
                                        click: () => {
                                            this.showDetail(params.index)
                                        }
                                    }
                                }, '简述'),
                                h('Button', {
                                    props: { type: 'success', size: 'small'},
                                    style: { marginRight: '5px'},
                                    on: {
                                        click: () => {
                                            this.openSource(params.index)
                                        }
                                    }
                                }, '原址')
                            ]);
                          }
                    }
                ]
            }
        },
        computed: {
          current: {
            set: function (value) {
              this.$store.commit('setCurrent', value)
            },
            get: function () {
              return this.$store.state.app.current
            }
          },
          ...mapState({
              rent: state => state.app.rent,
              loading: state => state.app.loading,
              number: state => state.app.number
          })
        },
        methods: {
            showDetail (index) {
                ajax.getDetail({topic_id: this.rent[index]['topic_id']}).then((res)=>{
                    this.$Modal.info({
                      title: '租房信息简述',
                      content: res.data.detail['detail'],
                      width: 650
                    })
                });
            },
            openSource(index){
              window.open(this.rent[index]['title_link'])
            },
            changePage(page){
              console.log(this.current);
              let params = {
                  place: this.$store.state.app.place,
                  idx: this.$store.state.app.idx
              };
              params['page'] = page;
              this.$store.commit('setLoading', true);
              ajax.getRent(params).then((res)=>{
                  this.$store.commit('setNumber', res.data['number']);
                  this.$store.commit('setRent', res.data['rent']);
                  this.$store.commit('setLoading', false);
              })
            }
        }
    }
</script>
<style scoped>
  .datalist {
    margin: 15px;
  }
  #page {
    text-align: center;
  }
</style>
