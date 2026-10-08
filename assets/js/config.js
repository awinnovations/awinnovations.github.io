/*
 * AgeWell Innovations site configuration.
 * ------------------------------------------------------------------
 * This is the ONLY file to edit when the Brevo forms exist.
 *
 * newsletterFormAction: paste the "action" URL from the Brevo
 *   subscription form's embed code (it looks like
 *   https://XXXXXXXX.sibforms.com/serve/LONG_TOKEN). It is a public
 *   form-post URL, not an API key. Never put a Brevo API key here or
 *   anywhere else in browser code.
 * interestFormAction: the same, for a second Brevo form that feeds the
 *   "Interest list" (programs, volunteering, hosting, sponsorship).
 *
 * While a value is empty the form stays in PREVIEW mode: it validates
 * input and explains that signup is not open yet. Nothing is sent.
 */
window.AGEWELL_CONFIG = {
  newsletterFormAction: "",
  interestFormAction: "",
  // Brevo's embed uses these field names. Check them against the
  // generated Brevo form before launch and adjust here if they differ.
  fieldNames: {
    email: "EMAIL",
    firstName: "FIRSTNAME",
    optIn: "OPT_IN",
    safetyAlerts: "SAFETY_ALERTS",
    honeypot: "email_address_check"
  }
};
