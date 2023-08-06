import datetime as dt
from enum import Enum
from typing import Any, Dict, List

import pandas as pd
from pydantic import BaseModel

from ..utils import dict_to_camel_case, dict_to_snake_case

REGEX_NUMERIC = r'^\d*$'
REGEX_CAP_NUM = r'^[A-Z0-9\-\s]*$'


class Resource(BaseModel):
    _date_format = '%Y%m%d'

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        transformed = dict_to_snake_case(d)
        return cls(**transformed)

    def dict(self, to_camel_case: bool = False, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        res = {}
        for key, value in d.items():
            if isinstance(value, dt.date) or isinstance(value, dt.datetime):
                res[key] = value.strftime(self._date_format)
            elif isinstance(value, Enum):
                res[key] = value.value
            else:
                res[key] = value
        if to_camel_case:
            res = dict_to_camel_case(res)
            res = res
        return res

    @classmethod
    def from_dataframe(cls, name: str, df: pd.DataFrame):
        """
        el nombre debe de venir en formato:
        CLAVEINSTITUCION_REPORTE_YYYYMMDD.csv
        ejemplo:
        065014_2610_20210831.csv
        """
        list_field_name = (
            'informacion_solicitada'
            if 'informacion_solicitada' in cls.__fields__
            else 'informacion_financiera'
        )
        list_element_cls = cls.__fields__[list_field_name].type_
        identificador_reporte_cls = cls.__fields__[
            'identificador_reporte'
        ].type_

        elements_for_list = []
        for _, row in df.iterrows():
            elements_for_list.append(list_element_cls._from_series(row))

        name = name.replace('.csv', '')
        name_fields = name.split('_')
        identificador_reporte = identificador_reporte_cls(
            inicio_periodo=dt.datetime.strptime(name_fields[2], '%Y%m%d'),
            fin_periodo=dt.datetime.strptime(name_fields[2], '%Y%m%d'),
            clave_institucion=name_fields[0],
            reporte=name_fields[1],
        )

        obj = {
            list_field_name: elements_for_list,
            'identificador_reporte': identificador_reporte,
        }

        return cls(**obj)

    @classmethod
    def _from_series(cls, row: pd.Series):
        obj = dict()
        for k, v in cls.__fields__.items():
            if v.outer_type_ == List:
                if v.type_ == str:
                    obj[k] = row[v.name].split(',')
                elif issubclass(v.type_, BaseModel):
                    obj[k] = [v.type_._from_series(row)]
                # TODO: checar qué hacer cuando .type_ es diferente a str
            elif issubclass(v.type_, BaseModel):
                obj[k] = v.type_._from_series(row)
            else:
                obj[k] = row[v.name]

        return cls(**obj)
