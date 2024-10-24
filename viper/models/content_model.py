from datetime import datetime

from viper.models.base_model import BaseModel


class ContentModel(BaseModel):

    async def add_content(self, message_id, content):
        sql_str = '''
            INSERT INTO 
                contents 
                (message_id, content) 
            VALUES 
                (%s, %s)
        '''
        await self.conn()
        await self.execute(sql_str, (message_id, content))
        await self.commit()
        lastrowid = self.cursor.lastrowid
        await self.close()
        return lastrowid
