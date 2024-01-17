console.log('here I am...')

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
