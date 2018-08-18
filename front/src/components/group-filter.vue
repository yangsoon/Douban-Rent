<template>
  <div class="filter">
      <Modal v-model="show" scrollable :closable="false" width="700">
        <Alert show-icon> <h3>{{title}}</h3>
          <Icon type="ios-bulb-outline" slot="icon"></Icon>
        </Alert>
        <div v-html="detail" style="margin: 10px; font-size: 15px;"></div>
        <div slot="footer">
          <Button type="primary" @click="del">确定</Button>
        </div>
      </Modal>
      <Card style="padding: 2px 0px">
          <Row type="flex" justify="center" align="middle">
              <Col span="11">
                  <Form>
                      <FormItem label="小组选择">
                          <CheckboxGroup v-model="selected_groups" v-if="places" size="large">
                              <Checkbox v-for="item in active_groups" :label="item" :key="item">
                                {{ map_place[place+'-'+item ]}}
                              </Checkbox>
                          </CheckboxGroup>
                      </FormItem>
                      <FormItem label="性别限制">
                          <RadioGroup size="large" v-model="gender">
                              <Radio :label="1">男</Radio>
                              <Radio :label="0">女</Radio>
                              <Radio :label="2">不限</Radio>
                          </RadioGroup>
                      </FormItem>
                      <FormItem label="关键字搜索">
                          <Input search enter-button placeholder="输入关键字, 比如: 北航"
                                 @on-search="search" v-model="key_word" size="large"></Input>
                      </FormItem>
                  </Form>
              </Col>
              <Col span="11" offset="1">
                  <Alert show-icon>
                      <p style="margin-bottom: 5px">关于</p>
                      <Icon type="ios-bulb-outline" slot="icon"></Icon>
                      <template slot="desc">
                        1. 如果过滤时限制性别，搜索结果有限，可以先选择不限性别 <br>
                        2. 进行关键字搜索时，希望你能使用一些常用的缩略词代替，
                        比如用北航代替北京航空航天大学，使用北邮之类的词。
                      </template>
                  </Alert>
              </Col>
          </Row>
        </Card>
      <Row>
        <Divider>筛选结果</Divider>
        <Table v-if="rent" border :columns="column" :data="rent"></Table>
      </Row>
  </div>
</template>
<script>
    import { mapState } from 'vuex'
    import ajax from '@/ajax'
    export default {
        data(){
            return{
              selected_groups: [],
              gender: 2,
              rent: null,
              key_word: '',
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
                    { title: '发帖时间', key: 'add_time', width: 175, align: 'center'},
                    { title: '回应数', key: 'comment_num',width: 86, align: 'center'},
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
        computed:{
            ...mapState({
                place: state => state.app.place,
                places: state => state.app.places,
                map_place: state => state.app.map_place
            }),
            active_groups(){
              let groups = [];
              for(let place in this.places[this.place]){
                groups.push(place)
              }
              this.selected_groups = groups;
              return groups
            }
        },
        methods: {
            search(){
                if(!this.key_word&&this.gender===2){
                    this.$Notice.error({
                      title: "筛选参数错误",
                      desc: "请选择一个性别限制或者输入关键字"
                    })
                }
                else {
                    let params = {
                        place: this.place,
                        groups: this.selected_groups.join('-'),
                        gender: this.gender,
                        key_word: this.key_word
                    };
                    ajax.filterRent(params).then((res)=>{
                        this.rent = res.data['rent']
                    })
                }
            },
            openSource(index){
                window.open(this.rent[index]['title_link'])
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
            del(){
                this.show = false;
            },
        }
    }
</script>
<style scoped>
.filter{
  margin: 25px;
}
</style>
