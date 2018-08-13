<template>
    <div>
      <group-header @change-route="change"></group-header>
      <router-view></router-view>
    </div>
</template>

<script>
    import groupHeader from "./group-header"
    export default {
      name: "group-content",
      components:{
          groupHeader
        },
      created(){
        this.$router.push({name: 'info'})
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
