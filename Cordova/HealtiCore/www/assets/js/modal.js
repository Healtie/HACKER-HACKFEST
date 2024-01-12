/*------------------------------------- Home Screen Popup-------------------------------------*/
 let deferredPrompt;
 window.addEventListener('beforeinstallprompt', (e) => {
   deferredPrompt = e;
 });
 const installApp = document.getElementById('installApp');
 installApp.addEventListener('click', async () => {
   if (deferredPrompt !== null) {
     deferredPrompt.prompt();
     const { outcome } = await deferredPrompt.userChoice;
     if (outcome === 'accepted') {
       deferredPrompt = null;
     }
   }
 });
$(window).on('load', function () {
    setTimeout(function () {
      $('#offcanvas').offcanvas('show');
    }, 2500);
  });