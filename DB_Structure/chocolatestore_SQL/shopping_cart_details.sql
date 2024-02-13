create definer = root@localhost view shopping_cart_details as
select `u`.`id`                        AS `user_ID`,
       `sc`.`id`                       AS `cart_ID`,
       `i`.`ItemName`                  AS `Item_name`,
       `i`.`image_path`                AS `image_path`,
       `i`.`price`                     AS `price`,
       `sc`.`quantity`                 AS `item_quantity`,
       (`i`.`price` * `sc`.`quantity`) AS `total_price`
from ((`chocolatestore`.`shopping_cart` `sc` join `chocolatestore`.`users` `u`
       on ((`sc`.`user_Id` = `u`.`id`))) join `chocolatestore`.`items` `i` on ((`sc`.`item_Id` = `i`.`id`)))
where ((`u`.`id` = `sc`.`user_Id`) and (`sc`.`item_Id` = `i`.`id`));

