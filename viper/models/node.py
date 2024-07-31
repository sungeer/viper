from datetime import datetime

from touch.models.base import BaseModel


class NodeModel(BaseModel):

    async def add_node(self, params):
        sql_str = '''
            INSERT INTO node ('WorkflowID', 'Name', 'Order', 'Func', 'Group')
            VALUES (%s, %s, %s, %s, %s);
        '''
        values = (params['workflow_id'], params['name'], params['order'], params['func'], params['group'])
        await self.conn()
        await self.execute(sql_str, values)
        await self.commit()
        await self.close()
        return
