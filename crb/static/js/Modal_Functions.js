var active = "";
var rn = ""
var btns = document.getElementsByClassName("book-btn");
for (i = 0; i < btns.length; i++){
    addHoverHandler(btns[i]);
}

function addHoverHandler(element) {
    element.addEventListener("mouseover", function () {
        let currentID = element.id;
        active = currentID.toString().replace("PSC_", "");
        let status = document.getElementById("room_status_" + active).value.toString();
        if (status == "False"){
            document.getElementsByClassName("book-confirm")[0].value = "Cancel Booking";
        }
        document.getElementsByClassName("modal-form-label")[0].innerHTML = "PSC_" + active;
        document.getElementsByClassName("modal-form-roomNumber")[0].value = active;

    });    
}