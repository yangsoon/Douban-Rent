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
                    <BreadcrumbItem>Home</BreadcrumbItem>
                    <BreadcrumbItem>Components</BreadcrumbItem>
                    <BreadcrumbItem>Layout</BreadcrumbItem>
                </Breadcrumb>
                <Content :style="{padding: '15px 0',background: '#fff'}">
                    <Layout>
                        <Sider hide-trigger :style="{background: '#fff'}">
                            <Menu active-name="1-2" theme="light" width="auto" :open-names="['1']">
                                <Submenu name="1">
                                    <template slot="title">
                                        <Icon type="ios-navigate"></Icon>
                                        Item 1
                                    </template>
                                    <MenuItem name="1-1">Option 1
                                    </MenuItem>
                                    <MenuItem name="1-2">Option 2</MenuItem>
                                    <MenuItem name="1-3">Option 3</MenuItem>
                                </Submenu>
                                <Submenu name="2">
                                    <template slot="title">
                                        <Icon type="ios-keypad"></Icon>
                                        Item 2
                                    </template>
                                    <MenuItem name="2-1">Option 1</MenuItem>
                                    <MenuItem name="2-2">Option 2</MenuItem>
                                </Submenu>
                                <Submenu name="3">
                                    <template slot="title">
                                        <Icon type="ios-analytics"></Icon>
                                        Item 3
                                    </template>
                                    <MenuItem name="3-1">Option 1</MenuItem>
                                    <MenuItem name="3-2">Option 2</MenuItem>
                                </Submenu>
                            </Menu>
                        </Sider>
                        <Content :style="{padding: '5px',minHeight: '650px', background: '#fff'}">
                          <router-view></router-view>
                        </Content>
                    </Layout>
                </Content>
            </Layout>
            <Footer class="layout-footer-center">2018 &copy; Douban-Rent</Footer>
        </Layout>
    </div>
</template>
<script>
    export default {
      created(){
        this.$router.push('/group')
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
