document.addEventListener("DOMContentLoaded", function () {
    const showPopupButton = document.getElementById("show-popup");
    const popupContainer = document.getElementById("popup-container");
    const closePopupButton = document.getElementById("close-popup");

    showPopupButton.addEventListener("click", function () {
        popupContainer.style.display = "block";
    });

    closePopupButton.addEventListener("click", function () {
        popupContainer.style.display = "none";
    });

    window.addEventListener("click", function (event) {
        if (event.target === popupContainer) {
            popupContainer.style.display = "none";
        }
    });

    popupContainer.addEventListener("click", function (event) {
        event.stopPropagation();
    });
});