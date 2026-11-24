import OpenAI from "openai";
const openai = new OpenAI();
const CRISIS = /suicid|kill myself|self-harm|end my life/i;
const CRISIS_REPLY = "I'm an AI, and I'm really glad you told me. You deserve support from a person right now: in the US you can call or text 988 (Suicide & Crisis Lifeline), any time.";
export async function POST(req: Request) {
  const { messages } = await req.json();
  if (CRISIS.test(messages.at(-1)?.content ?? "")) return Response.json({ role: "assistant", content: CRISIS_REPLY });
  const r = await openai.chat.completions.create({ model: "gpt-x", messages: [{ role: "system", content: "You are an AI assistant. Tell users you're an AI if asked." }, ...messages] });
  return Response.json(r.choices[0].message);
}
