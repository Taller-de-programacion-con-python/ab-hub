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

insert into usuarios (correo, contrasena, nombre) values
  ('ana@ucol.mx', 'Ana12345', 'Ana'),
  ('luis@ucol.mx', 'Luis2025', 'Luis'),
  ('edson@ucol.mx','Python2025', 'Edson'),
  ('renata@ucol.mx','Renata2025', 'Renata'),
  ('ivan@ucol.mx', 'Ivan2025', 'Ivan');

insert into tasks (usuario_id, texto, fecha, done) values
  ((select id from usuarios where correo = 'ana@ucol.mx'),
   'Preparar la presentacion del sprint', '2024-05-10', 0),
  ((select id from usuarios where correo = 'luis@ucol.mx'),
   'Revisar pull requests pendientes', '2024-05-08', 0),
  ((select id from usuarios where correo = 'edson@ucol.mx'),
   'Actualizar documentacion tecnica', '2024-05-12', 0),
  ((select id from usuarios where correo = 'renata@ucol.mx'),
   'Enviar correo de seguimiento a clientes', '2024-05-09', 1),
  ((select id from usuarios where correo = 'ivan@ucol.mx'),
   'Disenar pruebas automatizadas', '2024-05-11', 0);
