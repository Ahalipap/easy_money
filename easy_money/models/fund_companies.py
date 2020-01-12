from models.__init__ import BaseModel


class FundCompaniesModel(BaseModel):
    table_name = 'fund_companies'

    def __init__(self, *, fond_code=None, fond_company_name=None, **kwargs):
        super().__init__(**kwargs)
        self.fond_code = fond_code
        self.fond_company_name = fond_company_name
