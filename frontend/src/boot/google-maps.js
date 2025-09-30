// src/boot/google-maps.js
import { boot } from 'quasar/wrappers';
// به جای default یا named import، همه چیز را به صورت یک namespace وارد کن
import * as VueGoogleMapAll from 'vue3-google-map';

const GOOGLE_MAPS_API_KEY = 'AIzaSyDnWWhRvds75DoC8HIVwhq4rAlzZQkGGrI';

export default boot(({ app }) => {
  // برای دیباگ، ببینیم چه چیزی داخل VueGoogleMapAll است
  console.log("VueGoogleMap exports:", VueGoogleMapAll);

  // کتابخانه ممکن است پلاگین را در یک پراپرتی default داخل این آبجکت قرار دهد
  const VueGoogleMap = VueGoogleMapAll.default || VueGoogleMapAll;

  if (!GOOGLE_MAPS_API_KEY || GOOGLE_MAPS_API_KEY === 'YOUR_GOOGLE_MAPS_API_KEY') {
    console.warn('Google Maps API Key is not configured.');
    return;
  }

  // حالا از متغیر VueGoogleMap استفاده کن
  app.use(VueGoogleMap, {
    load: {
      key: GOOGLE_MAPS_API_KEY,
      libraries: "places,geocoding",
    },
  });
  console.log("Attempted to register Google Maps plugin.");
});
