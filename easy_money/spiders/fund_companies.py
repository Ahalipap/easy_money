import asyncio
import json
import uuid

import aiohttp

from models.fund_companies import FundCompaniesModel
from target_urls import fund_companies_urls


class FundCompaniesSpider:
    target_url = fund_companies_urls

    # total_page = 40
    def get_data(self):
        pass


async def fetch(session, url):
    async  with session.get(url) as response:
        return await response.text()


async def main():
    for i in range(1,41):
        async with aiohttp.ClientSession() as session:
            html = await fetch(session,
                               rf'http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=1&lx=1&letter=&gsid=&text=&sort=zdf,desc&page={i},200&dt=1578762717421&atfc=&onlySale=0')
            datas = html.split('var ')[1].split('db=')[1].split('datas:')[1]
            data_list = datas.split('],')
            print(len(data_list))
            for v in data_list:
                if v.split(',').__len__() != 21:
                    continue
                else:
                    fond_code = v.split(',')[0].replace('[', '').replace('"', '')
                    fond_company_name = v.split(',')[1].replace('"', '')
                    UUID = uuid.uuid5(namespace=uuid.NAMESPACE_OID, name=fond_code.__str__() + fond_company_name).__str__()
                    model = FundCompaniesModel(
                        uuid=UUID, fond_code=fond_code,
                        fond_company_name=fond_company_name)
                    await FundCompaniesModel(
                        uuid=UUID, fond_code=fond_code,
                        fond_company_name=fond_company_name).replace()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
