export default function Signup() {
  return (
    <main>
      <img src="/hero.png" alt="Dashboard preview">
      <form>
        <label htmlFor="email">Email</label><input id="email" type="email" name="email">
        <label htmlFor="phone">Mobile (optional)</label><input id="phone" type="tel" name="phone">
        <label><input id="sms" type="checkbox" name="sms_consent"> I agree to receive text messages from Acme. Message frequency varies. Msg & data rates may apply. Reply STOP to opt out, HELP for help.</label>
        <p>14-day free trial, then $20/month. Renews monthly until you cancel. Cancel anytime in Settings. We email you 3 days before your trial ends.</p>
        <button>Start free trial</button>
      </form>
      <footer><a href="/privacy">Privacy Policy</a> · <a href="/terms">Terms of Service</a></footer>
    </main>
  );
}
