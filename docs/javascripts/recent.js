// Recently visited pages — a collapsible list at the top of the left nav.
// Records each page (except the home page) in localStorage on load, newest
// first, and renders the list (minus the current page) wherever the left-nav
// container exists. No-ops gracefully if storage is unavailable.
(function () {
  var KEY = "pm-recent";
  var OPEN_KEY = "pm-recent-open";
  var MAX = 5;

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || []; }
    catch (e) { return []; }
  }
  function save(list) {
    try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) {}
  }
  function meta(name) {
    var el = document.querySelector('meta[name="' + name + '"]');
    return el ? el.getAttribute("content") : null;
  }

  // Record the current page (unless it's the home page); return the updated list.
  function record() {
    if (meta("pm-page-home") !== null) return load();
    var title = meta("pm-page-title");
    if (!title) return load();
    var url = location.pathname;
    var list = load().filter(function (e) { return e.url !== url; });
    list.unshift({ title: title, url: url });
    list = list.slice(0, MAX);
    save(list);
    return list;
  }

  function render(list) {
    var box = document.querySelector(".pm-recent");
    if (!box) return;

    // Remember the open/closed state across page loads (default open).
    try { if (localStorage.getItem(OPEN_KEY) === "0") box.open = false; } catch (e) {}
    box.addEventListener("toggle", function () {
      try { localStorage.setItem(OPEN_KEY, box.open ? "1" : "0"); } catch (e) {}
    });

    var here = location.pathname;
    var items = list.filter(function (e) { return e.url !== here; });
    if (!items.length) return;   // nothing to show — leave it hidden

    var ul = box.querySelector(".pm-recent__list");
    ul.innerHTML = "";
    items.forEach(function (e) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.className = "pm-localnav__link pm-recent__link";
      a.href = e.url;
      a.textContent = e.title;
      li.appendChild(a);
      ul.appendChild(li);
    });
    box.hidden = false;
  }

  function run() { render(record()); }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
