// Flag tables whose first column is entirely empty with data-no-row-labels, so
// extra.css can hide that column (convention: leave the whole first column blank
// for tables that have column labels but no row labels).
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".md-content__inner table").forEach(function (table) {
    var allEmpty = Array.from(table.querySelectorAll("tr")).every(function (row) {
      return row.cells.length === 0 || row.cells[0].textContent.trim() === "";
    });
    if (allEmpty) table.setAttribute("data-no-row-labels", "");
  });
});

// Scroll shadows for wide tables. Material wraps every table in a horizontally
// scrolling .md-typeset__scrollwrap; because the cells are opaque, we can't paint
// the shadow on the scroller itself. Instead wrap the scroller in a non-scrolling
// .pm-tablewrap and let its ::before / ::after (a bordered gradient, see extra.css)
// float above the table at whichever edge still has hidden content. Classes are
// toggled from the live scroll position so the shadow only shows when it can scroll.
function pmInitTableScrollShadows() {
  document.querySelectorAll(".md-content__inner .md-typeset__scrollwrap").forEach(function (scroller) {
    var wrap = scroller.parentElement;
    if (!wrap.classList.contains("pm-tablewrap")) {
      wrap = document.createElement("div");
      wrap.className = "pm-tablewrap";
      scroller.parentNode.insertBefore(wrap, scroller);
      wrap.appendChild(scroller);
    }

    function update() {
      var max = scroller.scrollWidth - scroller.clientWidth;
      var x = scroller.scrollLeft;
      wrap.classList.toggle("pm-tablewrap--left", x > 1);
      wrap.classList.toggle("pm-tablewrap--right", x < max - 1);
    }

    if (!scroller.dataset.pmShadowBound) {
      scroller.addEventListener("scroll", update, { passive: true });
      window.addEventListener("resize", update);
      scroller.dataset.pmShadowBound = "1";
    }
    update();
  });
}

// Run on load so Material has already wrapped the tables in .md-typeset__scrollwrap.
window.addEventListener("load", pmInitTableScrollShadows);
