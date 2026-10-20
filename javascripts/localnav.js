// Left-nav initial scroll — on load, scroll the local nav so the current page's
// entry sits about 10% down the panel (or as far as the panel will scroll while
// keeping the entry on screen, when it can't reach 10%). Runs only where the
// panel actually overflows; no-ops otherwise.
(function () {
  var TOP_FRACTION = 0.10;   // rest the active entry this far down the panel

  function run() {
    var panel = document.querySelector(".pm-localnav__panel");
    if (!panel) return;
    var active = panel.querySelector(".pm-localnav__link--active");
    if (!active) return;

    var panelRect = panel.getBoundingClientRect();
    var activeRect = active.getBoundingClientRect();
    var relTop = activeRect.top - panelRect.top;         // entry's current offset in the panel
    var target = TOP_FRACTION * panel.clientHeight;       // where we want it to rest

    // scrollTop is clamped by the browser to [0, maxScroll], so when the entry is
    // too near the bottom to reach 10% the panel simply scrolls as far as it can.
    panel.scrollTop += relTop - target;
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
