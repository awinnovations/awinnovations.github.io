/* AgeWell Innovations site behavior. This file itself sets no cookies and uses no storage.
   Note: every page also loads Google Analytics 4 (G-ME7ZJEWXJD) in <head>, which sets
   first-party analytics cookies (Google signals and ad personalization are off).
   Never send names, emails or form contents to Analytics. */
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

  /* ---------- Active page indicator ---------- */
  if (nav) {
    var here = location.pathname.replace(/index\.html$/, "");
    nav.querySelectorAll("a").forEach(function (a) {
      var p = a.getAttribute("href").replace(/index\.html$/, "");
      if (p === here && !a.classList.contains("btn")) a.setAttribute("aria-current", "page");
    });
  }

  /* ---------- Auto-tag sections and cards for gentle entrances (JS-only, so no-JS stays visible) ---------- */
  if (motionOK()) {
    document.querySelectorAll("main > section:not(:first-child) > .wrap > :not(.hub-grid):not(.card-grid):not(.carousel), .hub-grid > li, .card").forEach(function (el, i) {
      if (el.closest(".reveal") && !el.classList.contains("reveal")) return;
      el.classList.add("reveal");
      var sib = el.parentNode ? Array.prototype.indexOf.call(el.parentNode.children, el) : 0;
      if (sib > 0) { el.setAttribute("data-stagger", ""); el.style.setProperty("--i", Math.min(sib, 6)); }
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

  /* ---------- Hero parallax (desktop, motion OK) / reading progress / cursor glow ---------- */
  var desktop = window.matchMedia && window.matchMedia("(min-width: 900px) and (pointer: fine)");
  var para = document.querySelector("[data-parallax]");
  var longPage = document.body.scrollHeight > window.innerHeight * 2.5 && /guide|notes|learn|privacy|faq|about|accessibility/.test(location.pathname);
  var bar = null;
  if (longPage && motionOK()) {
    bar = document.createElement("div"); bar.className = "read-progress"; bar.setAttribute("aria-hidden", "true");
    document.body.appendChild(bar);
  }
  var ticking = false;
  function onScroll() {
    if (ticking) return; ticking = true;
    window.requestAnimationFrame(function () {
      ticking = false;
      var y = window.scrollY || 0;
      if (para && motionOK() && desktop && desktop.matches) para.style.setProperty("--py", Math.min(y * 0.12, 60).toFixed(1) + "px");
      if (bar) { var max = document.documentElement.scrollHeight - window.innerHeight; bar.style.setProperty("--p", max > 0 ? Math.min(y / max, 1).toFixed(3) : 0); }
    });
  }
  if ((para || bar) && motionOK()) window.addEventListener("scroll", onScroll, { passive: true });
  if (motionOK() && desktop && desktop.matches) {
    var glow = document.createElement("div"); glow.className = "cursor-glow"; glow.setAttribute("aria-hidden", "true");
    document.body.appendChild(glow);
    window.addEventListener("pointermove", function (e) {
      if (e.pointerType !== "mouse") return;
      glow.style.setProperty("--cx", e.clientX + "px"); glow.style.setProperty("--cy", e.clientY + "px");
    }, { passive: true });
    document.addEventListener("mouseleave", function () { glow.style.setProperty("--cx", "-999px"); });
  }

  /* ---------- Manual carousels: arrows, dots, swipe (native scroll-snap). Never autoplays. ---------- */
  document.querySelectorAll("[data-carousel]").forEach(function (car) {
    var track = car.querySelector(".carousel-track");
    var slides = Array.prototype.slice.call(track.children);
    var controls = car.querySelector(".carousel-controls");
    var dotsBox = car.querySelector(".carousel-dots");
    var prev = car.querySelector("[data-prev]"), next = car.querySelector("[data-next]");
    var status = car.querySelector("[data-carousel-status]");
    controls.hidden = false;
    var dots = slides.map(function (s, i) {
      var d = document.createElement("button");
      d.type = "button"; d.className = "carousel-dot"; d.setAttribute("aria-label", "Step " + (i + 1) + " of " + slides.length);
      d.addEventListener("click", function () { go(i); });
      dotsBox.appendChild(d); return d;
    });
    var cur = 0;
    function go(i) {
      i = Math.max(0, Math.min(slides.length - 1, i));
      track.scrollTo({ left: slides[i].offsetLeft - track.offsetLeft, behavior: motionOK() ? "smooth" : "auto" });
      mark(i, true);
    }
    function mark(i, announce) {
      cur = i;
      dots.forEach(function (d, k) { d.setAttribute("aria-current", k === i ? "true" : "false"); });
      prev.disabled = i === 0;
      next.disabled = i >= slides.length - 1 || track.scrollLeft + track.clientWidth >= track.scrollWidth - 4;
      fit();
      if (announce && status) status.textContent = "Step " + (i + 1) + " of " + slides.length + ": " + (slides[i].querySelector("h3") || {}).textContent;
    }
    function fit() {
      // Only on phones, where one card is in view; wider screens show several cards at full height.
      var one = !window.matchMedia || window.matchMedia("(max-width: 759px)").matches;
      car.classList.toggle("is-fit", one);
      var a = slides[cur]; if (!a || !one) return;
      var last = a.lastElementChild, cs = getComputedStyle(a);
      var h = last ? last.getBoundingClientRect().bottom - a.getBoundingClientRect().top + parseFloat(getComputedStyle(last).marginBottom) + parseFloat(cs.paddingBottom) + parseFloat(cs.borderBottomWidth) : a.scrollHeight;
      h = Math.ceil(h);
      car.style.setProperty("--h", h + "px");
    }
    window.addEventListener("resize", fit);
    window.addEventListener("load", fit);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
    prev.addEventListener("click", function () { go(cur - 1); });
    next.addEventListener("click", function () { go(cur + 1); });
    track.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); go(cur + 1); }
      if (e.key === "ArrowLeft") { e.preventDefault(); go(cur - 1); }
    });
    var st = null;
    track.addEventListener("scroll", function () {
      window.clearTimeout(st);
      st = window.setTimeout(function () {
        var best = 0, bd = Infinity;
        slides.forEach(function (s, k) { var d = Math.abs(s.offsetLeft - track.offsetLeft - track.scrollLeft); if (d < bd) { bd = d; best = k; } });
        mark(best, false);
      }, 120);
    }, { passive: true });
    mark(0, false);
  });

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
    okNewsletter: "Check your inbox to confirm your subscription.",
    okInterest: "Thank you! You’re on the interest list. We’ll be in touch about what you checked.",
    server: "Sorry, we couldn’t sign you up just now, and nothing was saved. Please check your internet connection and try again in a few minutes. If it keeps happening, email hello@awinnovations.org.",
    preview: "Preview only: signup isn’t open yet. Nothing was sent or saved, and you are not subscribed. The form will connect to our email service before launch."
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
    // Only a Brevo-hosted form endpoint is accepted (also enforced by the CSP form-action/connect-src).
    if (action && !/^https:\/\/[a-z0-9-]+\.sibforms\.com\/serve\/[A-Za-z0-9_=-]+$/.test(action)) action = "";
    var note = document.querySelector('[data-preview-note="' + kind + '"]');
    if (note) note.hidden = !!action;
    // Optional Safety Alerts list: Brevo's multi-list block names the checkbox after the
    // form (e.g. lists_12[]) and uses the list id as its value. Copy both from the embed code.
    var alerts = form.querySelector("[data-alerts]"), F = CFG.fieldNames || {};
    if (alerts && F.safetyAlertsListField) { alerts.name = F.safetyAlertsListField; alerts.value = F.safetyAlertsListValue || "1"; }
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
      // Send only the fields the Brevo form has (same as /join): EMAIL, FIRSTNAME, email_address_check, locale.
      if (kind === "newsletter") { data.delete("OPT_IN"); data.delete("SAFETY_ALERTS"); }
      // Same call Brevo's own embed script makes: POST to the form action with ?isAjax=1, JSON reply {success}.
      fetch(action + "?isAjax=1", { method: "POST", body: data, credentials: "omit" })
        .then(function (r) { return r.json().catch(function () { return { success: r.ok }; }); })
        .then(function (j) {
          // Success copy appears ONLY when Brevo itself reports success.
          if (j && j.success === true) {
            setStatus(form, "is-ok", kind === "newsletter" ? MSG.okNewsletter : MSG.okInterest);
            form.reset();
          } else {
            setStatus(form, "is-err", MSG.server);
          }
        })
        .catch(function () { setStatus(form, "is-err", MSG.server); })
        .then(function () { btn.disabled = false; });
    });
  }
  document.querySelectorAll("form[data-form]").forEach(wireForm);

  /* Donate button: driven by donateUrl in config.js. Empty = no link, "coming soon" shown. */
  var donateUrl = (CFG.donateUrl || "").trim();
  var donateOK = /^https:\/\/[^\s"'<>]+$/.test(donateUrl);
  document.querySelectorAll("[data-donate]").forEach(function (a) {
    if (donateOK) { a.href = donateUrl; a.hidden = false; } else { a.removeAttribute("href"); a.hidden = true; }
  });
  document.querySelectorAll("[data-donate-soon]").forEach(function (n) { n.hidden = donateOK; });
  // While donateUrl is empty, Donate is hidden everywhere (nav, footer, section),
  // unless the review-only flag is on.
  var showDonate = donateOK || CFG.reviewShowDonate === true;
  document.querySelectorAll("[data-donate-show]").forEach(function (n) { n.hidden = !showDonate; });
})();
