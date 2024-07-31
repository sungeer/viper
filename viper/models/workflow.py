from datetime import datetime

from touch.models.base import BaseModel


class WorkflowModel(BaseModel):

    async def add_workflow(self, params):
        sql_str = '''
            INSERT INTO workflow (Name, Desc)
            VALUES (%s, %s);
        '''
        values = (params['name'], params['desc'])
        await self.conn()
        await self.execute(sql_str, values)
        await self.commit()
        lastrowid = self.cursor.lastrowid
        await self.close()
        return lastrowid
