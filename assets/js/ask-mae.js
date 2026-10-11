/* Ask Mae: DEMONSTRATION ONLY.
 * Answers come from two local, reviewed files on this website:
 *   assets/data/mae-knowledge.json  (scripted topics)
 *   assets/data/notes.json          (AI & Safety Notes)
 * No AI service, no API key, no third-party requests. Nothing typed here is
 * stored (no cookies, no localStorage) or sent anywhere. It disappears on reload.
 */
(function () {
  "use strict";
  var dialog = document.getElementById("ask-mae");
  var triggers = document.querySelectorAll("[data-ask-mae]");
  if (!dialog || !triggers.length) return;

  var log = dialog.querySelector("[data-mae-log]");
  var form = dialog.querySelector("[data-mae-form]");
  var input = dialog.querySelector("[data-mae-input]");
  var startersBox = dialog.querySelector("[data-mae-starters]");
  var closeBtn = dialog.querySelector("[data-mae-close]");
  var resetBtn = dialog.querySelector("[data-mae-reset]");
  var title = dialog.querySelector("#ask-mae-title");
  var KB = null, NOTES = [], lastTrigger = null, loading = null;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  triggers.forEach(function (t) { t.hidden = false; t.addEventListener("click", function (e) { e.preventDefault(); open(t); }); });
  document.querySelectorAll(".mae-nojs").forEach(function (n) { n.hidden = true; });

  function load() {
    if (loading) return loading;
    function get(u) { return fetch(u, { credentials: "same-origin" }).then(function (r) { if (!r.ok) throw new Error(u); return r.json(); }); }
    loading = Promise.all([get("assets/data/mae-knowledge.json"), get("assets/data/notes.json")]).then(function (res) {
      KB = res[0]; NOTES = (res[1] && res[1].notes) || [];
    });
    return loading;
  }

  /* ---------- open / close, focus trap ---------- */
  function open(trigger) {
    lastTrigger = trigger || document.activeElement;
    if (typeof dialog.showModal === "function") dialog.showModal(); else dialog.setAttribute("open", "");
    document.documentElement.classList.add("mae-open");
    title.focus();
    load().then(function () { if (!log.children.length) start(); }).catch(function () {
      log.textContent = "";
      addMae([{ p: "Sorry, Mae’s demo answers didn’t load. Please reload the page, or ask a person at hello@awinnovations.org. Email is not emergency support." }]);
    });
  }
  function close() {
    if (typeof dialog.close === "function" && dialog.open) dialog.close(); else { dialog.removeAttribute("open"); afterClose(); }
  }
  function afterClose() {
    document.documentElement.classList.remove("mae-open");
    if (lastTrigger && document.contains(lastTrigger)) lastTrigger.focus();
  }
  dialog.addEventListener("close", afterClose);
  dialog.addEventListener("cancel", function (e) { e.preventDefault(); close(); }); // Esc
  closeBtn.addEventListener("click", close);
  dialog.addEventListener("click", function (e) { if (e.target === dialog) close(); }); // backdrop
  dialog.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { e.preventDefault(); close(); return; }
    if (e.key !== "Tab") return;
    var f = Array.prototype.filter.call(dialog.querySelectorAll('a[href],button:not([disabled]),textarea,input,[tabindex="-1"]#ask-mae-title'), function (el) {
      return el.offsetParent !== null || el === title;
    });
    f = f.filter(function (el) { return el !== title; });
    if (!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if (e.shiftKey && (document.activeElement === first || document.activeElement === title)) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });

  /* ---------- rendering (DOM only; never innerHTML with visitor text) ---------- */
  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; }
  function scrollTo(node) { node.scrollIntoView({ block: "nearest", behavior: reduce ? "auto" : "smooth" }); }

  function personBox() {
    var a = KB.askAPerson, box = el("div", "mae-person");
    box.appendChild(el("p", "mae-person-title", a.title));
    box.appendChild(el("p", null, a.text));
    var link = el("a", "btn btn-secondary mae-person-link", "Email " + a.email);
    link.href = "mailto:" + a.email + "?subject=" + encodeURIComponent("Question for AgeWell");
    box.appendChild(link);
    box.appendChild(el("p", "mae-small", a.emergency));
    box.appendChild(el("p", "mae-small", a.noTranscript));
    return box;
  }

  function noteBox(n) {
    var box = el("div", "mae-note-card");
    box.appendChild(el("p", "mae-note-title", n.title + " (" + n.dateLabel + ")"));
    var c = el("div", "mae-src-block mae-company");
    c.appendChild(el("p", "mae-src-label", "Company announcement (" + n.source.publisher + ", " + n.source.dateLabel + ")"));
    c.appendChild(el("p", null, n.company.summary));
    box.appendChild(c);
    var g = el("div", "mae-src-block mae-guidance");
    g.appendChild(el("p", "mae-src-label", "AgeWell guidance"));
    g.appendChild(el("p", null, "Who it affects: " + n.affects));
    g.appendChild(el("p", null, "Practical step: " + n.step));
    if (n.guidance) g.appendChild(el("p", null, n.guidance));
    g.appendChild(el("p", null, "Status and limits: " + n.status));
    g.appendChild(el("p", null, n.teachingLabel + ": “" + n.teaching + "”"));
    box.appendChild(g);
    var s = el("p", "mae-small");
    s.appendChild(document.createTextNode("Official source: "));
    var a = el("a", null, n.source.title); a.href = n.source.url; a.rel = "noopener";
    s.appendChild(a);
    s.appendChild(document.createTextNode(". Reviewed by AgeWell: " + n.reviewedLabel + "."));
    box.appendChild(s);
    return box;
  }

  function renderBlocks(blocks, ctx) {
    var frag = document.createDocumentFragment();
    blocks.forEach(function (b) {
      if (b.p) frag.appendChild(el("p", null, b.p));
      else if (b.steps) { var ol = el("ol", "mae-steps"); b.steps.forEach(function (s) { ol.appendChild(el("li", null, s)); }); frag.appendChild(ol); }
      else if (b.list) { var ul = el("ul", "mae-list"); b.list.forEach(function (s) { ul.appendChild(el("li", null, s)); }); frag.appendChild(ul); }
      else if (b.note) { var n = el("p", "mae-remember"); n.appendChild(el("strong", null, (b.label || "Note") + ": ")); n.appendChild(document.createTextNode(b.note)); frag.appendChild(n); }
      else if (b.links) { var p = el("p", "mae-links"); b.links.forEach(function (l, i) { var a = el("a", null, l.text); a.href = l.href; a.addEventListener("click", function () { close(); }); if (i) p.appendChild(document.createTextNode(" · ")); p.appendChild(a); }); frag.appendChild(p); }
      else if (b.person) frag.appendChild(personBox());
      else if (b.notes) {
        var list = NOTES;
        if (ctx && ctx.text) {
          var hit = NOTES.filter(function (n) { return n.keywords.some(function (k) { return has(ctx.text, k); }); });
          if (hit.length && hit.length < NOTES.length) list = hit;
        }
        list.forEach(function (n) { frag.appendChild(noteBox(n)); });
        var more = el("p", "mae-links"); var a2 = el("a", null, "See all notes"); a2.href = "notes.html"; more.appendChild(a2); frag.appendChild(more);
      }
    });
    return frag;
  }

  function addMae(blocks, followups, ctx) {
    var msg = el("div", "mae-msg mae-from-mae");
    msg.appendChild(el("p", "mae-who", "Mae (demo)"));
    var body = el("div", "mae-body"); body.appendChild(renderBlocks(blocks, ctx)); msg.appendChild(body);
    if (followups && followups.length) {
      var row = el("div", "mae-chips");
      row.setAttribute("role", "group"); row.setAttribute("aria-label", "Suggested next questions");
      followups.forEach(function (id) {
        var b = el("button", "mae-chip", KB.followupLabels[id] || id); b.type = "button";
        b.addEventListener("click", function () { ask(b.textContent, id); });
        row.appendChild(b);
      });
      msg.appendChild(row);
    }
    log.appendChild(msg); scrollTo(msg);
    return msg;
  }
  function addUser(text, hidden) {
    var msg = el("div", "mae-msg mae-from-you");
    msg.appendChild(el("p", "mae-who", "You"));
    msg.appendChild(el("p", hidden ? "mae-hidden" : null, hidden ? "(Hidden: this looked like private information)" : text));
    log.appendChild(msg);
  }

  function start() {
    log.textContent = "";
    addMae([{ p: KB.opening }]);
  }

  /* ---------- simple keyword matching ---------- */
  function norm(s) { return (" " + s.toLowerCase().replace(/[’']/g, "'").replace(/[^a-z0-9'@.+\- ]+/g, " ").replace(/\s+/g, " ") + " "); }
  function esc(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }
  function has(text, k) { return new RegExp("(^|[^a-z0-9])" + esc(k.toLowerCase()) + "($|[^a-z0-9])").test(text); }

  function looksSensitive(raw) {
    var t = raw.toLowerCase();
    if (/\b\d{3}-\d{2}-\d{4}\b/.test(t)) return true;                                // SSN pattern
    if (/(?:\d[ -]?){12,19}/.test(t.replace(/[^\d -]/g, " "))) return true;         // card / long account number
    if (/\b(password|passcode|pass code|pin|otp|verification code|security code|one-time code|code)\b\s*(is|was|=|:)?\s*[^\s]{3,}/.test(t) &&
        /\b(password|passcode|pin)\b\s*(is|was|=|:)\s*\S+|\b(code|pin|otp)\b\D{0,12}\d{4,8}\b/.test(t)) return true;
    if (/(^|[^$\d,.])\d{5,8}(?![\d,.])/.test(t.replace(/\b(19|20)\d{2}\b/g, ""))) {
      if (!looksPhone(raw)) return true;                                               // bare 5–8 digit code
    }
    if (/(acct|account|routing|member)\s*(number|no\.?|#)?\s*(is|:)?\s*\d{4,}/.test(t)) return true;
    var tokens = raw.split(/\s+/);
    for (var i = 0; i < tokens.length; i++) {                                           // password-like token
      var w = tokens[i];
      if (w.length >= 8 && !/[@\/]/.test(w) && /[a-z]/i.test(w) && /\d/.test(w) && /[^a-z0-9]/i.test(w.replace(/[.,!?]$/, ""))) return true;
    }
    return false;
  }
  function looksPhone(raw) {
    return /(?:\+?1[ .-]?)?\(?\d{3}\)?[ .-]?\d{3}[ .-]?\d{4}\b/.test(raw) || /1-8\d\d-[a-z0-9-]{7,}/i.test(raw);
  }

  function findTopic(id) {
    var list = KB.topics;
    for (var i = 0; i < list.length; i++) if (list[i].id === id || list[i].alias === id) return list[i];
    return null;
  }
  function match(raw) {
    var text = norm(raw), best = null, bestScore = 0;
    KB.topics.forEach(function (t) {
      var s = 0; (t.keywords || []).forEach(function (k) { if (has(text, k)) s++; });
      if (s > bestScore) { best = t; bestScore = s; }
    });
    if (!best && looksPhone(raw)) best = findTopic("phone");
    return best;
  }

  function respond(topic, ctx) {
    if (!topic) { addMae(KB.fallback.blocks, KB.fallback.followups, ctx); return; }
    addMae(topic.blocks, topic.followups, ctx);
  }

  function ask(label, topicId) {
    if (!KB) return;
    addUser(label, false);
    respond(findTopic(topicId), { text: "" });
  }

  KBready();
  function KBready() {
    startersBox.querySelectorAll("[data-topic]").forEach(function (b) {
      b.addEventListener("click", function () { load().then(function () { ask(b.textContent.trim(), b.getAttribute("data-topic")); }); });
    });
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var raw = input.value.trim();
    if (!raw || !KB) { input.focus(); return; }
    input.value = "";
    if (looksSensitive(raw)) {
      addUser(raw, true);
      addMae([{ note: KB.sensitive.label, label: "Mae" }].concat(KB.sensitive.blocks), KB.sensitive.followups);
      input.focus();
      return;
    }
    addUser(raw, false);
    var t = norm(raw);
    respond(match(raw), { text: t });
    input.focus();
  });

  resetBtn.addEventListener("click", function () { if (KB) { start(); title.focus(); } });
})();
