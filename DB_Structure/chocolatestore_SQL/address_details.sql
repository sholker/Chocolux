create table address_details
(
    id      int auto_increment
        primary key,
    user_ID int          null,
    address varchar(255) null,
    city    varchar(255) null,
    country varchar(255) null,
    constraint address_details_ibfk_1
        foreign key (user_ID) references users (id)
);

create index user_ID
    on address_details (user_ID);

