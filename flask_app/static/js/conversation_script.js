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

var shy = [document.getElementById("title")]

var hidden = [
    document.getElementById("change_title"),
    document.getElementById("invite")
];

for(i=0; i<hidden.length; i++){
    hidden[i].style.display = "none";
    console.log(hidden[i], 'ishiding')
}
function display(id){
    hidden[id].style.display = "inherit"
}
function nevermind(id){
    hidden[id].style.display = "none"
}
function reveal(id){
    shy[id].style.display = "inherit"
}
function hide(id){
    shy[id].style.display = "none"
}