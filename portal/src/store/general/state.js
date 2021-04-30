export default function () {
  return {
    username: '',
    firstName: '',
    lastName: '',
    email: '',
    forgotEmail: '',
    password: '',
    samePassword: false,
    validationCode: null,
    resetCode: '',
    resetCodeStatus: 0,
    statusMessage: '',

    reqURLs: {
      api: process.env.API.replace(/^"(.+(?="$))"$/, '$1')
    },
    reqSlugs: {
      csrf: {
        name: 'set-csrf',
        method: 'GET'
      },
      createAccount: {
        name: 'create',
        method: 'POST'
      },
      validateEmail: {
        name: 'validate',
        method: 'POST'
      },
      forgotEmailSend: {
        name: 'forgot',
        method: 'POST'
      },
      changePassword: {
        name: 'passwordreset',
        method: 'POST'
      },
      validResetCode: {
        name: 'reset',
        method: 'POST'
      }
    },

    requestOptions: {
      method: 'GET',
      mode: 'cors',
      cache: 'no-cache',
      credentials: 'include', // same-origin, omit, include: see https://javascript.info/fetch-crossorigin
      referrerPolicy: 'no-referrer',
      headers: { // 'Content-Type': 'text/plain',
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    }
  }
}
