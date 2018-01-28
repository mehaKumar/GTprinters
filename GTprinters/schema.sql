drop table if exists tickets;
create table tickets (
  timestamp integer primary key,
  printer text not null,
  issue text not null,
  date text not null
);
