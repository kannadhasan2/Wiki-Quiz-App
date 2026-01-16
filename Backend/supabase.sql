create table if not exists wiki_quizzes (
  id bigserial primary key,
  url text not null unique,
  title text not null,
  summary text,
  sections jsonb not null default '[]'::jsonb,
  key_entities jsonb not null default '{}'::jsonb,
  quiz jsonb not null default '[]'::jsonb,
  related_topics jsonb not null default '[]'::jsonb,
  raw_html text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_wiki_quizzes_created_at on wiki_quizzes (created_at desc);

create or replace function set_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

drop trigger if exists trg_set_updated_at on wiki_quizzes;

create trigger trg_set_updated_at
before update on wiki_quizzes
for each row execute function set_updated_at();
