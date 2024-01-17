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
