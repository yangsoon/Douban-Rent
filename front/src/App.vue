<template>
    <div class="layout">
        <Layout>
            <Header>
                <Menu mode="horizontal" theme="dark" active-name="index">
                    <div class="layout-logo">
                      <h2 style="color: white; line-height: 35px;">
                        豆瓣租房
                      </h2>
                    </div>
                    <div class="layout-nav">
                      <MenuItem name="index">
                        <Icon type="ios-navigate" size="24"></Icon>
                        首页
                      </MenuItem>
                      <MenuItem name="github">
                        <Icon type="logo-github" size="24"></Icon>
                        GitHub
                      </MenuItem>
                      <MenuItem name="beg">
                        <Icon type="ios-thumbs-up-outline" size="24"></Icon>
                        打赏
                      </MenuItem>
                    </div>
                </Menu>
            </Header>
            <Layout :style="{padding: '0 50px'}">
                <Breadcrumb :style="{margin: '16px 0'}">
                    <BreadcrumbItem>主页</BreadcrumbItem>
                    <BreadcrumbItem v-if="act_name">{{ act_place }}</BreadcrumbItem>
                    <BreadcrumbItem v-if="act_name">{{ map_place[act_name] }}</BreadcrumbItem>
                </Breadcrumb>
                <Content :style="{padding: '15px 0',background: '#fff'}">
                    <Layout>
                        <Sider hide-trigger :style="{background: '#fff'}">
                            <Menu v-if="places" :active-name="act_name" theme="light" width="auto" :open-names="open_names"
                            @on-select="changePlace">
                                <Submenu v-for="(items, place) in places" :name="place" :key="place">
                                    <template slot="title">
                                        <Icon type="ios-navigate"></Icon>
                                        {{ map_place[place] }}
                                    </template>
                                    <MenuItem :name="place+'-'+idx" v-for="(url, idx) in items" :key="idx">
                                      {{ map_place[place+'-'+idx]}}
                                    </MenuItem>
                                </Submenu>
                            </Menu>
                        </Sider>
                        <Content :style="{padding: '5px',minHeight: '650px', background: '#fff'}">
                          <keep-alive>
                            <router-view></router-view>
                          </keep-alive>
                        </Content>
                    </Layout>
                </Content>
            </Layout>
            <Footer class="layout-footer-center">2018 &copy; Douban-Rent</Footer>
        </Layout>
    </div>
</template>
<script>
    import ajax from "@/ajax"
    export default {
        mounted(){
            this.$Spin.show();
            ajax.getPlace().then((res)=>{
                this.$Spin.hide();
                this.places = res.data['urls'];
                this.map_place = res.data['map_place'];
                this.init(res.data['urls']);
            });

        },
        data(){
            return {
              places: null,
              map_place: null,
              act_name: null,
              open_names: []
            }
        },
        computed: {
          act_place(){
              let place = this.act_name.split('-')[0];
              return this.map_place[place]
          }
        },
        methods:{
            init(places){
                for (let i in places){
                  this.open_names.push(i)
                }
                this.act_name = this.open_names[0] + '-' + '1';
                let params = {place:this.open_names[0], idx:'1'};
                this.$store.commit("setPlace", params);
                this.fetchRent(params);
            },
        changePlace(name){
            let result = name.split('-');
            let params = {place: result[0], idx: result[1]};
            this.$store.commit('setPlace', params);
            this.fetchRent(params);
            this.act_name = name
        },
        fetchRent(params){
            this.$store.commit('setLoading', true);
            params['page'] = 1;
            ajax.getRent(params).then((res)=>{
                this.$store.commit('setRent', res.data['rent']);
                this.$store.commit('setNumber', res.data['number']);
                this.$router.push('/group/info');
                this.$store.commit('setLoading', false);
                this.$store.commit('setCurrent', 1)
            });
        }
      }
    }
</script>
<style scoped>
.layout{
    border: 1px solid #d7dde4;
    background: #f5f7f9;
    position: relative;
    border-radius: 4px;
    overflow: hidden;
}
.layout-logo{
    width: 100px;
    height: 30px;
    border-radius: 3px;
    float: left;
    position: relative;
    top: 15px;
    left: 40px;
    text-align: center;
}
.layout-nav{
    width: 420px;
    margin: 0 auto;
    margin-right: 5px;
}
.layout-footer-center{
    text-align: center;
}
</style>
