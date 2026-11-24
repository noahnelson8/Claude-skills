export default function Signup() {
  return (
    <main>
      <img src="/hero.png">
      <script dangerouslySetInnerHTML={{ __html: "!function(f,b,e,v){fbq('init','123')}" }} />
      <form>
        <input type="email" name="email" placeholder="Email">
        <input type="tel" name="phone" placeholder="Phone">
        <button>Start free trial</button>
      </form>
      <section>
        <h2>What customers say</h2>
        {[{ name: "Sarah K.", quote: "Doubled my revenue in a week!", stars: 5 }].map(t => <blockquote key={t.name}>{t.quote}</blockquote>)}
      </section>
    </main>
  );
}
