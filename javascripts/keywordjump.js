// Keyword-jump behaviours for the single sticky A-Z / level rail on a page.
//
// 1. One-line scroll + shadows — the rail always stays one line tall. Its links
//    are wrapped in a hidden-scrollbar scroller; when they overflow, edge shadows
//    (reusing the table scroll-shadow look, see extra.css) mark the side(s) with
//    more content. --left / --right are toggled from the live scroll position,
//    mirroring tables.js.
//
// 2. Landing offset — an anchor jump would drop the target under the sticky bar
//    (Material's default :target margin only clears the header). Measure header +
//    bar height and publish it as --pm-jump-offset on the content container;
//    extra.css feeds that into the target's scroll-margin-top.
//
// 3. Stuck state — the bar has no way in CSS to know when it pins to the top, so
//    an IntersectionObserver toggles .keyword-jump--stuck while it's pinned; on
//    mobile extra.css uses that to widen the card into a full-width bar.
//
// All no-op on pages without a jump bar.
(function () {
  "use strict";

  var GAP = 8;   // px of breathing room between the bar's bottom edge and the target
  var container, bar, scroll;

  // Move the rail's links into a scroller + centring strip so they can scroll
  // horizontally under the fixed frame. Returns the scroller.
  function wrap() {
    var existing = bar.querySelector(".keyword-jump__scroll");
    if (existing) return existing;
    var scroller = document.createElement("span");
    scroller.className = "keyword-jump__scroll";
    var inner = document.createElement("span");
    inner.className = "keyword-jump__inner";
    while (bar.firstChild) inner.appendChild(bar.firstChild);
    scroller.appendChild(inner);
    bar.appendChild(scroller);
    return scroller;
  }

  function updateShadows() {
    if (!scroll) return;
    var max = scroll.scrollWidth - scroll.clientWidth;
    var x = scroll.scrollLeft;
    bar.classList.toggle("keyword-jump--left", x > 1);          // hidden content to the left
    bar.classList.toggle("keyword-jump--right", x < max - 1);   // hidden content to the right
  }

  function measure() {
    if (!container || !bar) return;
    var header = document.querySelector(".md-header");
    var headerH = header ? header.offsetHeight : 0;   // sticky header the bar rests under
    container.style.setProperty("--pm-jump-offset", (headerH + bar.offsetHeight + GAP) + "px");
  }

  function watchStuck() {
    if (!("IntersectionObserver" in window)) return;
    // The bar pins at its CSS `top` (the header height). Shrink the observer root
    // by that line + 1px: while pinned its top edge sits above the line, clipping
    // it so intersectionRatio drops below 1 — our "stuck" signal.
    var top = parseFloat(getComputedStyle(bar).top) || 0;
    new IntersectionObserver(function (entries) {
      bar.classList.toggle("keyword-jump--stuck", entries[0].intersectionRatio < 1);
    }, { threshold: [1], rootMargin: "-" + (top + 1) + "px 0px 0px 0px" }).observe(bar);
  }

  function init() {
    container = document.querySelector(".md-content__inner");
    if (!container) return;
    bar = container.querySelector(".keyword-jump");
    if (!bar) return;

    scroll = wrap();
    measure();
    watchStuck();
    updateShadows();

    scroll.addEventListener("scroll", updateShadows, { passive: true });
    // The scrollbar is hidden and there's no drag target, so a plain vertical
    // wheel can't scroll the rail in Firefox/Safari (Blink redirects it for us).
    // Translate a vertical wheel into horizontal scroll here, releasing to the
    // page at either end so we never trap the page's own scroll.
    scroll.addEventListener("wheel", function (e) {
      var max = scroll.scrollWidth - scroll.clientWidth;
      if (max <= 0 || e.deltaX !== 0) return;   // nothing to scroll, or horizontal intent handled natively
      var delta = e.deltaY * (e.deltaMode === 1 ? 16 : 1);   // lines → ~px
      if (!delta) return;
      var atStart = scroll.scrollLeft <= 0;
      var atEnd = scroll.scrollLeft >= max - 1;
      if ((delta < 0 && atStart) || (delta > 0 && atEnd)) return;   // boundary → let the page scroll
      scroll.scrollLeft += delta;                                    // browser clamps at the ends
      e.preventDefault();
    }, { passive: false });
    window.addEventListener("resize", function () { measure(); updateShadows(); });
    window.addEventListener("load", updateShadows);
    // Web-font swaps change link widths, which can flip the overflow state.
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(updateShadows);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
