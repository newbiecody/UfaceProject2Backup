var list = document.getElementById('namelist');
var valueToAdd = 
function changeText2() {
    var firstname = toAdd[0];
    document.getElementById('boldStuff2').innerHTML = firstname;
    var entry = document.createElement('li');
    entry.appendChild(document.createTextNode(firstname));
    list.appendChild(entry);
}