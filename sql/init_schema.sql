-- Drop and recreate schema
DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;

-- Create enums first
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'action_type') THEN
        CREATE TYPE action_type AS ENUM ('Reflect', 'Respond', 'Pray');
    END IF;
END$$;

-- Hymns table
CREATE TABLE IF NOT EXISTS hymns (
    id bigserial primary key,
    created_at timestamptz not null default now(),
    "hymnTitle" text null default ''::text,
    "hymnVerse" text null default ''::text,
    CONSTRAINT hymns_hymnTitle_key UNIQUE ("hymnTitle")
);

-- Open Heavens (main)
create table public.open_heavens (
  id bigserial primary key,
  created_at timestamptz not null default now(),
  topic text null,
  date date null,
  "bibleReading" text null,
  "bibleReadingText" text null,
  "memoryVerse" text null,
  message text null,
  "actionType" action_type null,
  hymn bigint not null,
  "bible1Year" text null,
  "bible1YearText" text null,
  "actionPoint" text null,
  constraint open_heavens_hymn_fkey foreign key (hymn) references hymns (id)
);

-- Open Heavens Teenagers
create table public.open_heavens_teenagers (
  id bigserial primary key,
  created_at timestamptz not null default now(),
  "Title" text null default ''::text,
  "Date" date null,
  "Memories" text null default ''::text,
  "Read" text null default ''::text,
  "BibleReading" text null default ''::text,
  "Message" text null default ''::text,
  "HymnTitle" text null default ''::text,
  "Hymn" text null default ''::text,
  "Bible_in_One_Year_Verse" text null default ''::text,
  "Bible_in_One_Year" text null default ''::text,
  "Action_Text" text null default ''::text,
  "Action_Types" text null default ''::text,
  "Hymnal" bigint null,
  constraint open_heavens_teenagers_hymnal_fkey foreign key ("Hymnal") references hymns (id)
);

-- Comments
create table public.comments (
  id bigserial primary key,
  created_at timestamptz not null default now(),
  "openHeavensId" bigint null,
  comment text null,
  name text null,
  constraint comments_openHeavensId_fkey foreign key ("openHeavensId") references open_heavens (id)
);

create view public.comments_count_by_open_heavens as
select
  c."openHeavensId",
  count(*) as comment_count
from
  comments c
group by
  c."openHeavensId";

-- Likes
create table public.likes (
  id bigserial primary key,
  created_at timestamptz not null default now(),
  "openHeavensId" bigint null,
  "like" bigint null,
  liked boolean not null,
  constraint likes_openHeavensId_fkey foreign key ("openHeavensId") references open_heavens (id)
);

create view public.likes_count_by_open_heavens as
select
  c."openHeavensId",
  count(*) as like_count
from
  likes c
group by
  c."openHeavensId";

-- Prayer requests and pray
create table public.prayer_requests (
  id bigserial primary key,
  created_at timestamptz not null default now(),
  disabled boolean null default false,
  name text null,
  "userRef" text null,
  request_content text null
);

create table public.pray (
  id bigserial primary key,
  created_at timestamptz not null default now(),
  prayer_content text null,
  prayer_request_id bigint null,
  name text null,
  constraint pray_prayer_request_id_fkey foreign key (prayer_request_id) references prayer_requests (id) on update cascade on delete cascade
);
