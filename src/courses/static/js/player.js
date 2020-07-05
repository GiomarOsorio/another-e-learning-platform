$(document).ready(function () {
  // Change "{}" to your options:
  // https://github.com/sampotts/plyr/#options

  const player = new Plyr('#player', {
    youtube: { noCookie: false, rel: 0, showinfo: 0, iv_load_policy: 3, modestbranding: 1 },
  });

  // Expose player so it can be used from the console
  window.player = player;

});