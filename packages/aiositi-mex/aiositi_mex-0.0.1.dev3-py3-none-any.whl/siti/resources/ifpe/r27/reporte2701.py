import datetime as dt
from typing import List, Optional

from ....http import Session, session as global_session
from ...base import Resource
from ..base import ReportIFPE, Resendable, Sendable, Updateable


class IdentificacionReclamacion(Resource):
    _date_format = '%Y-%m-%d'

    folio_reclamacion: str
    estatus_reclamacion: str
    fecha_actualizacion_estatus: str


class IdentificadorClienteCuentaMovimiento(Resource):
    identificador_cliente: str
    identificador_cuenta: str
    identificador_movimiento: str


class DetalleReclamacion(Resource):
    _date_format = '%Y-%m-%d'

    fecha_reclamacion: dt.date
    canal_recepcion_reclamacion: str
    tipo_reclamacion: str
    motivo_reclamacion: str
    descripcion_reclamacion: str


class DetalleEventoOriginaReclamacion(Resource):
    fecha_evento: dt.date
    objeto_evento: str
    canal_operacion: str
    importe_valorizado_moneda_nacional: int


class DetalleResoucion(Resource):
    _date_format = '%Y-%m-%d'

    fecha_resolucion: dt.date
    sentio_resolucon: str
    importe_abonado_cuenta_cliente: int
    fecha_abono_cuenta_cliente: dt.date
    identificador_cuenta_fideicomiso_institucion: str
    importe_recuperado: int
    fecha_recuperacion_recursos: dt.date
    identificador_cuenta_recibe_importe_recuperado: str
    quebranto_institucion: int
    # cambiar formato de fecha a '%Y-%m-%d


class InformacionSolicitada(Resource):
    identificacion_reclamacion: IdentificacionReclamacion
    identificador_cliente_cuenta_movimiento: IdentificadorClienteCuentaMovimiento  # noqa: E501
    detalle_reclamacion: DetalleReclamacion
    detalle_evento_origina_reclamacion: DetalleEventoOriginaReclamacion
    detalle_resolucion: DetalleResoucion


class Reporte2701(ReportIFPE, Sendable, Resendable, Updateable):
    _resource = '/IFPE/R27/2701'

    informacion_solicitada: Optional[List[InformacionSolicitada]]

    async def send(self, *, session: Session = global_session, **data):
        self._resource = '/IFPE/R27/2701'
        if not self.informacion_solicitada:
            self._resource = '/IFPE/R27/2701/envio-vacio'
        return await super().send(session=session, **data)
