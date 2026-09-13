-- ============================================================================
-- CV Builder Pro — Supabase schema
-- Run this once in Supabase Dashboard -> SQL Editor -> New query
-- ============================================================================

-- One row per saved CV profile per user. The "data" column holds the exact
-- same JSON shape the app already builds locally (cv_data fields +
-- collect_full_config() styling/layout fields) — no format change needed,
-- just a different place to put it.
create table if not exists cv_profiles (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade not null,
  profile_name text not null,
  data jsonb not null,
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  unique (user_id, profile_name)
);

-- Row Level Security: without this, ANY authenticated user could read/edit
-- every row in the table. This makes it so a user can only ever see or
-- change rows where user_id matches their own auth.uid() — enforced by
-- Postgres itself, not by app code (so even a bug in the Streamlit app
-- can't leak one user's CVs to another).
alter table cv_profiles enable row level security;

create policy "Users can view their own profiles"
  on cv_profiles for select
  using (auth.uid() = user_id);

create policy "Users can insert their own profiles"
  on cv_profiles for insert
  with check (auth.uid() = user_id);

create policy "Users can update their own profiles"
  on cv_profiles for update
  using (auth.uid() = user_id);

create policy "Users can delete their own profiles"
  on cv_profiles for delete
  using (auth.uid() = user_id);

-- Keep updated_at current automatically on every edit (used for the
-- Gallery View's "sort newest first" / "last saved" display).
create or replace function update_cv_profiles_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create trigger set_cv_profiles_updated_at
before update on cv_profiles
for each row execute function update_cv_profiles_updated_at();