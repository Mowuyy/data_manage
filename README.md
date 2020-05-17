# data_manage

## 1、淘宝后台数据管理系统

## 2、功能介绍

 - 首页：欢迎进入数据管理系统
 
 - 订单管理
    - 订单导入
        - 单个录入：寄件物流号、收件人、订单状态、订单号、申请时间、旺旺号、产品型号、退货物流公司、退货物流号、备注、上传附件
        - 批量导入
    - 订单展示
        - 列表页：删除
        - 详情页：修改
        
 - 库存管理
    - 产品入库
    - 产品展示
        - 列表页：删除
        - 详情页：修改
        
 - 数据分析
        
 - 回收站
    - 订单
    - 库存
    
## 3、环境依赖

```bash
# python3.6
cd deploy/
pip install -r requirements.txt
cd src/web/db/
sqlite3 data_mgr_product.db
# 复制deploy/tables.sql里的tb_order_info表构建
```

- 启动
```bash
python src/web/manage.py
```

- 访问浏览器：http://127.0.0.1
