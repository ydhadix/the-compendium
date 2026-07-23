// Keyword-jump landing offset — on pages with a sticky A-Z jump bar, an anchor
// jump would drop the target under the bar (Material's default :target margin
// only clears the header). Measure header + bar height and publish it as
// --pm-jump-offset on the content container; extra.css feeds that into the
// target's scroll-margin-top so the target rests just beneath the bar. Native
// fragment scrolling (clicks, back/forward, initial hash) honours scroll-margin,
// so no click interception is needed. No-ops on pages without a jump bar.
(function () {
  var GAP = 8;   // px of breathing room between the bar's bottom edge and the target

  function run() {
    var container = document.querySelector(".md-content__inner");
    if (!container) return;
    var bar = container.querySelector(".keyword-jump");
    if (!bar) return;

    var header = document.querySelector(".md-header");
    var headerH = header ? header.offsetHeight : 0;   // sticky header the bar rests under
    var offset = headerH + bar.offsetHeight + GAP;
    container.style.setProperty("--pm-jump-offset", offset + "px");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
  window.addEventListener("resize", run);   // bar height changes when the letters rewrap
})();
