create definer = root@localhost view user_order_totals as
select `u`.`id`         AS `user_ID`,
       `u`.`username`   AS `username`,
       `u`.`firstname`  AS `firstname`,
       `u`.`lastname`   AS `lastname`,
       count(`o`.`id`)  AS `count_orders`,
       sum(`o`.`total`) AS `total_orders`
from (`chocolatestore`.`users` `u` left join `chocolatestore`.`orders` `o` on ((`u`.`id` = `o`.`user_ID`)))
group by `u`.`id`
having (count(`o`.`id`) > 0)
order by `total_orders` desc;

