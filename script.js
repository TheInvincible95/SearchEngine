// Function to start the timer
function startTimer(micImg) {
    var timer = 3; // Timer duration in seconds
    var display = document.querySelector('#timer');
    // Function to update the display with the remaining time
    function updateDisplay() {
        display.textContent = timer + "s";
        if (timer <= 0) {
            clearInterval(timerInterval);
            display.innerHTML = "";
            display.setAttribute('id', 'loader');
            micImg.remove();

        }
        timer--;
    }

    // Initial call to update display immediately
    updateDisplay();

    // Call updateDisplay function every sec
    var timerInterval = setInterval(updateDisplay, 1000);
}

//Function for audio capture
function toggleMic() {
    var micImg = document.getElementById("mic-img");
    var micButton = document.querySelector(".record-button");

    if (micImg.src.includes("microphone-black-shape.png")) {

        saveSelections();

        // Toggle mic to dot icon with red bg
        micImg.src = "img/dot.png";
        micButton.style.backgroundColor = "red";

        // Keep blinking every 500 ms
        blink = setInterval(function () {
            micImg.style.visibility = (micImg.style.visibility == 'hidden' ? '' : 'hidden');
        }, 500);

        // Notify python STT script to start
        fetch("/trigger-STT", {
            method: 'GET',
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok.');
                }
                return response.text();
            })
            .then(responseData => {
                window.location.href = "/results?data=" + responseData;
            })
            .catch(error => {
                console.error('Error occurred:', error);
            });

        startTimer(micImg);
    }
}

function saveSelections() {
    const checkboxes = document.querySelectorAll('input[name="cat"]:checked');
    const interests = Array.from(checkboxes).map(checkbox => checkbox.value);

    const interestsString = JSON.stringify(interests.join(''));

    // Store the category in a cookie
    document.cookie = `rave_cat_data=${interestsString}; path=/; SameSite=Strict`;

}