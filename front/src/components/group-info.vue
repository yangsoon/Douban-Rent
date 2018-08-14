<template>
  <div>
    <div class="datalist">
      <Table border :columns="column" :data="rent" v-if="rent"></Table>
    </div>
    <Page :total="100" />
  </div>
</template>
<script>
    import ajax from '@/ajax'
    export default {
        data () {
            return {
                column: [
                    { title: '标题', key: 'title_text', width: 450},
                    { title: '作者', key: 'author_name', width: 110, align: 'center'},
                    { title: '评论数', key: 'comment_num',align: 'center'},
                    { title: '最后回应', key: 'recent', width: 110, align: 'center'},
                    { title: '发帖时间', key: 'add_time', width: 180, align: 'center'},
                    { title: '详情',  key: 'action',
                      width: 150, align: 'center',
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
                ],
            }
        },
        computed: {
          rent(){
            return this.$store.state.app.rent
          }
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
              windows.open(this.rent[index]['title_link'])
            }
        }
    }
</script>
<style scoped>
  .datalist {
    margin: 15px;
  }
</style>
