<template>
  <div>
    <div class="datalist">
      <Table border :columns="columns7" :data="data6"></Table>
    </div>
    <Page :total="100" />
  </div>
</template>
<script>
    export default {
        data () {
            return {
                columns7: [
                    {
                        title: '标题',
                        key: 'text',
                    },
                    {
                        title: '作者',
                        key: 'auth'
                    },
                    {
                        title: '评论数',
                        key: 'comment'
                    },
                    {
                        title: '最后回应',
                        key: 'recent'
                    },
                    {
                        title: '详情',
                        key: 'action',
                        width: 150,
                        align: 'center',
                        render: (h, params) => {
                            return h('div', [
                                h('Button', {
                                    props: {
                                        type: 'primary',
                                        size: 'small'
                                    },
                                    style: {
                                        marginRight: '5px'
                                    },
                                    on: {
                                        click: () => {
                                            this.show(params.index)
                                        }
                                    }
                                }, '简述'),
                                h('Button', {
                                    props: {
                                        type: 'success',
                                        size: 'small'
                                    },
                                    style: {
                                        marginRight: '5px'
                                    },
                                    on: {
                                        click: () => {
                                            this.show(params.index)
                                        }
                                    }
                                }, '原址')
                            ]);
                        }
                    }
                ],
                data6: [
                    {
                        text: 'John Brown',
                        auth: 18,
                        comment: 'New York No. 1 Lake Park',
                        recent: '08-13 14:56'
                    },
                    {
                        text: 'John Brown',
                        auth: 18,
                        comment: 'New York No. 1 Lake Park',
                        recent: '08-13 14:56'
                    }
                ]
            }
        },
        methods: {
            show (index) {
                this.$Modal.info({
                    title: 'User Info',
                    content: `Name：${this.data6[index].name}<br>Age：${this.data6[index].age}<br>Address：${this.data6[index].address}`
                })
            },
            remove (index) {
                this.data6.splice(index, 1);
            }
        }
    }
</script>
<style scoped>
  .datalist {
    margin: 15px;
  }
</style>
