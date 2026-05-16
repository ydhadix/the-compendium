// ============================================================
// HEADING LAYOUT CONTRACT
//
// h1  — page title; one per page; excluded from ToC
// h2  — main section titles; no cards
// h3  — card titles (ToC-visible): features, spells, conditions, etc.
//        A card spans from an h3 to the next h3 or higher heading.
// h4  — table titles (ToC-visible): stat blocks, ship stats, major tables
// h5  — subsection titles (hidden from ToC); flat, no card
// h6  — sub-card titles (hidden from ToC): ancestry options, sub-entries, etc.
//        A subcard spans from an h6 to the next h5, h6, or higher heading.
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

    // --- Empty first-column detection ---------------------------------
    // Tables where every cell in the first column is empty receive the
    // .no-row-labels class, suppressing the column and any row-label
    // styling. Combined with the CSS empty-thead rule this covers all
    // four label combinations:
    //
    //   thead empty + first col empty  →  no labels at all
    //   thead empty + first col filled →  row labels only
    //   thead filled + first col empty →  column labels only  (.no-row-labels)
    //   thead filled + first col filled → full matrix table
    //
    // Matrix tables with an empty A1 corner cell: put &nbsp; there.
    // trim() does not strip non-breaking spaces ( ), so &nbsp;
    // is treated as non-empty and the column is preserved.
    document.querySelectorAll(".md-content__inner table").forEach(function (table) {
        var allEmpty = Array.from(table.querySelectorAll("tr")).every(function (row) {
            return row.cells.length === 0 || row.cells[0].textContent.trim() === "";
        });
        if (allEmpty) table.setAttribute("data-no-row-labels", "");
    });

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

    // --- h6 sub-card wrapping -----------------------------------------
    // Inside each .card, wrap each h6 and its following siblings (until
    // the next h5, h6, or higher heading) in a <div class="subcard">.
    document.querySelectorAll(".card").forEach(function (card) {
        var children = Array.from(card.children);
        var i = 0;
        while (i < children.length) {
            var el = children[i];
            if (el.tagName === "H6") {
                var subcard = document.createElement("div");
                subcard.className = "subcard";
                el.parentNode.insertBefore(subcard, el);
                subcard.appendChild(el);
                i++;
                while (i < children.length) {
                    var next = children[i];
                    if (next.tagName === "H1" || next.tagName === "H2" ||
                        next.tagName === "H3" || next.tagName === "H4" ||
                        next.tagName === "H5" || next.tagName === "H6") break;
                    subcard.appendChild(next);
                    i++;
                }
            } else {
                i++;
            }
        }
    });

});
