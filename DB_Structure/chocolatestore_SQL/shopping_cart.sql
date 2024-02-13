create table shopping_cart
(
    id         int auto_increment
        primary key,
    user_Id    int      null,
    item_Id    int      null,
    quantity   int      null,
    lastUpdate datetime null,
    constraint shopping_cart_ibfk_1
        foreign key (user_Id) references users (id),
    constraint shopping_cart_ibfk_2
        foreign key (item_Id) references items (id)
);

create index item_Id
    on shopping_cart (item_Id);

create index user_Id
    on shopping_cart (user_Id);

