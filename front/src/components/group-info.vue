<template>
  <div>
    <div class="datalist"  v-if="rent">
      <Table border :columns="column" :data="rent" :loading="loading"></Table>
    </div>
    <div v-if="number">
      <Page id="page" :current.sync="current" :total="number" :page-size="25" @on-change="changePage"/>
    </div>
    <Modal v-model="show" scrollable :closable="false" width="700">
      <Alert show-icon> <h3>{{title}}</h3>
        <Icon type="ios-bulb-outline" slot="icon"></Icon>
      </Alert>
      <div v-html="detail" style="margin: 10px; font-size: 15px;"></div>
      <div slot="footer">
        <Button type="primary" @click="del">确定</Button>
      </div>
    </Modal>
  </div>
</template>
<script>
    import ajax from '@/ajax'
    import { mapState } from 'vuex'
    export default {
        data () {
            return {
                show: false,
                title: null,
                detail: null,
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
                    { title: '回应数', key: 'comment_num',width: 100, align: 'center'},
                    { title: '最后回应', key: 'recent', width: 110, align: 'center'},
                    { title: '详情', width: 150, align: 'center',
                        render: (h, params) => {
                            return h('div', [
                                h('Button', {
                                    props: { type: 'primary', size: 'small', disabled: !params.row.add_time},
                                    style: { marginRight: '5px'},
                                    on: {
                                        click: () => {
                                            this.showDetail(params.index)
                                        }
                                    },
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
            del(){
              this.show = false;
            },
            showDetail (index) {
                ajax.getDetail({topic_id: this.rent[index]['topic_id']}).then((res)=>{
                    this.title = this.rent[index]['title_text'];
                    this.show = true;
                    if(res.data.detail['detail'].length === 0){
                        this.detail = `<br>信息不完整请点击<strong>`+
                                       `<a href='https://www.douban.com/group/topic/${this.rent[index]['topic_id']}/'`+
                                       ` target="_blank">原址</a>` +
                                       `</strong>查看详情`;
                    }
                    else{
                        this.detail = res.data.detail['detail']
                    }
                });
            },
            openSource(index){
              window.open(this.rent[index]['title_link'])
            },
            changePage(page){
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
