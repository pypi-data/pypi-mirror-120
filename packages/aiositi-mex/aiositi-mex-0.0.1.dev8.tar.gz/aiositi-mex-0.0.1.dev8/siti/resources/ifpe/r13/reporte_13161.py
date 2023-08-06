from typing import List

from ..base import ReportIFPE, Resendable, Sendable, Updateable
from .commons import InformacionFinanciera


class Reporte13161(ReportIFPE, Resendable, Sendable, Updateable):
    _resource = '/IFPE/R13/13161'

    informacion_financiera: List[InformacionFinanciera]
