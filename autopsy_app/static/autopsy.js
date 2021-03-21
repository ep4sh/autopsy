function setAva(name) {
    const avatar_name = name + '.png';
    console.log(avatar_name);
    document.getElementById('avatar').value = avatar_name;

    highlight_avatar(name);
    return true;
}

function highlight_avatar(name) {
    var x = document.getElementsByClassName("ava")
    for (var i = 0; i < x.length; i++) {
       x[i].style.border = "0rem solid white";
    }
    document.getElementById(name).style.border = "0.2rem solid black" ;
}
