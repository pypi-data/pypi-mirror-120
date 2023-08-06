import math
from common.okex.client import AsyncClient


class OkexService:
    def __init__(self, client: AsyncClient):
        self.client = client

    async def cancel_all_orders(self, instId_list: [str]):
        """
        全部撤单
        """
        rst = await self.client.pending_orders()
        orders = rst.data
        payload = [{
            "ordId": order['ordId'],
            "instId": order['instId']
        } for order in orders if order['instId'] in instId_list]

        if payload:
            await self.client.batch_cancel_orders(payload)

    async def get_price_tick_size(self, instType, instId) -> int:
        # 获取交易价格精度
        rst = await self.client.instruments(instType=instType, instId=instId)
        return int(abs(math.log10(float(rst.data[0]['tickSz']))))
