from datetime import datetime

from viper.models.base_model import BaseModel


class ChatModel(BaseModel):

    async def add_chat(self, conversation_id, title, user_id):
        sql_str = '''
            INSERT INTO 
                chats 
                (conversation_id, title, user_id) 
            VALUES 
                (%s, %s, %s)
        '''
        values = (conversation_id, title, user_id)
        await self.conn()
        await self.execute(sql_str, values)
        await self.commit()
        lastrowid = self.cursor.lastrowid
        await self.close()
        return lastrowid

    async def get_chats(self, user_id):
        sql_str = '''
            SELECT
                id, conversation_id, title, created_time
            FROM
                chats
            WHERE
                user_id = %s
            LIMIT 100
        '''
        await self.conn()
        await self.execute(sql_str, (user_id,))
        chats = await self.cursor.fetchall()
        await self.close()
        return chats

    async def get_chat_by_conversation(self, conversation_id):
        sql_str = '''
            SELECT 
                id, conversation_id, title, created_time
            FROM 
                chats
            WHERE
                conversation_id = %s
        '''
        await self.conn()
        await self.execute(sql_str, (conversation_id,))
        chat_info = await self.cursor.fetchone()
        await self.close()
        return chat_info
