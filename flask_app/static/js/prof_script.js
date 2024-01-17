
var hidden = [
    document.getElementById('new_message'),
    document.getElementById('messaged'),
];

var shy = [
    document.getElementById('about'),
    document.getElementById('message'),
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
