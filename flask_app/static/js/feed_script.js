// open dropdown menu
const dropdown = (id) => {
    // close any open menu
    document.querySelectorAll('.dropmenu.show').forEach((dropdown) => {
        dropdown.classList.remove('show');
        });
    // open desired menu
    document.getElementById(id).classList.toggle("show");
}

// close all open menus when clicking outside nav
window.onclick = (event) => {
    if (!event.target.matches('.dropbtn')) {
        document.querySelectorAll('.dropmenu.show').forEach((dropdown) => {
            dropdown.classList.remove('show');
        });
    }
}



