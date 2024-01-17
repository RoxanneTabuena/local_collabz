function hide(element){
    element.style.display="none"
}

var hidden = [
    document.getElementById("skills"),
    document.getElementById("interests"),
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

