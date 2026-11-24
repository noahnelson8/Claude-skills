import Stripe from "stripe";
import { createClient } from "@supabase/supabase-js";
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
const supabase = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_KEY!);
export async function setup() {
  await supabase.storage.createBucket("user-uploads", { public: true });
}
export async function startTrial(customer: string) {
  return stripe.subscriptions.create({ customer, items: [{ price: "price_123" }], trial_period_days: 14 });
}
