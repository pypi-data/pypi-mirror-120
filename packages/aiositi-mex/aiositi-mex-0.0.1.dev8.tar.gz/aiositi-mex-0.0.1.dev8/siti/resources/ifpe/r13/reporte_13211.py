from typing import List

from ..base import ReportIFPE, Resendable, Sendable, Updateable
from .commons import InformacionFinancieraBase


class Reporte13211(ReportIFPE, Resendable, Sendable, Updateable):
    _resource = '/IFPE/R13/13211'

    informacion_financiera: List[InformacionFinancieraBase]
