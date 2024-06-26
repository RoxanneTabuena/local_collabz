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

document.getElementById("login").style.display = "none";
document.getElementById("register").style.display = "none";

function login(){
    document.getElementById("login").style.display = "inherit";
    document.getElementById("l_or_r").style.display = "none";
}

function register(){
    document.getElementById("register").style.display = "inherit";
    document.getElementById("l_or_r").style.display = "none";
}
