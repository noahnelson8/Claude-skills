import Stripe from "stripe";
import { createClient } from "@supabase/supabase-js";
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
const supabase = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_KEY!);
export async function setup() {
  await supabase.storage.createBucket("user-uploads", { public: false });
}
export async function startTrial(customer: string) {
  return stripe.subscriptions.create({ customer, items: [{ price: "price_123" }], trial_period_days: 14 });
}
export async function portal(customer: string) {
  return stripe.billingPortal.sessions.create({ customer, return_url: "https://example.com/settings" });
}
export async function onWebhook(event: Stripe.Event) {
  if (event.type === "customer.subscription.trial_will_end") { /* send trial reminder email */ }
}
