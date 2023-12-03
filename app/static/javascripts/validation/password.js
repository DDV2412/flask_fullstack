// Mendapatkan semua elemen dengan class password-icon
const passwordIcons = document.querySelectorAll(".password-icon");

// Menambahkan event listener ke setiap elemen
passwordIcons.forEach(function (passwordIcon) {
  passwordIcon.addEventListener("click", function () {
    const inputField = passwordIcon
      .closest(".password-field")
      .querySelector(".input-field");

    // Toggle antara password dan text
    if (inputField.type === "password") {
      inputField.type = "text";
    } else {
      inputField.type = "password";
    }

    const inActive = passwordIcon.querySelector(".in-active");
    const active = passwordIcon.querySelector(".active");

    inActive.classList.remove("in-active");
    inActive.classList.add("active");

    active.classList.remove("active");
    active.classList.add("in-active");
  });
});
