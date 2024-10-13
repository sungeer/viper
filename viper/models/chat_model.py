from datetime import datetime

from viper.models.base_model import BaseModel


class ChatModel(BaseModel):

    async def add_chat(self, conversation_id, title, user_id):
        sql_str = '''
            INSERT INTO 
                chats 
                (ConversationID, Title, UserID) 
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
                ID, ConversationID, Title, CreatedTime
            FROM
                chats
            WHERE
                UserID = %s
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
                ID, ConversationID, Title, CreatedTime
            FROM 
                chats
            WHERE
                ConversationID = %s
        '''
        await self.conn()
        await self.execute(sql_str, (conversation_id,))
        chat_info = await self.cursor.fetchone()
        await self.close()
        return chat_info
