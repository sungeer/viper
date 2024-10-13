from datetime import datetime

from viper.models.base_model import BaseModel


class UserModel(BaseModel):

    async def get_user_by_phone(self, phone_number):
        sql_str = '''
            SELECT
                ID, Name, Phone, PasswordHash, IsAdmin, CreatedTime
            FROM
                users
            WHERE
                Phone = %s
        '''
        await self.conn()
        await self.execute(sql_str, (phone_number,))
        user_info = await self.cursor.fetchone()
        await self.close()
        return user_info
