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
        let pending = document.getElementById("room_pending_" + active).value.toString();
        if (status == "False"){
            document.getElementsByClassName("book-confirm")[0].value = "Not Available";
            document.getElementsByClassName("current-booking-status")[0].innerHTML = "This room is already booked and is not currently available";
        }
        else if(pending == "True"){
            document.getElementsByClassName("book-confirm")[0].value = "Confirm";
            document.getElementsByClassName("current-booking-status")[0].innerHTML = "A request is pending for this room. \n You may still request to book this room.";
        }
        else{
            document.getElementsByClassName("current-booking-status")[0].innerHTML = "This room is not being used and is available to be booked.";
        }
        document.getElementsByClassName("modal-form-label")[0].innerHTML = "PSC_" + active;
        document.getElementsByClassName("modal-form-roomNumber")[0].value = active;

    });    
}