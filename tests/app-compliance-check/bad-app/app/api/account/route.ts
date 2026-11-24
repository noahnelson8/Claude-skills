import { createClient } from "@supabase/supabase-js";
export async function POST(req: Request) {
  const { userId } = await req.json();
  const supabase = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_KEY!);
  await supabase.auth.admin.deleteUser(userId);
  return Response.json({ ok: true });
}
