
-- 删除表中所有行，并重置自增列
TRUNCATE TABLE table_name;


CREATE TABLE workflow (
    id INT(10) NOT NULL AUTO_INCREMENT COMMENT 'ID',
    name VARCHAR(255) NOT NULL COMMENT '流程名称',
    description TEXT NOT NULL COMMENT '描述',

    PRIMARY KEY (id) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='流程';


CREATE TABLE node (
    id INT(10) NOT NULL AUTO_INCREMENT COMMENT 'ID',
    workflow_id INT(10) NOT NULL COMMENT 't_workflow',
    name VARCHAR(255) NOT NULL COMMENT '节点名称',
    node_order INT NOT NULL COMMENT '节点顺序',
    func VARCHAR(255) NOT NULL COMMENT '调用的接口',
    node_group INT(10) DEFAULT 0 COMMENT '并行调用组',

    PRIMARY KEY (id) USING BTREE,
    INDEX idx_workflow_id (workflow_id) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='节点';


CREATE TABLE record (
    id INT(10) NOT NULL AUTO_INCREMENT COMMENT 'ID',
    workflow_id INT(10) NOT NULL COMMENT 't_workflow',
    node_id INT(10) NOT NULL COMMENT 't_node',
    status ENUM('pending', 'active', 'done') DEFAULT 'pending' COMMENT '执行状态',
    func VARCHAR(255) NOT NULL COMMENT '调用的接口',
    result TEXT COMMENT '执行结果',
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id) USING BTREE,
    INDEX idx_workflow_id (workflow_id) USING BTREE,
    INDEX idx_node_id (node_id) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='节点执行';

-- ext

CREATE TABLE users (
    id INT(10) NOT NULL AUTO_INCREMENT COMMENT 'ID',
    name VARCHAR(100) NOT NULL COMMENT '姓名',
    gender ENUM('男', '女') NOT NULL COMMENT '性别',
    birth DATE NOT NULL COMMENT '出生年份',
    phone VARCHAR(20) NOT NULL COMMENT '手机',
    address VARCHAR(50) NOT NULL COMMENT '地区',
    comment VARCHAR(255) NULL DEFAULT NULL COMMENT '备注',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id) USING BTREE,
    UNIQUE KEY uniq_phone (phone),
    INDEX idx_created_time (created_time) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='客户';


CREATE TABLE user_sources (
    id INT(10) NOT NULL AUTO_INCREMENT COMMENT 'ID',
    name VARCHAR(100) NOT NULL COMMENT '来源',

    PRIMARY KEY (id) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='客户来源';


CREATE TABLE user_source_relations (
    id INT(10) NOT NULL AUTO_INCREMENT COMMENT 'ID',
    user_id INT(10) NOT NULL COMMENT 't_users',
    source_id INT(10) NOT NULL COMMENT 't_user_sources',

    PRIMARY KEY (id) USING BTREE,
    INDEX idx_user_id (user_id) USING BTREE,
    INDEX idx_source_id (source_id) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='客户-来源关系';


CREATE TABLE jobs (
    id INT(10) NOT NULL AUTO_INCREMENT COMMENT 'ID',
    name VARCHAR(100) NOT NULL COMMENT '职业',

    PRIMARY KEY (id) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='职业';


CREATE TABLE goods (
    id INT(10) NOT NULL AUTO_INCREMENT COMMENT 'ID',
    name VARCHAR(100) NOT NULL COMMENT '商品',
    descr VARCHAR(255) NOT NULL COMMENT '商品描述',
    price DOUBLE(10, 2) NOT NULL COMMENT '销售价格',
    num INT(11) NOT NULL COMMENT '数量',
    unit VARCHAR(255) NOT NULL COMMENT '商品规格',
    pack VARCHAR(255) NOT NULL COMMENT '包装单位',
    img VARCHAR(255) NOT NULL COMMENT '商品图片',
    product_num VARCHAR(255) NOT NULL  COMMENT '生产批号',
    approve_num VARCHAR(255) NOT NULL  COMMENT '批准文号',
    status ENUM('可用', '禁用') DEFAULT '可用' COMMENT '状态',

    PRIMARY KEY (id) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='职业';


CREATE TABLE sales (
    id INT(10) NOT NULL AUTO_INCREMENT COMMENT 'ID',
    name VARCHAR(100) NOT NULL COMMENT '购买标识',
    pay_type VARCHAR(100) NOT NULL COMMENT '支付类型',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id) USING BTREE,
    INDEX idx_created_time (created_time) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='购买单';


CREATE TABLE sale_goods (
    id INT(10) NOT NULL AUTO_INCREMENT COMMENT 'ID',
    sale_id INT(10) NOT NULL COMMENT 't_sales',
    goods_id INT(10) NOT NULL COMMENT 't_goods',
    price DOUBLE NOT NULL COMMENT '销售单价',
    num INT(11) NOT NULL COMMENT '销售数量',
    unit VARCHAR(255) NOT NULL COMMENT '商品规格',
    total DOUBLE(10, 2) NOT NULL COMMENT '销售总价',
    comment VARCHAR(255) NOT NULL COMMENT '备注',

    PRIMARY KEY (id) USING BTREE,
    INDEX idx_sale_id (sale_id) USING BTREE,
    INDEX idx_goods_id (goods_id) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='商品-购买单关系';


CREATE TABLE user_sales (
    id INT(10) NOT NULL AUTO_INCREMENT COMMENT 'ID',
    user_id INT(10) NOT NULL COMMENT 't_users',
    sale_id INT(10) NOT NULL COMMENT 't_sales',

    PRIMARY KEY (id) USING BTREE,
    INDEX idx_user_id (user_id) USING BTREE,
    INDEX idx_sale_id (sale_id) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='客户-购买单关系';







