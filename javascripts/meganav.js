/*
  Mega-menu flyout repositioning.

  The mega-menu is a pure-CSS hover menu (see overrides/partials/megamenu.html
  and the .pm-megamenu rules in stylesheets/extra.css). By default a submenu
  opens flush with the top of its parent row (deeper levels use `top: 0;
  left: 100%`). For a parent low on the screen, that flyout runs off the bottom
  of the viewport, leaving its tail items unreachable.

  This nudges an overflowing flyout UP so it fits on screen:

    - Flyouts stay `position: absolute` (anchored to their in-flow <li>) so they
      scroll with the page rather than being pinned with `position: fixed`.

    - Alignment: rows carry dotted dividers, and separators (labeled or not)
      break row uniformity, so we never shift by `n * rowHeight`. We snap the
      shift to a real child-row boundary (a child's offsetTop). Because the
      default layout aligns a flyout's top edge with its parent row's top edge,
      shifting up by a child's offsetTop lands that child's divider line on the
      parent edge.

    - If a flyout is taller than the viewport, it can't fit no matter what, so we
      pin it to the top of the screen and let it clip off the bottom.

  The shift is applied with negative `margin-top` (the element stays absolutely
  positioned, no scrolling involved).
*/
(function () {
  "use strict";

  var MARGIN = 8; // px of breathing room from the viewport edges

  // Direct-child <li> top offsets within the flyout — the candidate snap lines.
  function childBoundaries(ul) {
    var tops = [];
    for (var i = 0; i < ul.children.length; i++) {
      tops.push(ul.children[i].offsetTop);
    }
    return tops;
  }

  // Smallest boundary >= want (so the bottom clears), else null.
  function snapAtLeast(boundaries, want) {
    var best = null;
    for (var i = 0; i < boundaries.length; i++) {
      var b = boundaries[i];
      if (b >= want && (best === null || b < best)) best = b;
    }
    return best;
  }

  // Largest boundary <= cap (the most we can shift and keep the top on screen).
  function snapAtMost(boundaries, cap) {
    var best = 0;
    for (var i = 0; i < boundaries.length; i++) {
      var b = boundaries[i];
      if (b <= cap && b > best) best = b;
    }
    return best;
  }

  function place(ul) {
    ul.style.marginTop = ""; // measure the natural, unshifted position
    var rect = ul.getBoundingClientRect();
    var overflow = rect.bottom - (window.innerHeight - MARGIN);
    if (overflow <= 0) return; // already fits

    var maxShift = rect.top - MARGIN; // lifting more would push the top off-screen
    var boundaries = childBoundaries(ul);

    // Prefer the smallest divider line that brings the bottom on screen; if none
    // fits (flyout taller than the viewport), pin to the top via the highest
    // divider line we can and let the bottom clip.
    var snapped = snapAtLeast(boundaries, overflow);
    if (snapped === null || snapped > maxShift) snapped = snapAtMost(boundaries, maxShift);

    ul.style.marginTop = "-" + snapped + "px";
  }

  function init() {
    var menu = document.querySelector(".pm-megamenu");
    if (!menu) return;
    var lists = menu.querySelectorAll(".pm-megamenu__list .pm-megamenu__list");

    var queued = false;
    function refresh() {
      if (queued) return;
      queued = true;
      requestAnimationFrame(function () {
        queued = false;
        for (var i = 0; i < lists.length; i++) {
          // getClientRects() is empty for display:none (the hidden default).
          if (lists[i].getClientRects().length) place(lists[i]);
          else lists[i].style.marginTop = "";
        }
      });
    }

    menu.addEventListener("mouseover", refresh); // a submenu may have opened
    window.addEventListener("resize", refresh);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
