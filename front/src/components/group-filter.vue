<template>
  <div class="filter">
      <Card style="padding: 5px">
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
                      关于
                      <Icon type="ios-bulb-outline" slot="icon"></Icon>
                      <template slot="desc">
                        进行关键字搜索时，希望你能使用一些常用的缩略词代替，<br>
                        比如用北航代替北京航空航天大学，使用北邮之类的词。
                      </template>
                  </Alert>
              </Col>
          </Row>
        </Card>
      <Row>
        <Divider>筛选结果</Divider>
        <Table></Table>
      </Row>

  </div>

</template>
<script>
    import { mapState } from 'vuex'
    export default {
        data(){
            return{
              selected_groups: [],
              gender: 2,
              key_word: null
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

              }
          }
        }
    }
</script>
<style scoped>
.filter{
  margin: 25px;
}
</style>
