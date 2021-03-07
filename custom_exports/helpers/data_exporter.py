# -*- coding: utf-8 -*-

import io
import logging

import pandas as pd

from .data_adapter import DataAdapter


logger = logging.getLogger(__name__)  # NOQA

"""
de = DataExporter(
   rows=[
       {'pk': 1, 'name': 'Test1', 'value': '123'},
       {'pk': 2, 'name': 'Test2', 'value': '245'},
   ],
   columns=[
       { 'field': 'pk', 'title':'ID'},
       { 'field': 'name', 'title':'Nom', 'fct': 'truncate', 'arg': 100 },
       { 'field': 'value', 'title':'Valeur', 'fct': 'int' },
   ],
)
"""


class DataExporter:
    class DataExporterError(Exception):
        pass

    def __init__(
        self,
        rows: list,
        columns: list,
        data_adapter: DataAdapter = None,
    ) -> None:
        logger.info(f"DataExporter:init {len(rows)} rows")

        self.data_adapter = data_adapter if data_adapter is not None else DataAdapter()

        self.columns = columns
        self.columns_names = [x["title"] for x in columns]
        self.rows = rows

    def export_as_csv(
        self,
        field_delimiter: str = ",",
        newline: str = "\n",
        list_separator: str = ", ",
        header: bool = True,
    ):
        rows = self.data_adapter.convert(
            columns=self.columns, rows=self.rows, list_separator=list_separator
        )

        pdf = self._pandas_frame(rows)

        if len(field_delimiter) == 1:
            csv = pdf.to_csv(
                # can't use with more than one char sep="",
                index=True,
                sep=field_delimiter,
                header=header,
                line_terminator=newline,
            )
        else:
            csv_rows = []
            for row in pdf.iterrows():
                cid = row[0]
                data = [
                    str(x).replace(field_delimiter, "--") for x in [cid] + list(row[1])
                ]

                csv_rows.append(field_delimiter.join(data))

            csv = newline.join(csv_rows)

        return csv

    def export_as_csv_with_encoding(
        self,
        encoding="utf-8",
        field_delimiter: str = ",",
        newline: str = "\n",
        list_separator: str = ", ",
        header: bool = True,
    ):
        csv = self.export_as_csv(
            field_delimiter=field_delimiter,
            newline=newline,
            list_separator=list_separator,
            header=header,
        )
        encoded_csv = csv.encode(encoding, "replace")
        # Beware, will return a binary
        return encoded_csv

    def export_as_sare(self):
        csv = self.export_as_csv_with_encoding(
            encoding="Windows-1252",
            field_delimiter="|;|",
            newline="\r\n",
            list_separator="_/_",
            header=False,
        )
        # Beware, will return a binary
        return csv

    def export_as_excel(self, sheet_name="Feuille1", list_separator: str = ", "):
        rows = self.data_adapter.convert(
            columns=self.columns, rows=self.rows, list_separator=list_separator
        )

        pdf = self._pandas_frame(rows)

        # Remove timezone from dataframe (not supported by excel)
        # > for col in pdf.select_dtypes(["datetimetz"]).columns:
        # >   pdf[col] = pdf[col].dt.tz_convert(None)

        iobuffer = io.BytesIO()
        with pd.ExcelWriter(iobuffer) as writer:
            pdf.to_excel(
                excel_writer=writer,
                sheet_name=sheet_name,
                freeze_panes=(1, 1),
            )
        return iobuffer.getvalue()

    def _pandas_frame(self, rows):
        # until python3.7, dict order is not guaranted
        # so order series as defined in columns
        pd_rows = [[row[x["field"]] for x in self.columns] for row in rows]

        df = pd.DataFrame(pd_rows, columns=self.columns_names)
        try:
            title_for_id = [x["title"] for x in self.columns if x["field"] == "ID"][0]
        except IndexError:
            pass
        else:
            df.set_index(title_for_id, drop=True, inplace=True)

        return df
