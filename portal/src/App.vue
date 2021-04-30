<template>
  <div id="q-app" class="picbg">
    <router-view />
  </div>
</template>
<script>
export default {
  name: 'App',

  mounted () {
    console.debug('App/mounted(): Started.')
    this.$store.dispatch('session/getCSRFToken')
    console.debug('App/mounted(): Finished')
  }
}
</script>
<style scoped>
.picbg {
  background-image: url("~assets/Wallpaper_AardeWoestijn.jpg");
  background-repeat: no-repeat;
}
</style>
