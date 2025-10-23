pragma foreign_keys = on;

drop table if exists tasks;
drop table if exists usuarios;

create table if not exists usuarios (
  id         integer primary key autoincrement,
  correo     text unique not null,
  contrasena text not null,
  nombre     text
);

create table if not exists tasks (
  id             integer primary key autoincrement,
  usuario_id     integer not null,
  texto          text not null,
  fecha          text not null,
  done           integer not null default 0,
  created_at     real not null default (strftime('%s','now')),
  foreign key (usuario_id) references usuarios(id) on delete cascade
);
