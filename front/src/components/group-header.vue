<template>
  <Menu mode="horizontal" active-name="info" @on-select="transfer">
      <MenuItem name="info">
          <Icon type="ios-paper" />
          租房信息
      </MenuItem>
      <MenuItem name="filter">
          <Icon type="ios-construct" />
          条件过滤
      </MenuItem>
      <MenuItem name="analysis">
          <Icon type="ios-stats" />
          统计分析
      </MenuItem>
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
