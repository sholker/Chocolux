create table payment_details
(
    id            int auto_increment
        primary key,
    user_ID       int          null,
    card_number   varchar(255) null,
    expride_date  varchar(255) null,
    security_code varchar(255) null,
    constraint payment_details_ibfk_1
        foreign key (user_ID) references users (id)
);

create index user_ID
    on payment_details (user_ID);

