CREATE TABLE order_info(
   id INTEGER(10) NOT NULL PRIMARY KEY,
   receivcer VARCHAR(128) NOT NULL,
   order_status TINYINT(3) NOT NULL, -- 订单状态：0 退货，1 退改，2 丢件 3 其他
   order_number INT(50),
   apply_time VARCHAR(50),
   wangwang_number VARCHAR(50),
   goods_number VARCHAR(50),
   mail_pd_number VARCHAR(50),
   return_pd_company VARCHAR(250),
   return_pd_number VARCHAR(50),
   update_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
   is_delete TINYINT(3) NOT NULL DEFAULT 0,  -- 逻辑删除：0 保留，1 删除
   delete_time timestamp NOT NULL DEFAULT '1970-01-01 13:00:01'
);