// Sizes the contextual left nav (.pm-localnav__inner) to the viewport space below
// the header, so a tall nav scrolls inside its own panel instead of stretching the
// page. The frame (.pm-localnav) is height:0 in CSS, so it never inflates the row —
// this just caps the overflowing inner to what's actually visible.
(function () {
  function init() {
    var frame = document.querySelector(".pm-localnav");
    var inner = document.querySelector(".pm-localnav__inner");
    if (!frame || !inner) return;

    var ticking = false;

    function size() {
      ticking = false;
      // frame.top is the sticky offset (2.4rem once stuck under the header; larger
      // while the banner is still on screen). Cap the inner to the space from there
      // to the bottom of the viewport, leaving a little breathing room.
      var top = frame.getBoundingClientRect().top;
      var avail = window.innerHeight - Math.max(top, 0) - 8;
      inner.style.maxHeight = Math.max(avail, 120) + "px";
    }

    function schedule() {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(size);
      }
    }

    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", schedule, { passive: true });
    size();
  }

  if (document.readyState !== "loading") init();
  else document.addEventListener("DOMContentLoaded", init);
})();
