import datetime as dt
from typing import Optional

from pydantic import Field

from ...http import Session, session as global_session
from ..base import Resource

# TODO: checar como generalizar los catálogos.


class ResourceIFPE(Resource):
    _endpoint: str = '/suptech-api/ifpe/1.0.0'
    _resource: str
    _folio: Optional[str]


class IdentificadorReporte(Resource):
    inicio_periodo: dt.date
    fin_periodo: dt.date
    clave_institucion: str = Field(..., min_length=6, max_length=6)
    # check how to assign this field automatically
    reporte: str = Field(..., min_length=3, max_length=5)


class ReportIFPE(ResourceIFPE):
    identificador_reporte: IdentificadorReporte


class Sendable(ResourceIFPE):
    async def send(self, *, session: Session = global_session, **data):
        resp = await session.post(
            f'{self._endpoint}{self._resource}',
            self.dict(to_camel_case=True, exclude_none=True),
            **data,
        )
        return resp


class Updateable(ResourceIFPE):
    async def update(self, *, session: Session = global_session, **data):
        resp = await session.put(
            f'{self._endpoint}{self._resource}/correccion/{self._folio}',
            self.dict(to_camel_case=True, exclude_none=True),
            **data,
        )
        return resp


class Resendable(ResourceIFPE):
    async def resend(self, *, session: Session = global_session, **data):
        resp = await session.put(
            f'{self._endpoint}{self._resource}/reenvio/{self._folio}',
            self.dict(to_camel_case=True, exclude_none=True),
            **data,
        )
        return resp
