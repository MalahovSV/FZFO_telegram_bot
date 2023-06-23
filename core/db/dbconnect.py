import asyncpg

class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def add_id_telegram(self, login, password, id_telegram):
        query = f"select * from Add_ID_UserTG('{login}','{password}', '{id_telegram}')"
        return await self.connector.fetchval(query)

    async def check_user_data(self, login, password):
        query = f"select * from check_data_user('{login}','{password}')"
        return await self.connector.fetchval(query)

    async def check_telegram_id(self, id):
        query = f"select * from check_id_telegram_user('{id}')"
        return await self.connector.fetchval(query)

    async def get_help_call_data (self, telegram_id, date_document):
        query = f"select * from get_data_for_document('{telegram_id}', '{date_document}')"
        return await self.connector.fetchrow(query)