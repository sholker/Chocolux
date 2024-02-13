create table items
(
    id         int auto_increment
        primary key,
    ItemName   varchar(255) null,
    price      int          null,
    desciption longtext     null,
    image_path varchar(255) null,
    quantity   varchar(255) null,
    outOfStock tinyint(1)   null,
    lastUpdate datetime     null,
    constraint ItemName
        unique (ItemName)
);

