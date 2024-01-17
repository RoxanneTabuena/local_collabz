function hide(element){
    element.style.display="none"
}
var hidden = [
    document.getElementById("update_stat"),
    document.getElementById("update_type"),
    document.getElementById("team_modify"),
    document.getElementById("skills"),
    document.getElementById("new_skills"),
    document.getElementById("edit_about"),
];
var shy =[
    document.getElementById("about")
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
function scare(id){
    shy[id].style.display = "none"
}