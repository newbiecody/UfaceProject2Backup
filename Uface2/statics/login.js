"use strict";

var uname1 = window.document.querySelector('#uname1');
var pdw1 = window.document.querySelector('#pwd1');


function login() {
    if (uname1 == "admin" && pwd1 == "password") {
        window.location.replace("SelectModule.html");
    }
}