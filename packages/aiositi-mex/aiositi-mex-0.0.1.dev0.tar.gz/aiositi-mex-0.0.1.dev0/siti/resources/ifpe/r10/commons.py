from pydantic import Field

from ...base import REGEX_NUMERIC, Resource


class InformacionFinanciera(Resource):
    conceto: str = Field(
        ..., min_length=12, max_length=12, regex=REGEX_NUMERIC
    )
    tipo_saldo: str = Field(
        ..., min_length=3, max_length=3, regex=REGEX_NUMERIC
    )
    tipo_movimiento: str = Field(
        ..., min_length=2, max_length=2, regex=REGEX_NUMERIC
    )
    dato: float
