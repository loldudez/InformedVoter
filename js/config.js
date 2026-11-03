// Site settings that depend on services the owner sets up. Empty means "not set up
// yet": the features that need them say so instead of pretending to work.
//
// MAIL_SERVICE_URL  the site's mail service: the web-app address (ending in /exec) of
//                   services/mail/Code.gs, a Google Apps Script deployed by
//                   REMINDER_FROM (README, "Email reminders and help tickets"). It sends
//                   help tickets to SUPPORT_EMAIL, and email reminders to visitors who
//                   tick the consent box and confirm by email. Until it is set, tickets
//                   open the visitor's email app addressed to SUPPORT_EMAIL, reminders are
//                   calendar files (.ics) only, and no email address is collected.
// SUPPORT_EMAIL     where help tickets go.
// REMINDER_FROM     the address reminders come from, shown in the sign-up form: the
//                   Google Workspace account that deployed the mail service.
// DONATE_URL        the site's PayPal donation page, linked above Cash App on both
//                   sections' "Support the site" pages.
// SHOW_EARLY_VOTE   the race pages' "Early vote" tab. The UF Election Lab's data is
//                   licensed for non-commercial use only (CC BY-NC-ND), so it is hidden
//                   while the site carries ads; EARLY_VOTE in scripts/update_races.py
//                   stops the refresh from reading it. Turn both back on together.

export const MAIL_SERVICE_URL = '';
export const SUPPORT_EMAIL = 'theinformedvoter.help@gmail.com';
export const REMINDER_FROM = 'caissonez@informedvoter.io';
export const DONATE_URL = 'https://www.paypal.com/donate/?hosted_button_id=RG9GTZ3R3TQAW';
export const SHOW_EARLY_VOTE = false;
