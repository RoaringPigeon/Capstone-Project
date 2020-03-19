var active = "";
var rn = ""
var btns = document.getElementsByClassName("book-btn");
for (i = 0; i < btns.length; i++){
    addHoverHandler(btns[i]);
}

function addHoverHandler(element) {
    element.addEventListener("mouseover", function () {
        let currentID = element.id;
        active = currentID;
        document.getElementsByClassName("modal-form-label")[0].innerHTML = active.toString();
        document.getElementsByClassName("modal-form-roomNumber")[0].value = active.toString().replace("PSC_", "");
        let test = document.getElementsByClassName("modal-form-roomNumber")[0];
        console.log(test);

    });    
}