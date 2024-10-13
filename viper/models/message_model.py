from datetime import datetime

from viper.models.base_model import BaseModel


class MessageModel(BaseModel):

    async def add_message(self, chat_id, trace_id, sender):
        sql_str = '''
            INSERT INTO 
                messages 
                (ChatID, TraceID, Sender) 
            VALUES 
                (%s, %s, %s)
        '''
        await self.conn()
        await self.execute(sql_str, (chat_id, trace_id, sender))
        await self.commit()
        last_rowid = self.cursor.lastrowid
        await self.close()
        return last_rowid

    async def get_messages(self, chat_id):
        sql_str = '''
            SELECT
                TraceID,
                MAX(CASE WHEN Sender = 'user' THEN Content END) AS 问题,
                MAX(CASE WHEN Sender = 'robot' THEN Content END) AS 回答,
                MAX(CASE WHEN Sender = 'user' THEN CreatedTime END) AS 问题时间,
                MAX(CASE WHEN Sender = 'robot' THEN CreatedTime END) AS 回答时间
            FROM
                (
                    SELECT
                        M.TraceID, CT.Content, M.Sender, M.CreatedTime
                    FROM
                        chats C
                        LEFT JOIN messages M ON C.ID = M.ChatID
                        LEFT JOIN contents CT ON M.ID = CT.MessageID
                    WHERE
                        C.ConversationID = %s
                ) AS subquery
            GROUP BY
                TraceID
            LIMIT 100;
        '''
        await self.conn()
        await self.execute(sql_str, (chat_id,))
        chats = await self.cursor.fetchall()
        await self.close()
        return chats
