<template>
  <q-page class="row q-pa-xs" padding>
    <q-space/>
        <q-card bordered class="col-3 column self-center q-pa-sm bg-grey-2 shadow-1 minwidth">
          <div class="text-h6 text-size-md text-grey-9 q-ml-md q-mt-md">Please fill in your details:</div>
          <q-card-section>
            <q-form>
              <firstname-field />
              <lastname-field />
              <email-field />
              <password-field />
            </q-form>
          </q-card-section>
          <q-card-actions class="row justify-evenly q-px-md">
            <q-btn style="min-width: 100px;" class="flex" unelevated color="deep-orange" size="lg" label="Register" />
            <q-btn style="min-width: 100px;" class="flex" unelevated color="primary" size="lg" label="Back" to="/login" />
          </q-card-actions>
        </q-card>
      <q-space/>
  </q-page>
</template>

<script>
import EmailField from '../components/EmailField.vue'
import FirstnameField from '../components/FirstnameField.vue'
import LastnameField from '../components/LastnameField.vue'
import PasswordField from '../components/PasswordField.vue'

export default {
  // name: 'PageName',
  components: {
    EmailField,
    FirstnameField,
    LastnameField,
    PasswordField
  },
  data: function () {
    return {
      firstname: '',
      lastname: '',
      email: '',
      password: '',
      passwordagain: ''
    }
  }
}
</script>
