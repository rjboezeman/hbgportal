import { Notify } from 'quasar'

export function getCSRFToken (context) {
  return new Promise((resolve, reject) => {
    console.debug('getCSRFToken(): starting...')

    context.dispatch('general/callAPI', { apicall: 'api', slug: 'csrf' }, { root: true })
      .then(
        result => {
          console.debug('getCSRFToken (): retrieved the following: ' + JSON.stringify(result))
          resolve()
        },
        error => {
          this.statusMessageStyle = this.errorStyle
          console.error('getCSRFToken (): ' + error.message)
          Notify.create({
            message: error.message,
            caption: 'Just now',
            color: 'secondary'
          })
          reject(error)
        }
      )
      .catch(
        error => {
          console.error('getCSRFToken (): ' + error.message)
          reject(error)
        }
      )
  })
}
