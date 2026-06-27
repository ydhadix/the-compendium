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
