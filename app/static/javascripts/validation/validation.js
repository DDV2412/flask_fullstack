const formElements = [
  {
    id: "journal-add",
    validationFields: [
      {
        id: "title",
        validationFn: isRequired,
        errorMessage: "This field is required.",
      },
      {
        id: "issn",
        validationFn: isRequired,
        errorMessage: "This field is required.",
      },
      {
        id: "e-issn",
        validationFn: isRequired,
        errorMessage: "This field is required.",
      },
      {
        id: "abbreviation",
        validationFn: isRequired,
        errorMessage: "This field is required.",
      },
      {
        id: "sites",
        validationFn: isRequired,
        errorMessage: "This field is required.",
      },
      {
        id: "editor",
        validationFn: isRequired,
        errorMessage: "This field is required.",
      },
      {
        id: "email",
        validationFn: isValidEmail,
        errorMessage: "Invalid email address",
      },
      {
        id: "thumbnail_image",
      },
      {
        id: "main_image",
      },
      {
        id: "short_summary",
      },
      {
        id: "description",
      },
    ],
  },
  {
    id: "journal-edit",
    validationFields: [
      {
        id: "title",
        validationFn: isRequired,
        errorMessage: "This field is required.",
      },
      {
        id: "issn",
        validationFn: isRequired,
        errorMessage: "This field is required.",
      },
      {
        id: "e-issn",
        validationFn: isRequired,
        errorMessage: "This field is required.",
      },
      {
        id: "abbreviation",
        validationFn: isRequired,
        errorMessage: "This field is required.",
      },
      {
        id: "sites",
        validationFn: isRequired,
        errorMessage: "This field is required.",
      },
      {
        id: "editor",
        validationFn: isRequired,
        errorMessage: "This field is required.",
      },
      {
        id: "email",
        validationFn: isValidEmail,
        errorMessage: "Invalid email address",
      },
      {
        id: "thumbnail_image",
      },
      {
        id: "main_image",
      },
      {
        id: "short_summary",
      },
      {
        id: "description",
      },
    ],
  },
  {
    id: "sync_journal",
    validationFields: [
      {
        id: "article",
      },
    ],
  },
  {
    id: "edit_article",
    validationFields: [
      {
        id: "title",
        validationFn: isRequired,
        errorMessage: "This field is required.",
      },
    ],
  },
  {
    id: "register",
    validationFields: [
      {
        id: "name",
        validationFn: isValidName,
        errorMessage: "Name must be at least 6 characters and cannot be empty",
      },
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
        id: "confirmPassword",
        validationFn: isValidConfirmPassword,
        errorMessage: "Passwords do not match.",
      },
    ],
  },
  {
    id: "create-user",
    validationFields: [
      {
        id: "name",
        validationFn: isValidName,
        errorMessage: "Name must be at least 6 characters and cannot be empty",
      },
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
        id: "role",
        validationFn: isRequired,
        errorMessage: "This field is required",
      },
    ],
  },
];

formElements.forEach((formData) => {
  const form = document.getElementById(formData["id"]);

  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();

      clearErrorMessages(formData.validationFields);

      let isFormValid = true;

      formData.validationFields.forEach((field) => {
        if (field.validationFn) {
          const inputElement = document.getElementById(field.id);
          const errorMessageElement = document.getElementById(
            `${field.id}-error-message`,
          );

          if (field.id === "confirmPassword") {
            const originalPassword = document.getElementById("password").value;
            const confirmPassword = inputElement.value;

            const isValidPass = field.validationFn(
              confirmPassword,
              originalPassword,
            );

            if (!isValidPass) {
              errorMessageElement.textContent = field.errorMessage;
              isFormValid = false;
            }
          } else {
            if (inputElement) {
              const isValid = field.validationFn(inputElement.value);

              if (!isValid) {
                errorMessageElement.textContent = field.errorMessage;
                isFormValid = false;
              }
            }
          }
        }
      });

      if (isFormValid) {
        form.submit();
      }
    });
  }
});

function clearErrorMessages(validationFields) {
  if (validationFields) {
    validationFields.forEach((field) => {
      const errorMessageElement = document.getElementById(
        `${field.id}-error-message`,
      );
      if (errorMessageElement) {
        errorMessageElement.textContent = "";
      }
    });
  }
}

function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function isValidPassword(password) {
  const passwordRegex =
    /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$/;
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
