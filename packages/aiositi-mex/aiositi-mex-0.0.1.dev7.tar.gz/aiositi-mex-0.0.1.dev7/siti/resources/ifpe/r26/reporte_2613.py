from typing import List, Optional

from ....http import Session, session as global_session
from ...base import Resource
from ..base import ReportIFPE, Resendable, Sendable, Updateable


class IdentificacionAdministrador(Resource):
    identificador_administrador: str


class IdentificacionComisionista(Resource):
    identificador_comisionista: str


class IdentificadorModulosEstablecimientos(Resource):
    clave_modulo_establecimiento: str


class InformacionOperativa(Resource):
    numero_modulo_establecimiento_comisionistas: int


class ClasificadoresAgrupacion(Resource):
    medio_pago_utilizado: str
    tipo_operacion_realizada: str


class MovimientosOperaciones(Resource):
    numero_operaciones_realizadas_comisionista: int
    monto_operaciones_realizadas_valorizadas_nacional: float
    numero_clientes_instituciones_realizaron_operaciones: int


class InformacionOperaciones(Resource):
    clasificadores_agrupacion: ClasificadoresAgrupacion
    movimientos_operaciones: MovimientosOperaciones


class InformacionSolicitada(Resource):
    identificacion_administrador: IdentificacionAdministrador
    identificacion_comisionista: IdentificacionComisionista
    identificador_modulos_establecimientos: IdentificadorModulosEstablecimientos  # noqa: E501
    informacion_operativa: InformacionOperativa
    informacion_operaciones: List[InformacionOperaciones]


class Reporte2613(ReportIFPE, Sendable, Updateable, Resendable):
    _resource = '/IFPE/R26/2613'

    informacion_solicitada: Optional[List[InformacionSolicitada]]

    async def send(self, *, session: Session = global_session, **data):
        self._resource = '/IFPE/R26/2613'
        if not self.informacion_solicitada:
            self._resource = '/IFPE/R26/2613/envio-vacio'
        return await super().send(session=session, **data)
