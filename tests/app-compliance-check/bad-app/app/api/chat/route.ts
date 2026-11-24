import OpenAI from "openai";
const openai = new OpenAI();
export async function POST(req: Request) {
  const { messages } = await req.json();
  const r = await openai.chat.completions.create({ model: "gpt-x", messages: [{ role: "system", content: "You are Mia, a friendly companion." }, ...messages] });
  return Response.json(r.choices[0].message);
}
