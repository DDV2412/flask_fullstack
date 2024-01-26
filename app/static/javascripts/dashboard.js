const sidebar = document.getElementById("sidebar");
const header = document.getElementById("header");
const menuToggle = document.getElementById("menu-toggle");
const sectionDashboard = document.querySelector(".section_dashboard");

menuToggle.addEventListener("click", () => {
  sidebar.classList.toggle("less");
  header.classList.toggle("expend");
  sectionDashboard.classList.toggle("expend");
});

const dropdownToogle = document.getElementById("dropdown-toogle");
const dropdownMenu = document.getElementById("dropdown-menu");

dropdownToogle.addEventListener("click", () => {
  dropdownMenu.classList.toggle("opened");
});

const thumbnailImage = document.getElementById("thumbnail");

if (thumbnailImage) {
  thumbnailImage.addEventListener("change", function () {
    const input = this;
    const file = input.files[0];

    if (file) {
      const formData = new FormData();
      formData.append("file", file);

      fetch("/upload", {
        method: "POST",
        body: formData,
      })
        .then((response) => {
          if (!response.ok) {
            return response.json().then((error) => Promise.reject(error));
          }
          return response.json();
        })
        .then((data) => {
          const fileUrl = data.file_url;

          const thumbnailImage = document.getElementById("image-thumbnail");
          const thumbnailPrev = document.getElementById("preview-thumbnail");
          const thumbnail = document.getElementById("thumbnail_image");

          if (thumbnailImage) {
            thumbnailImage.src = fileUrl;
          }

          if (thumbnailPrev) {
            thumbnailPrev.classList.toggle("show");
          }

          if (thumbnail) {
            thumbnail.value = fileUrl;
          }
        })
        .catch((error) => {
          const errorMessage = error.error;
          document.getElementById("thumbnail-error-message").textContent =
            errorMessage;
        });
    }
  });
}

const mainImage = document.getElementById("main_file");

if (mainImage) {
  mainImage.addEventListener("change", function () {
    const input = this;
    const file = input.files[0];

    if (file) {
      const formData = new FormData();
      formData.append("file", file);

      fetch("/upload", {
        method: "POST",
        body: formData,
      })
        .then((response) => {
          if (!response.ok) {
            return response.json().then((error) => Promise.reject(error));
          }
          return response.json();
        })
        .then((data) => {
          const fileUrl = data.file_url;

          const mainImage = document.getElementById("main_image_url");
          const mainPrev = document.getElementById("preview-image");
          const image = document.getElementById("main_image");

          if (mainImage) {
            mainImage.src = fileUrl;
          }

          if (mainPrev) {
            mainPrev.classList.toggle("show");
          }

          if (image) {
            image.value = fileUrl;
          }
        })
        .catch((error) => {
          const errorMessage = error.error;
          document.getElementById("main-error-message").textContent =
            errorMessage;
        });
    }
  });
}

const fileUpload = document.getElementById("file");

if (fileUpload) {
  fileUpload.addEventListener("change", function () {
    const input = this;
    const file = input.files[0];

    if (file) {
      const formData = new FormData();
      formData.append("file", file);
      fetch("/upload", {
        method: "POST",
        body: formData,
      })
        .then((response) => {
          if (!response.ok) {
            return response.json().then((error) => Promise.reject(error));
          }
          return response.json();
        })
        .then((data) => {
          const fileUrl = data.file_url;

          const fileName = data.filename;
          const name = document.getElementById("fileName");
          const fileView = document.getElementById("file_view");

          if (name) {
            name.textContent = fileName;
          }

          if (fileView) {
            fileView.value = fileUrl;
          }
        })
        .catch((error) => {
          const errorMessage = error.error;
          document.getElementById("file-error-message").textContent =
            errorMessage;
        });
    }
  });
}

const closeImage = document.getElementById("close-image");

if (closeImage) {
  closeImage.addEventListener("click", function () {
    document.getElementById("preview-image").classList.toggle("show");
    document.getElementById("main_image_url").src = "";
  });
}

const closeThumbnail = document.getElementById("close-thumbnail");

if (closeThumbnail) {
  closeThumbnail.addEventListener("click", function () {
    document.getElementById("preview-thumbnail").classList.toggle("show");
    document.getElementById("image-thumbnail").src = "";
  });
}
