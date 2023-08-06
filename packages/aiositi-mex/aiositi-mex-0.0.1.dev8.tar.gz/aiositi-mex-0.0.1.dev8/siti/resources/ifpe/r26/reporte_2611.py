from typing import List

from ...base import Resource
from ..base import ReportIFPE, Resendable, Sendable, Updateable


class IdentificacionAdministrador(Resource):
    identificador_administrador: str


class IdentificacionComisionista(Resource):
    tipo_movimiento: str
    identificador_comisionista: str
    nombre_comisionista: str
    rfc_comisionista: str
    personalidad_juridica_comisionista: str
    modalidad_comercial_comisionista: str
    nombre_comercial: str


class OperacionesContratadasComisionista(Resource):
    operaciones_contratadas: List[str]


class BajaComisionista(Resource):
    causa_baja_comisionista: str


class InformacionSolicitada2611(Resource):
    identificacion_administrador: IdentificacionAdministrador
    identificacion_comisionista: IdentificacionComisionista
    operaciones_contratadas_comisionista: OperacionesContratadasComisionista
    baja_comisionista: BajaComisionista


class Reporte2611(ReportIFPE, Sendable, Updateable, Resendable):
    _resource = '/IFPE/R26/2611'

    informacion_solicitada: List[InformacionSolicitada2611]
