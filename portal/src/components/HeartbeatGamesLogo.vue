<template>
<q-card  bordered class="flex flex-center q-gutter-xs q-px-lg hbglogo bg-blue-9">
  <q-card-section  horizontal >
    <q-card-section class=" col-4 flex q-pa-md">
      <q-img
        class="contain"
        :src="hbglogo"
      />
    </q-card-section>
    <q-card-section class="flex q-pa-md">
      <div class="text-orange-8 text-h3 text-weight-medium  q-pa-none heartbeat">Heartbeat</div>
      <div class="text-orange-6 text-h4 text-weight-medium   q-pa-none heartbeat">Games</div>
    </q-card-section>
  </q-card-section>
</q-card>
</template>
<script>
import hbglogo from '../assets/HBbird.png'

export default {

  data: function () {
    return {
      hbglogo: hbglogo
    }
  }
}
</script>
<style>
<style scoped>
.hbglogo {
  max-width: 350px;
}

.heartbeat {
  text-shadow:1px 1px 5px rgb(66, 66, 66), 0 0 0.01em  rgb(66, 66, 66), 0 0 1em  rgb(66, 66, 66);
}
</style>
