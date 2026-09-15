// ============================================================
// HEADING LAYOUT CONTRACT
//
// h1  — page header; one per page
// h2  — primary section header; flat, no card
// h3  — primary section header; creates a card spanning to the next h1/h2/h3
// h4  — subheader inside an h3 card; flat
// h5  — secondary section header; creates a subcard spanning to the next
//        h1/h2/h3/h4/h5
// h6  — subheader inside an h5 card; flat
//
// Wraps h3 sections in .card and h5 entries in .subcard (styled in extra.css).
//
// DIVIDERS
// A card absorbs every sibling up to its boundary heading, which would also
// swallow a trailing `---`. Such a rule separates the card from what follows,
// so it is hoisted back out; rules *inside* a card (a spell's metadata /
// effect / upcast breaks) have content on both sides and are left alone.
// ============================================================

document.addEventListener("DOMContentLoaded", function () {
  var content = document.querySelector(".md-content__inner");
  if (!content) return;

  // Move any trailing <hr>s out of a freshly closed card, preserving order.
  function hoistTrailingRules(box) {
    var last = box.lastElementChild;
    while (last && last.tagName === "HR") {
      box.parentNode.insertBefore(last, box.nextSibling);
      last = box.lastElementChild;
    }
  }

  // --- h5 subcard wrapping ------------------------------------------
  // Run first, while h3/h4 headers are still bare siblings the break can see.
  // A subcard spans from an h5 to the next h1/h2/h3/h4/h5 (only h6s stay in).
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
              next.tagName === "H3" || next.tagName === "H4" ||
              next.tagName === "H5") break;
          subcard.appendChild(next);
          i++;
        }
        hoistTrailingRules(subcard);
      } else {
        i++;
      }
    }
  }

  wrapSubcards(content);

  // --- h3 card wrapping ---------------------------------------------
  // Wrap each h3 and all following siblings (until the next h1/h2/h3) in a
  // .card. Any .subcard DIVs built above are absorbed here as ordinary
  // siblings, giving the correct subcard-inside-card nesting.
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
      hoistTrailingRules(card);
    } else {
      i++;
    }
  }
});
