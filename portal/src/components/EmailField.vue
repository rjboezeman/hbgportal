<template>
  <q-input filled
    v-model="email"
    type="email"
    label="email"
    bottom-slots
    :error="!isValidEmail"
    error-message="Please type a valid email address" >
           <template v-slot:prepend>
          <q-icon name="email" />
        </template>
  </q-input>
</template>
<script>
export default {
  props: {
    emailField: {
      default: ''
    },
    moduleValue: {
      default: 'account'
    }
  },
  data: function () {
    return {
      tmpEmail: ''
    }
  },
  computed: {
    email: {
      get () {
        return this.tmpEmail
        // return this.$store.state[this.moduleValue][this.emailField];
      },
      set (value) {
        this.tmpEmail = value.toLowerCase()
        if (this.validEmail(value)) {
          this.$store.state[this.moduleValue][this.emailField] = value.toLowerCase()
        }
        else {
          this.$store.state[this.moduleValue][this.emailField] = ''
        }
      }
    },
    isValidEmail () {
      return this.validEmail(this.tmpEmail)
    }
  },
  methods: {
    validEmail: function (email) {
      if (email === '') {
        return true
      }
      else {
        var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        // var re = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/;   //simpler one?
        console.log('Email address: ' + re.test(email))
        return re.test(email)
      }
    }
  }
}
</script>
