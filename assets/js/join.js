/* /join newsletter form. Posts to the AgeWell Brevo form (same call Brevo's embed makes:
   POST action?isAjax=1, JSON {success}). Without JavaScript the form posts natively. */
(function () {
  var form = document.querySelector("form[data-join]");
  if (!form) return;
  var action = form.getAttribute("action");
  if (!/^https:\/\/[a-z0-9-]+\.sibforms\.com\/serve\/[A-Za-z0-9_=-]+$/.test(action)) return;
  var email = document.getElementById("join-email"), err = document.getElementById("join-email-error");
  var status = form.querySelector("[data-status]"), btn = form.querySelector('button[type="submit"]');
  var RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  function say(cls, text) { status.className = "form-status " + cls; status.innerHTML = "<p></p>"; status.firstChild.textContent = text; }
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    err.hidden = true; email.removeAttribute("aria-invalid");
    var v = email.value.trim();
    if (!v || !RE.test(v)) {
      err.textContent = v ? "Please check your email address. It should look like name@example.com." : "Please enter your email address.";
      err.hidden = false; email.setAttribute("aria-invalid", "true"); email.focus(); return;
    }
    if (form.querySelector('input[name="email_address_check"]').value) return;
    var label = btn.textContent; btn.disabled = true; btn.classList.add("is-sending"); btn.textContent = "Sending…"; say("is-wait", "Sending…");
    fetch(action + "?isAjax=1", { method: "POST", body: new FormData(form), credentials: "omit" })
      .then(function (r) { return r.json().catch(function () { return { success: r.ok }; }); })
      .then(function (j) {
        if (j && j.success === true) { say("is-ok", "Thanks! Check your email to confirm."); form.reset(); btn.classList.add("is-sent"); btn.textContent = "✓ Sent"; window.setTimeout(function () { btn.classList.remove("is-sent"); btn.textContent = label; }, 4000); }
        else say("is-err", "Sorry, that didn't go through. Please try again, or email hello@awinnovations.org.");
      })
      .catch(function () { say("is-err", "Sorry, that didn't go through. Please try again, or email hello@awinnovations.org."); })
      .then(function () { btn.disabled = false; btn.classList.remove("is-sending"); if (!btn.classList.contains("is-sent")) btn.textContent = label; });
  });
})();
