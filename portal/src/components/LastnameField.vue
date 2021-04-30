<template>
  <q-input
  filled
  clearable
  label="last name"
  v-model='lastname'
  name='lastname'
  :error="noSpecialChars"
  error-message="No special characters"
  type='text' >
         <template v-slot:prepend>
          <q-icon name="face" />
        </template>
  </q-input>
</template>
<script>
export default {
  props: {
    pholder: {
      type: String,
      default: 'Last name'
    },
    lastnameField: {
      type: String,
      default: 'lastname'
    },
    moduleValue: {
      type: String,
      default: 'account'
    }
  },
  mixins: {
  },
  data: function () {
    return {
      lastname: ''
    }
  },
  computed: {
    noSpecialChars: function () {
      const re = /[0-9`~!@#$%^&*()|+=?;:",.<>{}[\]/]/
      return re.test(this.lastname)
    }
  },
  methods: {
  }
}
</script>
