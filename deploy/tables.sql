CREATE TABLE `tb_order_info`(
   `id` INTEGER NOT NULL,
   `receiver` VARCHAR(128) NOT NULL,
   `order_status` TINYINT(3) NOT NULL, -- 订单状态：1 退货，2 退改，3 丢件 4 其他
   `order_id` INT(50) NOT NULL ,
   `apply_time` VARCHAR(50),
   `wangwang_id` VARCHAR(50),
   `goods_id` VARCHAR(50),
   `mail_pd_id` VARCHAR(50),
   `return_pd_company` VARCHAR(250),
   `return_pd_id` VARCHAR(50),
   `comment` VARCHAR(500),
   `update_time` TIMESTAMP DEFAULT (DATETIME('now', 'localtime')),
   `is_delete` TINYINT(3) DEFAULT 0,  -- 逻辑删除：0 保留，1 删除
   `delete_time` TIMESTAMP DEFAULT '1970-01-01 13:00:01',
   PRIMARY KEY(`id`),
   UNIQUE (`order_id`)
);
