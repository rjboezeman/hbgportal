import { Notify } from 'quasar'

export function notifyNow (message) {
  Notify.create({
    message: message,
    caption: 'Reload the page to try again',
    color: 'negative'
  })
}
