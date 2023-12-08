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
];

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
    id: "delete_journal",
    validationFields: [
      {
        id: "journal_id",
      },
    ],
  },
  {
    id: "sync_journal",
    validationFields: [
      {
        id: "journal_id",
      },
    ],
  },
];

formElements.forEach((formData) => {
  const form = document.getElementById(formData["id"]);

  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      clearErrorMessages();

      let isFormValid = true;

      formData["validationFields"].forEach((field) => {
        if (field.validationFn) {
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
        }
      });

      if (isFormValid) {
        form.submit();
      }
    });
  }
});

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
