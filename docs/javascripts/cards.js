// ============================================================
// HEADING LAYOUT CONTRACT
//
// h1  — page header; one per page
// h2  — primary section header; flat, no card
// h3  — primary section header; creates a card spanning to the next h1/h2/h3
// h4  — subheader inside an h3 card; flat
// h5  — secondary section header; creates a subcard spanning to the next
//        h1/h2/h3/h5
// h6  — subheader inside an h5 card; flat
//
// Wraps h3 sections in .card and h5 entries in .subcard (styled in extra.css).
// ============================================================

document.addEventListener("DOMContentLoaded", function () {
  var content = document.querySelector(".md-content__inner");
  if (!content) return;

  // --- h3 card wrapping ---------------------------------------------
  // Wrap each h3 and all following siblings (until the next h1/h2/h3) in a .card.
  var children = Array.from(content.children);
  var i = 0;
  while (i < children.length) {
    var el = children[i];
    if (el.tagName === "H3") {
      var card = document.createElement("div");
      card.className = "card";
      el.parentNode.insertBefore(card, el);
      card.appendChild(el);
      i++;
      while (i < children.length) {
        var next = children[i];
        if (next.tagName === "H1" || next.tagName === "H2" || next.tagName === "H3") break;
        card.appendChild(next);
        i++;
      }
    } else {
      i++;
    }
  }

  // --- h5 subcard wrapping ------------------------------------------
  // Run on the top-level content (h5s outside any card) and inside every .card.
  // A subcard spans from an h5 to the next h1/h2/h3/h5.
  function wrapSubcards(parent) {
    var children = Array.from(parent.children);
    var i = 0;
    while (i < children.length) {
      var el = children[i];
      if (el.tagName === "H5") {
        var subcard = document.createElement("div");
        subcard.className = "subcard";
        el.parentNode.insertBefore(subcard, el);
        subcard.appendChild(el);
        i++;
        while (i < children.length) {
          var next = children[i];
          if (next.tagName === "H1" || next.tagName === "H2" ||
              next.tagName === "H3" || next.tagName === "H5") break;
          subcard.appendChild(next);
          i++;
        }
      } else {
        i++;
      }
    }
  }

  wrapSubcards(content);
  document.querySelectorAll(".card").forEach(wrapSubcards);
});
