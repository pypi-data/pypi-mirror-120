from typing import List

from ...base import Resource
from ..base import ReportIFPE, Resendable, Sendable, Updateable


class IdentificadorComisionista(Resource):
    identificador_comisionista: str


class IdentificadorModuloEstablecimiento(Resource):
    tipo_movimiento: str
    clave_modulo_establecimiento: str
    rfc_modulo_establecimiento: str
    clave_localidad_modulo_establecimiento: str
    clave_estado_modulo_establecimiento: str
    clave_municipio_moldulo_establecimiento: str  # la api dice moldulo
    codigo_postal_modulo_establecimiento: str
    latitud_ubicacion_modulo_establecimiento: str
    longitud_ubicacion_modulo_establecimiento: str


class BajaModuloEstablecimiento(Resource):
    causa_baja_modulo_establecimiento: str


class InformacionSolicitada(Resource):
    identificador_comisionista: IdentificadorComisionista
    identificador_modulo_establecimiento: IdentificadorModuloEstablecimiento
    baja_modulo_establecimiento: BajaModuloEstablecimiento


class Reporte2612(ReportIFPE, Sendable, Updateable, Resendable):
    _resource = '/IFPE/R26/2612'

    informacion_solicitada: List[InformacionSolicitada]
