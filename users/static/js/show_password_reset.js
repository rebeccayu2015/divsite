const newPassword1 = document.querySelector("#id_new_password1");
const newPassword2 = document.querySelector("#id_new_password2");

newPassword1.insertAdjacentHTML('beforebegin', '<i class="bi bi-eye-slash" id="toggleNewPassword1"></i>');
newPassword2.insertAdjacentHTML('beforebegin', '<i class="bi bi-eye-slash" id="toggleNewPassword2"></i>');

const toggleNewPassword1 = document.querySelector("#toggleNewPassword1");
const toggleNewPassword2 = document.querySelector("#toggleNewPassword2");

toggleNewPassword1.addEventListener("click", function () {
  // toggle the type attribute
  const type = newPassword1.getAttribute("type") === "password" ? "text" : "password";
  newPassword1.setAttribute("type", type);

  // toggle the icon
  this.classList.toggle("bi-eye");
});

toggleNewPassword2.addEventListener("click", function () {
  // toggle the type attribute
  const type = newPassword2.getAttribute("type") === "password" ? "text" : "password";
  newPassword2.setAttribute("type", type);

  // toggle the icon
  this.classList.toggle("bi-eye");
});