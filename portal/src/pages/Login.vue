<template>
  <q-page class="row q-pa-xs" padding>
    <q-space/>
        <q-card bordered class="col-3 column self-center q-pa-sm bg-grey-2 shadow-1 minwidth">
          <div class="text-h6 text-size-md text-grey-9 q-ml-md q-mt-md">Please login:</div>
          <q-card-section>
            <q-form>
              <email-field />
              <password-field />
            </q-form>
          </q-card-section>
          <q-card-actions class="row justify-center q-px-md">
            <q-btn style="min-width: 100px;" class="flex" unelevated color="deep-orange" size="lg" label="Login" />
            <q-space/>
            <q-btn style="min-width: 100px;" class="flex" unelevated color="primary" size="lg" label="Register" to="/register" />
            <q-btn style="min-width: 100px;" class="flex" unelevated color="primary" size="lg" label="Forgot" to="/forgot" />
          </q-card-actions>
        </q-card>
      <q-space/>
  </q-page>
</template>

<script>
import EmailField from '../components/EmailField.vue'
import PasswordField from '../components/PasswordField.vue'

export default {
  components: {
    EmailField,
    PasswordField
  },
  name: 'LoginPage',

  data: function () {
    return {
      email: '',
      password: ''
    }
  }
}
</script>
<style scoped>
.minwidth {
  width: 25%;
  min-width: 350px;
}
</style>
