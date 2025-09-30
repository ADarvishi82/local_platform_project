// src/boot/google-login-init.js
import { boot } from 'quasar/wrappers'
import vue3GoogleLogin from 'vue3-google-login'

const GOOGLE_CLIENT_ID = '279929399898-ir6jp70mc46v6pjojnrdl2veg3ta44h2.apps.googleusercontent.com';

export default boot(({ app }) => {
  if (!GOOGLE_CLIENT_ID || GOOGLE_CLIENT_ID.includes('YOUR_GOOGLE_CLIENT_ID')) {
    console.warn('Google Client ID for vue3-google-login is not configured.');
    return;
  }

  app.use(vue3GoogleLogin, {
    clientId: GOOGLE_CLIENT_ID
  })
  console.log("vue3-google-login initialized.");
})
