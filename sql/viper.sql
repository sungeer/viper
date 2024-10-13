
CREATE TABLE users (
    id INT(10) NOT NULL AUTO_INCREMENT COMMENT 'ID',
    name VARCHAR(100) NOT NULL COMMENT '姓名',
    phone VARCHAR(20) NOT NULL COMMENT '手机',
    passwordHash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    is_admin TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否管理员',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',

    PRIMARY KEY (id) USING BTREE,
    UNIQUE KEY phone (phone),
    INDEX idx_created_time (created_time) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户';


CREATE TABLE chats (
    id INT(10) NOT NULL AUTO_INCREMENT COMMENT 'ID',
    conversation_id VARCHAR(100) NOT NULL COMMENT '大模型的会话ID',
    title VARCHAR(255) NOT NULL COMMENT '会话标题',
    user_id INT(10) NOT NULL COMMENT 't_users',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',

    PRIMARY KEY (id) USING BTREE,
    INDEX idx_user_id (user_id) USING BTREE,
    INDEX idx_created_time (created_time) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='会话';


CREATE TABLE messages (
    id INT(10) NOT NULL AUTO_INCREMENT COMMENT 'ID',
    chat_id INT(10) NOT NULL COMMENT 't_chats',
    trace_id VARCHAR(100) NOT NULL COMMENT '每次问答的配对',
    sender VARCHAR(50) NOT NULL COMMENT 'user or robot',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',

    PRIMARY KEY (id) USING BTREE,
    INDEX idx_chat_id (chat_id) USING BTREE,
    INDEX idx_created_time (created_time) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='消息';


CREATE TABLE contents (
    message_id INT(10) NOT NULL COMMENT 't_messages',
    content TEXT NOT NULL COMMENT '消息内容',

    INDEX idx_message_id (message_id) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='消息内容';

