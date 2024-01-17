function hide(element){
    element.style.display="none"
}
var hidden = [
    document.getElementById("alias_info"),
    document.getElementById("cities"),
    document.getElementById("add_city"),
    document.getElementById("skillADD"),
    document.getElementById("sthkill"),
    document.getElementById("interADD"),
    document.getElementById("int"),
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