
var hidden = [
    document.getElementById('send'),
];

var shy = [
    document.getElementById('new'),
]

for(i=0; i<hidden.length; i++){
    hidden[i].style.display = "none";
}
function display(id){
    hidden[id].style.display = "inherit"
}
function nevermind(id){
    hidden[id].style.display = "none"
}
function hide(id){
    shy[id].style.display="none"
}
function show(id){
    shy[id].style.display="inherit"
}
