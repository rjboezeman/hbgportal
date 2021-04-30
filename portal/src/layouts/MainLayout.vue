<template>
  <q-layout class="" view="hHh LpR fFf">
    <q-header class="flex column transparent" elevated  height-hint="88">
      <div class="row flex-grow justify-center">
        <heartbeat-games-logo class="q-my-lg flex" />
      </div>
    <q-toolbar class="bg-primary text-white shadow-2">
      <q-btn flat round dense icon="menu" @click="left = !left" class="q-mr-sm" />
      <q-separator dark vertical inset />
      <q-btn stretch flat label="Home" to="/" />
      <q-separator dark vertical inset />
      <q-btn stretch flat label="Login" color="secondary" to="/login"/>
      <q-separator dark vertical inset />
      <q-btn stretch flat label="Register" to="/register"/>
      <q-space />

      <q-btn-dropdown stretch flat label="About">
        <q-list>
          <q-item-label header>Folders</q-item-label>
          <q-item v-for="n in 3" :key="`x.${n}`" clickable v-close-popup tabindex="0">
            <q-item-section avatar>
              <q-avatar icon="folder" color="secondary" text-color="white" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Photos</q-item-label>
              <q-item-label caption>February 22, 2016</q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-icon name="info" />
            </q-item-section>
          </q-item>
          <q-separator inset spaced />
          <q-item-label header>Files</q-item-label>
          <q-item v-for="n in 3" :key="`y.${n}`" clickable v-close-popup tabindex="0">
            <q-item-section avatar>
              <q-avatar icon="assignment" color="primary" text-color="white" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Vacation</q-item-label>
              <q-item-label caption>February 22, 2016</q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-icon name="info" />
            </q-item-section>
          </q-item>
        </q-list>
      </q-btn-dropdown>
    </q-toolbar>
    </q-header>

    <q-drawer v-model="left" side="left" elevated class="bg-blue-5" >
      <!-- drawer content -->
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer reveal elevated class="bg-grey-8 text-white">
      <q-toolbar>
        <q-toolbar-title>
          <q-avatar>
            <img src="~assets/HBbird.png">
          </q-avatar>
          Title
        </q-toolbar-title>
      </q-toolbar>
    </q-footer>
  </q-layout>
</template>

<script>
import HeartbeatGamesLogo from '../components/HeartbeatGamesLogo.vue'
import Vesto from '../assets/NpcVesto.png'
export default {
  components: { HeartbeatGamesLogo },
  data () {
    return {
      left: false,
      vesto: Vesto
    }
  }
}
</script>
<style scoped>
.picbg {
  background-image: url("~assets/Wallpaper_AardeWoestijn.jpg");
  background-repeat: no-repeat;
}
</style>
