import { createClient } from "@supabase/supabase-js";
export async function POST(req: Request) {
  const { userId } = await req.json();
  const supabase = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_KEY!);
  const { data } = await supabase.storage.from("user-uploads").list(userId);
  await supabase.storage.from("user-uploads").remove([...(data ?? []).map(f => `${userId}/${f.name}`)]);
  await supabase.auth.admin.deleteUser(userId);
  return Response.json({ ok: true });
}
