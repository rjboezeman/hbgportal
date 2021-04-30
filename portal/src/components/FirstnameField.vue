<template>
  <q-input
  clearable
  filled
  label="first name"
  v-model='firstname'
  name='firstname'
  ref='firstname'
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
      default: 'First name'
    },
    firstnameField: {
      type: String,
      default: 'firstname'
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
      firstname: ''
    }
  },
  computed: {
    noSpecialChars: function () {
      const re = /[0-9`~!@#$%^&*()|+=?;:",.<>{}[\]/]/
      return re.test(this.firstname)
    }
  },
  methods: {
  }
}
</script>
