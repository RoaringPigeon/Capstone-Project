$( document ).ready(function() {
    let btns = document.getElementsByClassName("approve-btn");
    for (i = 0; i < btns.length; i++){
    addHoverHandler(btns[i]);


    function addHoverHandler(element) {
        element.addEventListener("mouseover", function () {
            let currentID = element.id;
            active = currentID.toString().replace("PSC_", "");
            document.getElementsByClassName("modal-form-label")[0].innerHTML = currentID;
            document.getElementsByClassName("admin-room")[0].value = active;
            document.getElementsByClassName("admin-request")[0].value = document.getElementsByClassName("request-id")[0].value.toString();
            console.log(document.getElementsByClassName("admin-request")[0].value);
                
        });    
    }


}
})

