create table orders
(
    id         int auto_increment
        primary key,
    order_ID   varchar(255) null,
    user_ID    int          null,
    address_ID int          null,
    payment_ID int          null,
    total      int          null,
    order_date datetime     null,
    constraint orders_ibfk_1
        foreign key (user_ID) references users (id),
    constraint orders_ibfk_2
        foreign key (address_ID) references address_details (id),
    constraint orders_ibfk_3
        foreign key (payment_ID) references payment_details (id)
);

create index address_ID
    on orders (address_ID);

create index payment_ID
    on orders (payment_ID);

create index user_ID
    on orders (user_ID);

