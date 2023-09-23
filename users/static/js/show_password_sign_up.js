const password1 = document.querySelector("#id_password1");
const password2 = document.querySelector("#id_password2");

password1.insertAdjacentHTML('beforebegin', '<i class="bi bi-eye-slash" id="togglePassword1"></i>');
password2.insertAdjacentHTML('beforebegin', '<i class="bi bi-eye-slash" id="togglePassword2"></i>');

const togglePassword1 = document.querySelector("#togglePassword1");
const togglePassword2 = document.querySelector("#togglePassword2");

togglePassword1.addEventListener("click", function () {
  // toggle the type attribute
  const type = password1.getAttribute("type") === "password" ? "text" : "password";
  password1.setAttribute("type", type);

  // toggle the icon
  this.classList.toggle("bi-eye");
});


togglePassword2.addEventListener("click", function () {
  // toggle the type attribute
  const type = password2.getAttribute("type") === "password" ? "text" : "password";
  password2.setAttribute("type", type);

  // toggle the icon
  this.classList.toggle("bi-eye");
});