from datetime import datetime

from viper.models.base_model import BaseModel


class UserModel(BaseModel):

    async def get_user_by_phone(self, phone_number):
        sql_str = '''
            SELECT
                id, name, phone, password_hash, is_admin, created_time
            FROM
                users
            WHERE
                phone = %s
        '''
        await self.conn()
        await self.execute(sql_str, (phone_number,))
        user_info = await self.cursor.fetchone()
        await self.close()
        return user_info

    async def get_user_by_id(self, user_id):
        sql_str = '''
            SELECT
                id, name, phone, is_admin, created_time
            FROM
                users
            WHERE
                id = %s
        '''
        await self.conn()
        await self.execute(sql_str, (user_id,))
        user_info = await self.cursor.fetchone()
        await self.close()
        return user_info
