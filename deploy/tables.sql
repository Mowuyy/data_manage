CREATE TABLE order_info(
   id INT(10)  NOT NULL,
   receicer VARCHAR(128) NOT NULL,
   order_status TINYINT(3) NOT NULL, -- 订单状态：0 退货，1 退改，2 丢件 3 其他
   order_number INT(50),
   apply_time VARCHAR(50),
   wangwang VARCHAR(50),
   goods_number VARCHAR(50),
   mail_physical_distribution_number VARCHAR(50),
   return_physical_company VARCHAR(250),
   return_physical_distribution_number VARCHAR(50),
   PRIMARY KEY (`id`)
);