// Pick a random banner image on each page load. The <img> ships with the
// fallback as its src (see main.html); this swaps in a random choice from
// data-banners, and reverts to the fallback if that choice fails to load.
(function () {
  function pickBanner() {
    var img = document.querySelector(".pm-banner-img");
    if (!img) return;

    var base = img.getAttribute("data-banner-base") || "";
    var fallback = img.getAttribute("data-banner-fallback") || "";

    var list;
    try {
      list = JSON.parse(img.getAttribute("data-banners") || "[]");
    } catch (e) {
      list = [];
    }
    if (!Array.isArray(list) || list.length === 0) return; // keep the fallback src

    var choice = list[Math.floor(Math.random() * list.length)];
    if (!choice || choice === fallback) return; // already showing it

    // If the random pick 404s or is corrupt, fall back once.
    img.addEventListener("error", function onError() {
      img.removeEventListener("error", onError);
      if (fallback) img.src = base + fallback;
    });

    img.src = base + choice;
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", pickBanner);
  } else {
    pickBanner();
  }
})();
