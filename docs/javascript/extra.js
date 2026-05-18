// ============================================================
// HEADING LAYOUT CONTRACT
//
// h1  — page title; one per page
// h2  — section titles; creates a card spanning to the next h1/h2
// h3  — subsection titles (ToC-visible); flat, no card
// h4  — anchor-only (ToC-visible, invisible on page)
// h5  — entry titles (ToC-visible); always creates a subcard
//        A subcard spans from an h5 to the next h2, h3, or h5.
// h6  — sub-entry titles; bold, body-colored, no card
// ============================================================

document.addEventListener("DOMContentLoaded", function () {

    // --- Site name home link -------------------------------------------
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
    document.querySelectorAll(".md-content__inner table").forEach(function (table) {
        var allEmpty = Array.from(table.querySelectorAll("tr")).every(function (row) {
            return row.cells.length === 0 || row.cells[0].textContent.trim() === "";
        });
        if (allEmpty) table.setAttribute("data-no-row-labels", "");
    });

    var content = document.querySelector(".md-content__inner");
    if (!content) return;

    // --- h2 card wrapping ---------------------------------------------
    // Wrap each h2 and all following siblings (until the next h1/h2)
    // in a <div class="card">.
    var children = Array.from(content.children);
    var i = 0;

    while (i < children.length) {
        var el = children[i];
        if (el.tagName === "H2") {
            var card = document.createElement("div");
            card.className = "card";
            el.parentNode.insertBefore(card, el);
            card.appendChild(el);
            i++;
            while (i < children.length) {
                var next = children[i];
                if (next.tagName === "H1" || next.tagName === "H2") break;
                card.appendChild(next);
                i++;
            }
        } else {
            i++;
        }
    }

    // --- h5 subcard wrapping ------------------------------------------
    // Run on the top-level content (h5s before any h2) and inside every
    // .card (h5s within h2 sections). h4 does not break subcard boundaries.
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

// --- Anchor navigation for admonitions ------------------------------------
// h4 anchors are invisible (height: 0) and sit inside <details> elements.
// scroll-margin-top is unreliable on zero-height elements, and the browser
// fires the scroll before <details> has reflowed when it was closed.
// Instead: intercept hash navigation, open the parent <details> explicitly,
// wait one frame for layout, then scroll to the <details> box itself.
(function () {
    function scrollToAnchor() {
        var hash = window.location.hash;
        if (!hash) return;
        var target;
        try { target = document.querySelector(hash); } catch (e) { return; }
        if (!target) return;

        var details = target.closest("details");
        if (!details) return;

        details.open = true;

        requestAnimationFrame(function () {
            var headerEl = document.querySelector(".md-header");
            var tabsEl   = document.querySelector(".md-tabs");
            var offset   = (headerEl ? headerEl.offsetHeight : 0)
                         + (tabsEl   ? tabsEl.offsetHeight   : 0)
                         + 8;
            var top = details.getBoundingClientRect().top + window.scrollY - offset;
            window.scrollTo({ top: top, behavior: "instant" });
        });
    }

    window.addEventListener("hashchange", scrollToAnchor);
    window.addEventListener("load", scrollToAnchor);
}());
