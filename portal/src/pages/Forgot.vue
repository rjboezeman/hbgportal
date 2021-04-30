<template>
  <q-page class="row q-pa-xs" padding>
    <q-space/>
        <q-card bordered class="col-3 column self-center q-pa-sm bg-grey-2 shadow-1 minwidth">
          <div class="text-h6 text-size-md text-grey-9 q-ml-md q-mt-md">Type your email address:</div>
          <q-card-section>
            <q-form>
              <email-field />
            </q-form>
          </q-card-section>
          <q-card-actions class="row justify-center q-px-md">
            <q-btn style="min-width: 100px;" class="flex" unelevated color="deep-orange" size="lg" label="OK" />
            <q-space/>
            <q-btn style="min-width: 100px;" class="flex text-grey-9" unelevated color="warning" size="lg" label="Resend"  />
            <q-btn style="min-width: 100px;" class="flex" unelevated color="primary" size="lg" label="Back" to="/login" />
          </q-card-actions>
        </q-card>
      <q-space/>
  </q-page>
</template>

<script>
import EmailField from '../components/EmailField.vue'
export default {
  components: {
    EmailField
  }
  // name: 'PageName',
}
</script>
