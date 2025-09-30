// src/boot/auth-loader.js
import { boot } from 'quasar/wrappers';
import { useAuthStore } from 'stores/auth-store';

export default boot(async ({ store }) => { // 'store' در اینجا نمونه Pinia است
  const authStoreInstance = useAuthStore(store); // پاس دادن نمونه Pinia به store
                                                // این کار باعث می‌شود authStoreInstance به همان نمونه Pinia متصل شود
                                                // که توسط اپلیکیشن اصلی استفاده می‌شود.

  // هنگام بارگذاری اپلیکیشن، وضعیت احراز هویت را از LocalStorage چک کن
  authStoreInstance.checkAuthOnLoad();

  console.log("AUTH_LOADER: Boot file executed. IsAuthenticated:", authStoreInstance.isAuthenticated);
});