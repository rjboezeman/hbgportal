export function callAPI (context, { apicall, slug, body }) {
  return new Promise((resolve, reject) => {
    console.debug('callAPI(' + slug + '): starting...')
    // POST request using fetch with error handling
    var requestOptions = JSON.parse(JSON.stringify(context.state.requestOptions)) // deep copy JSON, otherwise use {...obj} which is the spread operator for shallow copies

    var apiURL = context.state.reqURLs[apicall] + context.state.reqSlugs[slug].name
    requestOptions.method = context.state.reqSlugs[slug].method
    if ((requestOptions.method !== 'HEAD') && (requestOptions.method !== 'GET')) {
      requestOptions.body = JSON.stringify(body)
    }

    console.debug('callAPI(' + slug + '): calling ' + apiURL + ' with method ' + context.state.reqSlugs[slug].method)
    fetch(apiURL, requestOptions) // and we signal the server to do the same
      .then(async response => {
        const data = await response.json()
        context.commit('sessionUpdate', data)
        console.debug('callAPI(' + slug + '):  output:  ' + JSON.stringify(data))
        // check for error response
        if (!response.ok) {
          // get error message from body or default to response status
          var error = {
            status: response.status,
            message: 'An ERROR occured'
          }
          if (data && data.message) {
            error.message = data.message
          }
          console.debug('callAPI(' + slug + '): Something went wrong: ' + JSON.stringify(error))
          context.commit('updateStatusMessage', error.message)
          reject(error)
        }
        else
        {
          console.debug('callAPI(' + slug + '): API call completed OK')
          resolve(data)
        }
      })
      .catch(error => {
        context.commit('updateStatusMessage', 'Error: could not contact Heartbeat Games!')
        console.error('ERROR: ', error)
        reject(error)
      })
  })
} // call API
