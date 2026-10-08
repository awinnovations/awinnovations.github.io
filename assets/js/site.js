/* AgeWell Innovations site behavior. No trackers, no cookies, no storage. */
(function () {
  "use strict";
  var root = document.documentElement;
  root.classList.add("js");
  var reduceQuery = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : null;
  function motionOK() { return !(reduceQuery && reduceQuery.matches); }
  if (motionOK()) root.classList.add("motion-ok");
  if (reduceQuery && reduceQuery.addEventListener) {
    reduceQuery.addEventListener("change", function () {
      root.classList.toggle("motion-ok", motionOK());
      if (!motionOK()) stopGreeting(true);
    });
  }

  /* ---------- Mobile menu ---------- */
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("site-nav");
  function setMenu(open) {
    if (!toggle || !nav) return;
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    nav.classList.toggle("is-open", open);
  }
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      setMenu(toggle.getAttribute("aria-expanded") !== "true");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) setMenu(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        setMenu(false);
        toggle.focus();
      }
    });
  }

  /* ---------- Gentle section entrances (content stays visible without JS) ---------- */
  var reveals = document.querySelectorAll(".reveal");
  if (motionOK() && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });
    reveals.forEach(function (el) { io.observe(el); });
    // Safety net: never leave content hidden.
    window.setTimeout(function () { reveals.forEach(function (el) { el.classList.add("is-in"); }); }, 6000);
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ---------- Mae's greeting: short, stops on its own, with a pause control ---------- */
  var greet = document.getElementById("mae-greeting");
  var greetBtn = greet ? greet.querySelector(".motion-toggle") : null;
  var greetTimer = null;
  function stopGreeting(hideBtn) {
    if (!greet) return;
    greet.classList.remove("is-playing");
    window.clearTimeout(greetTimer);
    if (greetBtn) {
      greetBtn.textContent = "Replay Mae’s greeting";
      greetBtn.hidden = !!hideBtn || !motionOK();
    }
  }
  function playGreeting() {
    if (!greet || !motionOK()) return;
    greet.classList.remove("is-playing");
    void greet.offsetWidth; // restart CSS animation
    greet.classList.add("is-playing");
    if (greetBtn) { greetBtn.hidden = false; greetBtn.textContent = "Pause animation"; }
    window.clearTimeout(greetTimer);
    greetTimer = window.setTimeout(function () { stopGreeting(false); }, 5000);
  }
  if (greet && greetBtn) {
    greetBtn.addEventListener("click", function () {
      if (greet.classList.contains("is-playing")) stopGreeting(false); else playGreeting();
    });
    if (motionOK()) window.setTimeout(playGreeting, 500);
  }

  /* ---------- Practice the callback ---------- */
  var practice = document.querySelector("[data-practice]");
  if (practice) {
    var FEEDBACK = {
      a: { cls: "fb-not", label: "Not the best choice.",
           text: "It’s kind to want to help right away. But gift cards are a common scam payment, and the money is hard to get back. A real emergency can wait for a quick callback. Try again, or see the best choice." },
      b: { cls: "fb-good", label: "A good start, but not enough.",
           text: "A family phrase is a helpful extra check. But phrases can leak, and a real loved one might forget hers under stress. Even with the right phrase, call back on a number you know before you send money. Try again, or see the best choice." },
      c: { cls: "fb-best", label: "Best choice. Well done.",
           text: "Yes. Hanging up and calling back on a number you already know is the strongest step. If you can’t reach Keisha, call someone else you trust, like her dad, even though the caller asked you not to.",
           after: "In this practice, the real Keisha answers. She’s at work, and she’s fine. That’s the callback at work." },
      d: { cls: "fb-not", label: "Not the best choice.",
           text: "The number that called you may belong to the scammer, even if it looks familiar. Caller ID can be faked. Use a number you already had saved. Try again, or see the best choice." }
    };
    var buttons = practice.querySelectorAll(".choice");
    var fbBox = practice.querySelector("[data-feedback]");
    buttons.forEach(function (b) { b.setAttribute("aria-pressed", "false"); });
    function choose(key) {
      var f = FEEDBACK[key];
      buttons.forEach(function (b) {
        var on = b.getAttribute("data-choice") === key;
        b.setAttribute("aria-pressed", on ? "true" : "false");
        b.classList.toggle("is-best", key === "c" && b.getAttribute("data-choice") === "c");
      });
      var html = '<div class="fb ' + f.cls + '"><p class="fb-label">Choice ' + key.toUpperCase() + ": " + f.label + "</p><p>" + f.text + "</p>" +
        (f.after ? "<p><strong>" + f.after + "</strong></p>" : "") + "</div>";
      fbBox.innerHTML = html;
    }
    buttons.forEach(function (b) {
      b.addEventListener("click", function () { choose(b.getAttribute("data-choice")); });
    });
    practice.querySelector("[data-show-best]").addEventListener("click", function () { choose("c"); });
    practice.querySelector("[data-reset]").addEventListener("click", function () {
      buttons.forEach(function (b) { b.setAttribute("aria-pressed", "false"); b.classList.remove("is-best"); });
      fbBox.innerHTML = '<p class="sr-only">Practice reset. Choose a response.</p>';
      buttons[0].focus();
    });
  }

  /* ---------- Interest-list shortcuts from cards ---------- */
  document.querySelectorAll("[data-interest]").forEach(function (link) {
    link.addEventListener("click", function () {
      var val = link.getAttribute("data-interest");
      var box = document.querySelector('.interest-form input[name="INTEREST"][value="' + val + '"]');
      if (box) box.checked = true;
    });
  });

  /* ---------- Forms (Brevo-ready; preview mode until configured) ---------- */
  var CFG = window.AGEWELL_CONFIG || {};
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  var MSG = {
    emptyEmail: "Please enter your email address.",
    badEmail: "That email address doesn’t look complete. Please check it and try again. Example: name@example.com",
    consent: "Please check the box to say you’d like the Update.",
    interest: "Please choose at least one thing you’re interested in.",
    okNewsletter: "Almost done! Check your email and click the link to confirm. If you don’t see it in a few minutes, check your spam or junk folder.",
    okInterest: "Thank you! You’re on the interest list. We’ll be in touch about what you checked.",
    already: "You’re already on the list. Thank you! Look for the next issue in your inbox.",
    server: "Something went wrong on our end. Please try again in a few minutes.",
    preview: "Signup isn’t open yet. This is a preview of the website, so nothing was sent or saved. The form will connect to our email service before launch."
  };
  function showError(input, errEl, text) {
    if (input) input.setAttribute("aria-invalid", "true");
    if (errEl) { errEl.textContent = text; errEl.hidden = false; }
  }
  function clearError(input, errEl) {
    if (input) input.removeAttribute("aria-invalid");
    if (errEl) { errEl.textContent = ""; errEl.hidden = true; }
  }
  function setStatus(form, cls, text) {
    var s = form.querySelector("[data-status]");
    s.className = "form-status " + cls;
    s.innerHTML = "<p>" + text + "</p>";
  }
  function wireForm(form) {
    var kind = form.getAttribute("data-form");
    var action = kind === "newsletter" ? CFG.newsletterFormAction : CFG.interestFormAction;
    var email = form.querySelector('input[type="email"]');
    var emailErr = document.getElementById(email.getAttribute("aria-describedby"));
    var consent = form.querySelector('input[name="OPT_IN"]');
    var consentErr = consent ? document.getElementById(consent.getAttribute("aria-describedby")) : null;
    var group = form.querySelector(".check-group");
    var groupErr = group ? document.getElementById(group.getAttribute("aria-describedby")) : null;

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var firstBad = null;
      clearError(email, emailErr);
      var v = email.value.trim();
      if (!v) { showError(email, emailErr, MSG.emptyEmail); firstBad = firstBad || email; }
      else if (!EMAIL_RE.test(v)) { showError(email, emailErr, MSG.badEmail); firstBad = firstBad || email; }
      if (consent) {
        clearError(consent, consentErr);
        if (!consent.checked) { showError(consent, consentErr, MSG.consent); firstBad = firstBad || consent; }
      }
      if (group) {
        clearError(null, groupErr);
        if (!group.querySelector("input:checked")) { showError(null, groupErr, MSG.interest); firstBad = firstBad || group.querySelector("input"); }
      }
      if (firstBad) { firstBad.focus(); return; }
      var hp = form.querySelector('input[name="email_address_check"]');
      if (hp && hp.value) return; // bot

      if (!action) { setStatus(form, "is-preview", MSG.preview); return; }

      var btn = form.querySelector('button[type="submit"]');
      btn.disabled = true;
      var data = new FormData(form);
      data.set("locale", "en");
      fetch(action, { method: "POST", body: data, credentials: "omit" })
        .then(function (r) { return r.json().catch(function () { return { success: r.ok }; }); })
        .then(function (j) {
          if (j && j.success) {
            setStatus(form, "is-ok", kind === "newsletter" ? MSG.okNewsletter : MSG.okInterest);
            form.reset();
          } else if (j && /already|exist/i.test(JSON.stringify(j))) {
            setStatus(form, "is-ok", MSG.already);
          } else {
            setStatus(form, "is-err", MSG.server);
          }
        })
        .catch(function () { setStatus(form, "is-err", MSG.server); })
        .then(function () { btn.disabled = false; });
    });
  }
  document.querySelectorAll("form[data-form]").forEach(wireForm);
})();
