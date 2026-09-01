// Back-to-top button. The banner scrolls away at the top of every page while the
// header (with the mega-menu) is sticky at top:0 — so the header pins to the top
// exactly when the banner has fully scrolled past. This watches the banner and
// reveals the button at that moment; clicking it returns to the top. Enhancement
// only: if there's no banner the button never shows.
(function () {
  "use strict";

  function init() {
    var btn = document.createElement("button");
    btn.className = "pm-top";
    btn.type = "button";
    btn.setAttribute("aria-label", "Back to top");
    btn.innerHTML =
      '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">' +
      '<path fill="none" stroke="currentColor" stroke-width="3" ' +
      'stroke-linecap="round" stroke-linejoin="round" d="M6 15l6-6 6 6"/></svg>';

    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    btn.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" });
    });
    document.body.appendChild(btn);

    var banner = document.querySelector(".pm-banner-link");
    if (!banner) return;   // no banner to scroll past → leave the button hidden

    // Show the button once the banner is entirely above the viewport — the point
    // at which the sticky header reaches the top.
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        btn.classList.toggle("pm-top--show", !entries[0].isIntersecting);
      }, { threshold: 0 }).observe(banner);
    } else {
      var onScroll = function () {
        btn.classList.toggle("pm-top--show", window.scrollY > banner.offsetHeight);
      };
      window.addEventListener("scroll", onScroll, { passive: true });
      onScroll();
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
