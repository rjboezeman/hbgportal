<template>
    <q-input
    v-model="password"
    label="password"
    filled
    :type="isPwd ? 'password' : 'text'">
      <template v-slot:prepend>
        <q-icon name="password" />
      </template>
      <template v-slot:append>
        <q-icon
          :name="isPwd ? 'visibility_off' : 'visibility'"
          class="cursor-pointer"
          @click="isPwd = !isPwd"
        />
      </template>
    </q-input>
</template>

<script>
export default {
  // name: 'ComponentName',
  data () {
    return {
      password: '',
      isPwd: true
    }
  }
}
</script>
