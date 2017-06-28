CREATE TABLE IF NOT EXISTS agent (
  id                INTEGER PRIMARY KEY  AUTOINCREMENT,
  ip                VARCHAR(20) NOT NULL,
  cpu_idle          VARCHAR(20) NOT NULL,
  cpu_count         INT(10)     NOT NULL,
  cpu_logical_count INT(10)     NOT NULL,
  cpu_user          VARCHAR(20) NOT NULL,
  cpu_nice          VARCHAR(20) NOT NULL,
  cpu_system        VARCHAR(20) NOT NULL,
  nginx_ok          BOOLEAN     NOT NULL,
  fpm_ok            BOOLEAN     NOT NULL,
  boot_time         VARCHAR(20) NOT NULL,
  php_version       VARCHAR(10) NOT NULL,
  create_time       INT(10)     NOT NULL,
  nginx_version     VARCHAR(10) NOT NULL,
  memory_total      INT(10)     NOT NULL,
  memory_used       INT(10)     NOT NULL,
  memory_free       INT(10)     NOT NULL
);


CREATE TABLE IF NOT EXISTS disk (
  id          INTEGER PRIMARY KEY  AUTOINCREMENT,
  agent_id    INT(10)     NOT NULL,
  disk_name   VARCHAR(10) NOT NULL,
  total       INT(10)     NOT NULL,
  used        INT(10)     NOT NULL,
  percent     VARCHAR(10) NOT NULL,
  fstype      VARCHAR(10) NOT NULL,
  create_time INT(10)     NOT NULL
);
