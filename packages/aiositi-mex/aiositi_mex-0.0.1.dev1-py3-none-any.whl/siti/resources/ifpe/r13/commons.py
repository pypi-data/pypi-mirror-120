from ..base import Resource


class InformacionFinancieraBase(Resource):
    concepto: str
    dato: float


class InformacionFinanciera(InformacionFinancieraBase):
    tipo_saldo: str
