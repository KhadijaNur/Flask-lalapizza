function changeImage() {
    document.getElementById("pizzaimage").src = "static/images/pizza2.png";
}

function restoreImage() {
    document.getElementById("pizzaimage").src = "static/images/pizza.png";
}
function openTab(tabId) {
    var tabContents = document.getElementsByClassName('tab-content');
    for (var i = 0; i < tabContents.length; i++) {
        tabContents[i].classList.remove('active');
    }

    var tabs = document.getElementsByClassName('tab');
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].classList.remove('active');
    }

    document.getElementById(tabId).classList.add('active');

    var selectedTab = document.querySelector('.tab[onclick="openTab(\'' + tabId + '\')"]');
    selectedTab.classList.add('active');
}




$(document).ready(function() {
    $(".booking-form").submit(function() {
        var name = $(this).find("input[name='name']").val();  
        var time = $(this).find("input[name='time']").val();  
        var date = $(this).find("input[name='date']").val();  
        var num_people = $(this).find("input[name='num_people']").val();  

        Swal.fire({
            title: 'Confirm Reservation',
            html: `Name: ${name}<br>Booking details: A table for ${num_people} people booked<br>Your date is ${date}<br>Time: ${time}<br>We look forward to welcoming you, ${name}!`,
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: 'Confirm',
            cancelButtonText: 'Cancel'
        }).then((result) => {
            if (result.isConfirmed) {
                $(this).off("submit").submit();
            }
        });

        return false;
    });
});


