$( document ).ready(function() {
    let btns = document.getElementsByClassName("approve-btn");
    for (i = 0; i < btns.length; i++){
    addHoverHandler(btns[i]);


    function addHoverHandler(element) {
        element.addEventListener("mouseover", function () {
            let currentID = element.id.toString().split("-");
            active = currentID[0].toString().replace("PSC_", "");
            let currentRequest = currentID[1].toString();
            document.getElementsByClassName("modal-form-label")[0].innerHTML = currentID[0].toString();
            document.getElementsByClassName("admin-room")[0].value = active;
            document.getElementsByClassName("admin-request")[0].value = document.getElementsByClassName("request-id")[0].value.toString();
            let date = document.getElementById("date-desired-" + currentRequest).value.toString().split("-");
            document.getElementById("date-format").innerHTML = date[1].toString() + "/" + date[2].toString() + "/" + date[0];
            let time = document.getElementById("time-desired-" + currentRequest).value.toString().split(":");
            document.getElementById("time-format").innerHTML = time[0].toString() + ":" + time[1].toString();
        });    
    }


}
})
