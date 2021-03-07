# -*- coding: utf-8 -*-

import io

import pandas as pd

"""
from custom_exports.helpers.export_queryset import ExportQueryset
a=ExportQueryset(Action.objects.all(), ["id", "model__name"])

b=a.export_as_csv()
with open('test.csv', 'w') as f:
    f.write(b)
    f.close()

b=a.export_as_excel()
with open('test.xlsx', 'wb') as f:
    f.write(b)
    f.close()
"""


class ExportQueryset:
    def __init__(self, queryset, columns=None):
        self.queryset = queryset
        if columns is None:
            self.columns = [
                field.name for field in self.queryset.first()._meta.get_fields()
            ]
        else:
            self.columns = columns

    def export_as_csv(self, encoding="utf-8"):
        pdf = self._pandas_frame_from_queryset
        csv = pdf.to_csv(
            sep=";",
            index=True,
            encoding=encoding,
        )
        return csv

    def export_as_excel(self, sheet_name="Feuille1"):
        pdf = self._pandas_frame_from_list_of_dicts
        # Remove timezone from dataframe (not supported by excel)
        for col in pdf.select_dtypes(["datetimetz"]).columns:
            pdf[col] = pdf[col].dt.tz_convert(None)

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer) as writer:
            pdf.to_excel(
                excel_writer=writer,
                sheet_name=sheet_name,
                freeze_panes=(1, 1),
            )
        return buffer.getvalue()

    @property
    def _pandas_frame_from_queryset(self):
        df = pd.DataFrame(
            data=self.queryset.values_list(*self.columns),
            columns=self.columns,
        )
        df.set_index("id", drop=True, inplace=True)
        return df
