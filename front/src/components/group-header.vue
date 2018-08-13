<template>
  <Menu mode="horizontal" active-name="1" @on-select="transfer">
      <MenuItem name="info">
          <Icon type="ios-paper" />
          租房信息
      </MenuItem>
      <MenuItem name="filter">
          <Icon type="ios-construct" />
          条件过滤
      </MenuItem>
      <Submenu name="analysis">
          <template slot="title">
              <Icon type="ios-stats" />
              统计分析
          </template>
          <MenuGroup title="使用">
              <MenuItem name="3-1">新增和启动</MenuItem>
              <MenuItem name="3-2">活跃分析</MenuItem>
              <MenuItem name="3-3">时段分析</MenuItem>
          </MenuGroup>
          <MenuGroup title="留存">
              <MenuItem name="3-4">用户留存</MenuItem>
              <MenuItem name="3-5">流失用户</MenuItem>
          </MenuGroup>
      </Submenu>
  </Menu>
</template>

<script>
    export default {
        name: "group-header",
        methods:{
          transfer(name){
            this.$emit('change-route', {name: name})
          }
        }
    }
</script>

<style scoped>

</style>
