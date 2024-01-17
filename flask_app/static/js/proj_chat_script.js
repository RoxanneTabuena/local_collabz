var shy = [
    document.getElementById("title"),
    document.getElementById("members"),
];

var hidden = [
    document.getElementById("change_title"),
    document.getElementById("invite"),
    document.getElementById("roles")
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