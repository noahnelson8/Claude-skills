# Compliance checklist

Each section: **detect** (code / live) → **good looks like** → **fix**. Section numbers match the scanner's report.

## 1. Privacy policy exists and is reachable
- **Detect:** code: a `privacy` route or page; live: a "Privacy Policy" link in the footer of every page (funnel steps and checkout included), plus in app settings and signup.
- **Good:** linked everywhere data is collected; has a "last updated" date; names the business and a contact method.
- **Fix:** add the page and footer link. In GHL: Settings → the funnel/site footer, or add a Text element with the link on every step.

## 2. Policy matches what's actually collected
- **Detect:** compare the scanner's personal-data fields, cookies and services with the policy's list of data and purposes.
- **Good:** every category collected (contact info, payment, usage/analytics, device/IP, uploaded content, messages) is named with its purpose.
- **Fix:** add the missing categories and purposes to the policy (draft for review).

## 3. Policy discloses AI use
- **Detect:** scanner "AI providers" (OpenAI, Anthropic, Google AI, etc.) or AI features in the UI.
- **Good:** says user content may be processed by AI providers, for what, and whether it's used to train models (check each provider's API terms; most API terms say no training by default).
- **Fix:** add an "AI features" section naming the providers or the category.

## 4. Policy names third parties that receive data
- **Detect:** scanner categories: analytics, ad pixels (Meta, TikTok, Google Ads, LinkedIn), payments, email/SMS/CRM (GoHighLevel/LeadConnector, Twilio, SendGrid...), storage, error tracking, session replay.
- **Good:** lists them by name or clear category. Ad pixels and session replay are disclosed explicitly, since these are the ones that trigger "sharing" and wiretap-style claims.
- **Fix:** add them; for ad pixels on sites with California users, add a "Do Not Sell or Share" link and honour Global Privacy Control if pixels share data for advertising.

## 5. Deleted means deleted
- **Detect:** scanner "delete handlers". Open each one: when a user or record is deleted, are the stored files (S3/Supabase/Firebase/Cloudinary objects) also removed? Is there a way for users to delete their account or request deletion?
- **Good:** account deletion removes database rows **and** storage objects (or schedules it within a stated period); the policy describes it truthfully.
- **Fix:** add the storage removal call to the delete path, plus a background clean-up for orphans; make the policy match the real retention.

## 6. Storage isn't public
- **Detect:** scanner "storage public flags": Supabase `public: true` buckets, S3 `public-read` ACL or `Principal: "*"`, Firebase rules with `allow read: if true`, files served from guessable URLs.
- **Good:** user uploads private; served through signed, expiring URLs; only truly public assets (logos, marketing images) are public.
- **Fix:** make the bucket private, switch reads to signed URLs, and check whether anything was already exposed.

## 7. Testimonials and reviews are real
- **Detect:** scanner "testimonials" (hard-coded quotes, star ratings, review arrays); live: the testimonial section.
- **Good:** every testimonial is from a real customer who agreed to it, isn't AI-written or invented, discloses any payment or freebie, and atypical results say what's typical. No fake star counts.
- **Fix:** remove or replace anything that can't be traced to a real customer; add "results not typical" context where needed. Never generate testimonials.

## 8. Cancelling is as easy as signing up
- **Detect:** scanner "subscription/cancel": is there a self-serve cancel path (e.g. Stripe customer portal, a cancel button)? Count clicks for signup and for cancel. Is cancel hidden behind a call or chat?
- **Good:** cancel online in the same medium and with about the same effort as signup; any save offer can be declined in one click.
- **Fix:** add a "Cancel subscription" button in account settings or enable the Stripe customer portal.

## 9. Free trials and auto-renewal are disclosed and reminded
- **Detect:** scanner "trial" (`trial_period_days`, `trial_end`, trial copy) and renewal code; live: what's shown next to the buy button.
- **Good:** before payment, clear terms: price after the trial, when it starts charging, that it renews until cancelled, how to cancel; affirmative consent (unchecked box or explicit button text); a reminder email before a trial converts and before annual renewals; a confirmation email with cancel instructions.
- **Fix:** add the disclosure block next to the button, a reminder email (Stripe `customer.subscription.trial_will_end` webhook, or a GHL workflow), and a confirmation email.

## 10. AI chatbots handle self-harm and crisis
- **Detect:** scanner "chatbot" plus "crisis language" (988, crisis, self-harm, suicide) in prompts or handlers.
- **Good:** the bot discloses it's an AI; messages expressing suicidal thoughts or self-harm get a supportive reply with crisis resources (in the US, call or text **988**), the bot doesn't continue with harmful content, and the protocol is described on the site. Companion-style bots (ongoing relationship, emotional support) carry the strictest rules.
- **Fix pattern:** a check before the model call (keyword list plus a lightweight classifier prompt) that routes to a fixed, human-written crisis response; a system prompt rule as a second layer; logging without storing sensitive content longer than needed; a published "how our assistant handles crisis messages" note.

## 11. SMS and email marketing consent (GHL funnels especially)
- **Detect:** phone fields plus SMS providers (Twilio, GHL/LeadConnector); live: the text next to the phone field.
- **Good (SMS):** separate, unchecked consent checkbox, not required to buy; consent text names the business, says message frequency varies, "Msg & data rates may apply", "Reply STOP to opt out, HELP for help", and links to the privacy policy and terms; the policy says mobile numbers aren't shared for marketing. This is also what A2P 10DLC registration expects.
- **Good (email):** every marketing email has a working unsubscribe link and a physical mailing address; honour opt-outs promptly.
- **Fix:** in GHL: Sites → Funnels → step → Edit → the Form element → add a Checkbox field for SMS consent (not required), paste the consent text, link the policy pages.

## 12. Accessibility basics
- **Detect:** scanner counts: images without `alt`, inputs without labels, buttons without accessible names; live: keyboard tab-through, contrast.
- **Good:** alt text, labelled form fields, visible focus, 4.5:1 text contrast, captions on video with speech. Website accessibility lawsuits (ADA) are common against small businesses too.
- **Fix:** add the missing alt text and labels; fix contrast; add captions.

## 13. Cookies and tracking consent (if EU/UK users, or ad pixels)
- **Detect:** scanner "cookies" and ad pixels; live: whether trackers fire before consent.
- **Good:** for EU/UK visitors, non-essential cookies wait for consent and "Reject" is as easy as "Accept"; for US, a clear notice and opt-out for ad sharing.
- **Fix:** add a consent tool that blocks pixels until consent (where required).

## 14. Children
- **Detect:** product or copy aimed at kids; age fields; school use.
- **Good:** if under-13s could use it, stop and flag for a lawyer (COPPA). Otherwise, terms state a minimum age.
