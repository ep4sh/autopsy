function setAva(name) {
    const avatar_name = name + '.png';
    document.getElementById('avatar').value = avatar_name;
    highlight_avatar(name);
    return true;
}

function highlight_avatar(name) {
    let x = document.getElementsByClassName("ava")
    for (var i = 0; i < x.length; i++) {
       x[i].style.border = "0rem solid white";
    }
    document.getElementById(name).style.border = "0.2rem solid black" ;
}

function timeStamp() {
    let current = new Date();
    let cDate = current.getFullYear() + '-' + (current.getMonth() + 1) + '-' + current.getDate();
    let cTime = current.getHours() + ":" + current.getMinutes() + ":" + current.getSeconds();
    let dateTime = '\n'+cDate + 'T' + cTime+'\n';
    document.getElementById('mortem').value += dateTime;
    console.log(dateTime);
}
