const password = document.querySelector("#id_password");
password.insertAdjacentHTML('beforebegin', '<i class="bi bi-eye-slash" id="togglePassword"></i>');

const togglePassword = document.querySelector("#togglePassword");

togglePassword.addEventListener("click", function () {
  // toggle the type attribute
  const type = password.getAttribute("type") === "password" ? "text" : "password";
  password.setAttribute("type", type);

  // toggle the icon
  this.classList.toggle("bi-eye");
});
