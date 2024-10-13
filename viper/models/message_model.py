from datetime import datetime

from viper.models.base_model import BaseModel


class MessageModel(BaseModel):

    async def add_message(self, chat_id, trace_id, sender):
        sql_str = '''
            INSERT INTO messages (chat_id, trace_id, sender) 
            VALUES (%s, %s, %s)
        '''
        await self.conn()
        await self.execute(sql_str, (chat_id, trace_id, sender))
        await self.commit()
        lastrowid = self.cursor.lastrowid
        await self.close()
        return lastrowid

    async def get_messages(self, chat_id):
        sql_str = '''
            SELECT
                trace_id,
                MAX(CASE WHEN sender = 'user' THEN content END) AS 问题,
                MAX(CASE WHEN sender = 'robot' THEN content END) AS 回答,
                MAX(CASE WHEN sender = 'user' THEN created_time END) AS 问题时间,
                MAX(CASE WHEN sender = 'robot' THEN created_time END) AS 回答时间
            FROM
                (
                    SELECT
                        m.trace_id, ct.content, m.sender, m.created_time
                    FROM
                        chats c
                        LEFT JOIN messages M ON c.id = m.chat_id
                        LEFT JOIN contents CT ON m.id = ct.message_id
                    WHERE
                        c.conversation_id = %s
                ) AS subquery
            GROUP BY
                trace_id
            LIMIT 100;
        '''
        await self.conn()
        await self.execute(sql_str, (chat_id,))
        chats = await self.cursor.fetchall()
        await self.close()
        return chats
