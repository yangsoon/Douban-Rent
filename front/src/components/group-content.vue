<template>
    <div>
      <group-header @change-route="change"></group-header>
      <keep-alive>
        <router-view></router-view>
      </keep-alive>
    </div>
</template>

<script>
    import groupHeader from "./group-header"
    export default {
      name: "group-content",
      components:{
          groupHeader
        },
      methods:{
        change(name){
          this.$router.push({name: name.name})
        }
      }
    }
</script>

<style scoped>

</style>
