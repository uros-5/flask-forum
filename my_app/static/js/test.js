/**
 * Created by Uros on 1.10.2020.
 */
$(document).ready(function() {

    $(".dugme").on('click',function() {
       var ukucano = $(".test-text").val();
              console.log(ukucano);
        $("<p>nesto</p>".replace("nesto",ukucano)).appendTo(".komentari");
       // ajaxPost('/testing',ukucano);
    });


});

function ajaxPost(url,podaci) {
    $.getJSON("/testing",{"poruka":podaci},function (data) {
        console.log(data);
    });
    return false;
    //  $.ajax({
    //     type: 'POST',
    //     url: '',
    //     data: podaci,
    //     dataType: 'json',
    //     success: checkResponse,
    //     error:console.log("greska")
    // });
}

function checkResponse(response) {
    console.log(response);
}