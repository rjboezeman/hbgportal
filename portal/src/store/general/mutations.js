
export function updateStatusMessage (state, message) {
  console.log('updateStatusMessage running')
  console.log('sessionURL: ' + state.reqURLs.session)
  state.statusMessage = message
}
