function filterTable() {
    const input = document.getElementById("searchInput");
    const filter = input.value.toLowerCase();
    const rows = document.querySelectorAll("table tbody tr");

    rows.forEach(row => {
        const name = row.cells[0].textContent.toLowerCase();
        const level = row.cells[1].textContent.toLowerCase();
        if (name.includes(filter) || level.includes(filter)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
}

function clearSearch() {
    document.getElementById("searchInput").value = "";
    filterTable();
}
