var hbgMixins = {
  computed: {
    statusMessage: {
      get () {
        return this.$store.state.general.statusMessage
      },
      set (msg) {
        this.$store.state.general.statusMessage = msg
      }
    },
    errorMessage: {
      get () {
        return this.$store.state.general.errorMessage
      },
      set (msg) {
        this.$store.state.general.errorMessage = msg
      }
    },
    noSpecialChars: function () {
      const re = /[0-9`~!@#$%^&*()|+=?;:",.<>{}[\]/]/
      return re.test(this.firstname)
    }
  },
  methods: {
    clearVars: function () {
      this.$store.state.account.username = ''
      this.$store.state.account.password = ''
      this.$store.state.account.firstname = ''
      this.$store.state.account.lastname = ''
      this.$store.state.general.statusMessage = ''
      this.$store.state.general.errorMessage = ''
    },
    needSession: function () {
      return new Promise((resolve, reject) => {
        console.debug('needSession(): started!')
        this.$store.commit('sessionLoad')
        console.debug('needSession(): sessionHeader: \'' + this.getSessionStorage('sessionHeader') + '\', sessionId: \'' + this.getSessionStorage('sessionId') + '\', loggedIn: ' + this.getSessionStorage('loggedIn'))

        if (this.getSessionStorage('sessionId') == null) {
          // no session yet
          console.debug('needSession(): no session yet, dispatching one...')
          this.$store.dispatch('retrieveSession')
            .then(result => {
              console.debug('needSession(): retrieved the following: ' + JSON.stringify(result))
              if (this.getSessionStorageBoolean('loggedIn') && this.getSessionStorageBoolean('validEmail')) {
                // apparently, we are already logged in, routing to portal
                reject()
                this.$router.push({ name: 'portalhome' })
              }
              resolve()
            },
            error => {
              this.errorMessage = error.message
              console.error('needSession(): ' + error)
              reject(error)
            })
            .finally(() => {
            })
        }
        else if (this.getSessionStorageBoolean('loggedIn') && this.getSessionStorageBoolean('validEmail')) {
          // already logged in
          console.debug('needSession(): already logged in, email address validated rerouting to portal...')
          reject()
          this.$router.push({ name: 'portalhome' })
        }
        else {
          // session present, not logged in
          console.debug('needSession(): session present, not logged in')
          resolve()
        }
        console.debug('needSession(): finished')
      })
    }
  }
}

export default hbgMixins
