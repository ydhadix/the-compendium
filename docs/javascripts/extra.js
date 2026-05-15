// ============================================================
// HEADING LAYOUT CONTRACT
//
// h1  — page title; one per page; excluded from ToC
// h2  — main section titles; no cards
// h3  — card titles (ToC-visible): features, spells, conditions, etc.
//        A card spans from an h3 to the next h3 or higher heading.
// h4  — table titles (ToC-visible): stat blocks, ship stats, major tables
// h5  — subsection titles (hidden from ToC)
// h6  — minor table titles (hidden from ToC)
// ============================================================

document.addEventListener("DOMContentLoaded", function () {

    // --- Site name home link -------------------------------------------
    // Material renders the logo anchor with the correct base URL already;
    // reuse that href so we don't hardcode the GitHub Pages path.
    var logoAnchor = document.querySelector("a.md-header__button.md-logo");
    var titleEl    = document.querySelector(".md-header__title");
    if (titleEl && logoAnchor) {
        var a = document.createElement("a");
        a.href = logoAnchor.href;
        a.style.color = "inherit";
        a.style.textDecoration = "none";
        while (titleEl.firstChild) {
            a.appendChild(titleEl.firstChild);
        }
        titleEl.appendChild(a);
    }

    // --- h3 card wrapping ---------------------------------------------
    // Wrap each h3 and all following siblings (until the next h1/h2/h3)
    // in a <div class="card"> so they can be styled as a unit without
    // any markup in the markdown source files.
    var content = document.querySelector(".md-content__inner");
    if (!content) return;

    // Snapshot children before mutating the DOM.
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

});
