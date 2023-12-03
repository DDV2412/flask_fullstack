const validationFields = [
  {
    id: "email",
    validationFn: isValidEmail,
    errorMessage: "Invalid email address",
  },
  {
    id: "password",
    validationFn: isValidPassword,
    errorMessage:
      "Password must be at least 8 characters, contain a number, symbol, and an uppercase letter",
  },
  {
    id: "name",
    validationFn: isValidName,
    errorMessage: "Name must be at least 6 characters and cannot be empty",
  },
  {
    id: "confirmPassword",
    validationFn: isValidConfirmPassword,
    errorMessage: "Passwords do not match",
  },
  // Add more fields as needed
];

const form = document.querySelector("form");

if (form) {
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    clearErrorMessages();

    let isFormValid = true;

    validationFields.forEach((field) => {
      const inputElement = document.getElementById(field.id);
      const errorMessageElement = document.getElementById(
        `${field.id}-error-message`
      );

      if (inputElement) {
        const isValid = field.validationFn(inputElement.value);
        if (!isValid) {
          errorMessageElement.textContent = field.errorMessage;
          isFormValid = false;
        }
      }
    });

    if (isFormValid) {
      console.log("Form is valid. Submitting...");
      // Uncomment the next line to submit the form
      // form.submit();
    }
  });
}

function clearErrorMessages() {
  validationFields.forEach((field) => {
    const errorMessageElement = document.getElementById(
      `${field.id}-error-message`
    );
    if (errorMessageElement) {
      errorMessageElement.textContent = "";
    }
  });
}

// Rest of your validation functions...

function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function isValidPassword(password) {
  const passwordRegex =
    /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
  return passwordRegex.test(password);
}

function isValidName(name) {
  return name.length >= 6 && name.trim() !== "";
}

function isValidConfirmPassword(confirmPassword, originalPassword) {
  return confirmPassword === originalPassword;
}

function isRequired(value) {
  return value.trim() !== "";
}
