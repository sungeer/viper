from viper.models.base import BaseModel


class RecordModel(BaseModel):

    async def add_record(self, params):
        sql_str = '''
            INSERT INTO record ('WorkflowID', 'NodeID', 'Status', 'Func', 'Result')
            VALUES (%s, %s, %s, %s, %s);
        '''
        values = (params['workflow_id'], params['node_id'], params['status'], params['func'], params['result'])
        await self.conn()
        await self.execute(sql_str, values)
        await self.commit()
        await self.close()
        return

    async def update_record(self, params):
        sql_str = '''
            UPDATE record
            SET Status = %s, Result = %s
            WHERE id = %s
        '''
        values = (params['status'], params['result'])
        await self.conn()
        await self.execute(sql_str, values)
        await self.commit()
        rowcount = self.cursor.rowcount
        await self.close()
        return rowcount

    async def get_records(self, params):
        sql_str = '''
            SELECT COUNT(*)
            FROM record
            WHERE WorkflowID = %s AND Group = %s AND Status = 'pending';
        '''
        values = (params['workflow_id'], params['group'])
        await self.conn()
        await self.execute(sql_str, values)
        records = await self.cursor.fetchall()
        await self.close()
        return records
