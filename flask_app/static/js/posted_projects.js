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

function hide(element){
    element.style.display="none"
}

var hidden = [
    document.getElementById("status"),
    document.getElementById("people")
];

for(i=0; i<hidden.length; i++){
    hidden[i].style.display = "none";
}
function display(id){
    hidden[id].style.display = "inherit"
}
function nevermind(id){
    hidden[id].style.display = "none"
}
