/*
 * AgeWell Innovations site configuration.
 * ------------------------------------------------------------------
 * This is the ONLY file to edit when Brevo and the donation checkout exist.
 *
 * newsletterFormAction: paste the "action" URL from the Brevo sign-up
 *   form's embed code (Marketing > Forms > your form > Share > Embed;
 *   it looks like https://XXXXXXXX.sibforms.com/serve/LONG_TOKEN).
 *   It is a public form-post URL, not an API key. Never put a Brevo API
 *   key here or anywhere else in browser code. One-line swap to go live.
 * interestFormAction: the same, for the separate "Interest list" form.
 *   It must NOT be attached to the newsletter lists.
 *
 * While an action is empty that form stays in labeled PREVIEW mode: it
 * checks what was typed and says signup is not open. Nothing is sent,
 * and the success message can never appear.
 *
 * donateUrl: the https link to a HOSTED checkout page (Stripe Payment
 *   Link, PayPal, Zeffy or Givebutter; see site-evidence/donation-options.md).
 *   Empty = no Donate link; the section shows "Coming soon".
 *   Card details are never collected on this website.
 */
window.AGEWELL_CONFIG = {
  newsletterFormAction: "https://fe836f5c.sibforms.com/serve/MUIFAOsspgvUgEGNDbwaEI-Wi6EeEeZbZWKJU1-QqLkyNvQOx4uE_XfZS0q61ienjBP9GqSX7PzbaX-K_pKhLU5x-Zhw3b0PhZmxdaOr6xN0BZZ7Ojfv7QZ3_wQjD_cGwucNUtRD_XY8cDqflh2U55C8T2afk8BzY8N-GaV9-TushkBXWjD2jSuUEiCcKCDsWoH38Q53tfrh2fnbhQ==",
  interestFormAction: "",
  donateUrl: "",
  // REVIEW ONLY. true shows the hidden "Support AgeWell" section and nav
  // item in "Coming soon" state for a review screenshot. Must be false on
  // any published build. Ignored once donateUrl is set.
  reviewShowDonate: false,
  // INTERNAL TODO (never shown on the site): AgeWell's confirmed mailing
  // address. Do not publish a placeholder or any home address. Needed
  // before the Brevo welcome email (CAN-SPAM footer) can be finalized.
  // Brevo's embedded-form field names. Check them against the generated
  // Brevo embed code before launch and adjust here if they differ.
  fieldNames: {
    email: "EMAIL",
    firstName: "FIRSTNAME",
    optIn: "OPT_IN",
    honeypot: "email_address_check",
    // Optional "AgeWell Safety Alerts" list, via Brevo's multi-list
    // subscription block. Copy the checkbox name (e.g. "lists_12[]") and
    // value (the list id) from the embed code. Left empty, the box is sent
    // as a SAFETY_ALERTS attribute instead.
    safetyAlertsListField: "",
    safetyAlertsListValue: ""
  }
};
