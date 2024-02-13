create table users
(
    id        int auto_increment
        primary key,
    firstname varchar(255)         null,
    lastname  varchar(255)         null,
    email     varchar(255)         null,
    username  varchar(255)         null,
    password  varchar(255)         null,
    userType  tinyint(1) default 0 null
);

