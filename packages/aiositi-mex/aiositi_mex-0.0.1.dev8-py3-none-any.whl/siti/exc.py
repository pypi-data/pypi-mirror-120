class SitiException(Exception):
    """
    Exceptions returned by the SITI API
    """

    code: str
    desc: str

    def __init__(
        self, code: str = None, desc: str = None, *args: object
    ) -> None:
        super().__init__(*args)
        if code:
            self.code = code
        if desc:
            self.desc = desc

    def __str__(self) -> str:
        return self.desc


class InvalidCredentials(SitiException):
    """
    Invalid OAuth credentials
    """


class DateFormatError(SitiException):
    code = 'CLV_ERR_LFNSPP'
    desc = 'Las fechas no se pueden procesar.'


class UserNotFound(SitiException):
    code = 'CLV_ERR_NEEUIRE'
    desc = 'No existe el usuario con el que intenta realizar el envío.'


class DuplicateReport(SitiException):
    code = 'CLV_ERR_SHEOECPS'
    desc = (
        'Se ha encontrado otro envió correspondiente al periodo '
        'solicitado por lo que no se puede recibir otro igual.'
    )


class ReportNotFound(SitiException):
    code = 'CLV_ERR_NECRIRE'
    desc = (
        'No existe la clave del reporte con el que intenta realizar el envío.'
    )


class VersionNotFound(SitiException):
    code = 'CLV_ERR_NEVRP'
    desc = (
        'No existe una versión del reporte en el periodo con el '
        'que intenta realizar el envío.'
    )


class PeriodNotFound(SitiException):
    code = 'CLV_ERR_NEPR'
    desc = 'No existe el periodo que reporta.'


class PeriodNotStarted(SitiException):
    code = 'CLV_ERR_PENC'
    desc = 'El periodo de entrega aún no ha comenzado.'


class StructureError(SitiException):
    code = 'CLV_ERR_ESTR'
    desc = 'Error de estructura.'


class IndexNotFound(SitiException):
    code = 'CLV_ERR_IDNEX'
    desc = 'El folio no existe, verifique el dato y vuelva a intentarlo.'


class UnauthorizedInstitution(SitiException):
    code = 'CLV_ERR_SINTAUT'
    desc = 'Su institución no tiene autorización para usar ese folio.'


class DifferentDates(SitiException):
    code = 'CLV_ERR_FIFFNC'
    desc = 'La fecha de inicio y fin de periodo deben ser iguales.'


ERROR_CODES = {
    exc.code: exc
    for exc in [
        DateFormatError,
        UserNotFound,
        DuplicateReport,
        ReportNotFound,
        VersionNotFound,
        PeriodNotFound,
        PeriodNotStarted,
        StructureError,
        IndexNotFound,
        UnauthorizedInstitution,
        DifferentDates,
    ]
}
