import io
import math
import string
from datetime import date

import xlsxwriter

from fac.static_data import ACTIMMO_TAGS_PREFIXES


def _case(row, col):
    return f"{string.ascii_uppercase[col]}{row+1}"


def _if_divide_zero(operation):
    dividend = operation.split("/")[-1].strip()
    return f"=IF({dividend} = 0, 0, {operation.strip('=')})"


def create_xlsx(  # NOQA: CFQ001
    groups: [str],
    project_statistics: dict,
    project_statistics_laureates: list,
    export_actions: bool = True,
    export_statistics: bool = True,
) -> (str, bytes):
    """
    Create an XLSX file
    :groups: the Groups selected in the export
    :project_statistics: a dict from ProjectStatisticsSerializer.data
    :project_statistics_laureates: a list of tuples (Group, dict). the dicts are
                                         from ProjectStatisticsSerializer.data,
                                         corresponding to all the laureates we are seeing
    :export_actions: whether export actions or not
    :export_statistics: whether export budgets/statistics or not
    :return: filename, file_bytes : the bytes of the xlsx file along with its filename
    """

    xlsx_output = io.BytesIO()
    workbook = xlsxwriter.Workbook(xlsx_output)

    # ********* Create formats *********

    # TODO améliorer la gestion des formats
    # Actuellement c'est un peu foireux je trouve, c'est pas normal qu'on se
    # retrouve à les passer comme ça en paramètres de toutes les fonctions,
    # c'est illisible et hyper fastidieux quand on doit en rajouter un.

    title_cell_format = workbook.add_format({"font_size": 22})
    folder_name_format = workbook.add_format({"font_size": 16})
    table_title_format = workbook.add_format({"font_size": 12, "italic": True})
    top_bordered = workbook.add_format({"top": 1})
    left_bordered = workbook.add_format({"left": 1})
    header_wrap_format = workbook.add_format(
        {"text_wrap": 1, "bg_color": "#f2f2f2", "top": 1}
    )
    header_wrap_format.set_align("center")
    header_wrap_format.set_align("vcenter")
    header_centered_format = workbook.add_format({"bg_color": "#f2f2f2", "top": 1})
    header_centered_format.set_align("center")
    header_centered_format.set_align("vcenter")

    # num_format can change the apparence of positive, negative or null values
    # it works like this : positive;negative;zero;text
    # see https://support.office.com/article/number-format-codes-5026bbd6-04bc-48cd-bf33-80f18b4eae68

    number_format_top = workbook.add_format({"num_format": "0", "top": 1})
    number_format_top.set_align("center")
    number_format_top_null_dash = workbook.add_format(
        {"num_format": "0;0;-;-", "top": 1}
    )
    number_format_top_null_dash.set_align("center")
    number_format_top_null_dash = workbook.add_format(
        {"num_format": "0;0;-;-", "top": 1}
    )
    number_format_top_null_dash.set_align("center")
    number_format = workbook.add_format({"num_format": "0"})
    number_format.set_align("center")
    number_format_null_dash = workbook.add_format({"num_format": "0;0;-;-"})
    number_format_null_dash.set_align("center")
    percent_format_top = workbook.add_format({"num_format": "0%", "top": 1})
    percent_format_top.set_align("center")
    percent_format_top_null_dash = workbook.add_format(
        {"num_format": "0%;0%;-;@", "top": 1}
    )
    percent_format_top_null_dash.set_align("center")
    percent_format_top.set_align("center")
    percent_format = workbook.add_format({"num_format": "0%;0%;-;@"})
    percent_format.set_align("center")
    header_bold_center_format = workbook.add_format(
        {"bold": True, "bg_color": "#f2f2f2", "top": 1}
    )
    header_bold_center_format.set_align("vcenter")
    bold_center_format = workbook.add_format({"bold": True, "top": 1})
    bold_center_bordered_format = workbook.add_format({"bold": True, "border": 1})
    euro_format = workbook.add_format(
        {
            "num_format": '_-* #,##0.0" "[$€-C]_-;"-"* #,##0.0" "[$€-C]_-;_-* "-"??" "[$€-C]_-;_-@_-'
        }
    )
    euro_format_bordered = workbook.add_format(
        {
            "num_format": '_-* #,##0.0" "[$€-C]_-;"-"* #,##0.0" "[$€-C]_-;_-* "-"??" "[$€-C]_-;_-@_-',
            "border": 1,
        }
    )
    euro_italic_format = workbook.add_format(
        {
            "num_format": '_-* #,##0.0" "[$€-C]_-;"-"* #,##0.0" "[$€-C]_-;_-* "-"??" "[$€-C]_-;_-@_-',
            "top": 1,
            "italic": True,
        }
    )
    date_format = workbook.add_format({"num_format": "dd mmm yyyy"})
    date_format.set_align("center")
    date_format_border = workbook.add_format({"num_format": "mmm-yy", "border": 1})
    date_format_border.set_align("center")
    italic_right_format = workbook.add_format({"italic": True, "top": 1})
    italic_right_format.set_align("right")

    groups_name = "/".join(groups)

    # Create sheets
    if export_statistics:
        stats_sheet = workbook.add_worksheet("Statistiques")
        generate_statistics(
            stats_sheet,
            project_statistics,
            groups_name,
            bold_center_format,
            folder_name_format,
            header_bold_center_format,
            header_centered_format,
            header_wrap_format,
            left_bordered,
            number_format,
            number_format_null_dash,
            number_format_top,
            number_format_top_null_dash,
            percent_format,
            percent_format_top,
            percent_format_top_null_dash,
            table_title_format,
            title_cell_format,
            top_bordered,
        )
    if export_actions:
        actions_sheet = workbook.add_worksheet("Actions")
        generate_actions(
            actions_sheet,
            project_statistics,
            groups_name,
            title_cell_format,
            header_wrap_format,
            left_bordered,
            date_format,
            number_format,
        )
    if export_statistics and project_statistics["budget_tracking"]:
        budget_sheet = workbook.add_worksheet("Suivi budget")
        generate_budget(
            budget_sheet,
            project_statistics,
            groups_name,
            bold_center_format,
            bold_center_bordered_format,
            folder_name_format,
            header_bold_center_format,
            header_centered_format,
            header_wrap_format,
            left_bordered,
            number_format,
            percent_format,
            title_cell_format,
            top_bordered,
            euro_format,
            euro_format_bordered,
            euro_italic_format,
            date_format_border,
            italic_right_format,
        )
    for laureate_group, statistics in project_statistics_laureates:
        if export_statistics:
            stats_sheet = workbook.add_worksheet(f"Stats_{laureate_group}"[:31])
            generate_statistics(
                stats_sheet,
                statistics,
                laureate_group,
                bold_center_format,
                folder_name_format,
                header_bold_center_format,
                header_centered_format,
                header_wrap_format,
                left_bordered,
                number_format,
                number_format_null_dash,
                number_format_top,
                number_format_top_null_dash,
                percent_format,
                percent_format_top,
                percent_format_top_null_dash,
                table_title_format,
                title_cell_format,
                top_bordered,
            )
        if export_actions:
            actions_sheet = workbook.add_worksheet(f"Actions_{laureate_group}"[:31])
            generate_actions(
                actions_sheet,
                statistics,
                laureate_group,
                title_cell_format,
                header_wrap_format,
                left_bordered,
                date_format,
                number_format,
            )
        if export_statistics and statistics["budget_tracking"]:
            budget_sheet = workbook.add_worksheet(f"Budget_{laureate_group}"[:31])
            generate_budget(
                budget_sheet,
                statistics,
                laureate_group,
                bold_center_format,
                bold_center_bordered_format,
                folder_name_format,
                header_bold_center_format,
                header_centered_format,
                header_wrap_format,
                left_bordered,
                number_format,
                percent_format,
                title_cell_format,
                top_bordered,
                euro_format,
                euro_format_bordered,
                euro_italic_format,
                date_format_border,
                italic_right_format,
            )

    # return XLSX file
    workbook.close()
    xlsx_output.seek(0)

    return _make_filename(export_actions, export_statistics, groups), xlsx_output.read()


def _make_filename(export_actions, export_statistics, groups):
    export_name = ""
    if export_statistics:
        export_name += "_statistics"
    if export_actions:
        export_name += "_actions"
    if len(groups) == 1:
        groups_name = (
            "_".join(groups).replace(" ", "_").replace("/", "").replace("\\", "")
        )
    else:
        groups_name = ""

    if len(groups_name) > 30:
        groups_name = f"{groups_name[:27]}..."
    filename = (
        f"FAC_{groups_name}{export_name}_{date.today().strftime('%Y_%m_%d')}.xlsx"
    )
    return filename


def generate_actions(  # NOQA: CFQ001,CFQ002,C901
    actions_sheet,
    project_statistics,
    group,
    title_cell_format,
    header_wrap_format,
    left_bordered,
    date_format,
    number_format,
):
    is_actimmo = project_statistics["is_actimmo"]
    row = write_titles(
        group, project_statistics, actions_sheet, title_cell_format, "actions"
    )

    max_number_tags, row, tag_column, tag_row = _write_actions_header(
        actions_sheet,
        header_wrap_format,
        is_actimmo,
        row,
        project_statistics["custom_display_fields"],
    )

    organizations = project_statistics["organizations"]
    contacts = project_statistics["contacts"]

    for action in project_statistics["actions"]:
        if action["linked_object_type"] == "organization":
            organization = organizations.get(action["organization_pk"], {})
            tags = organization.get("tags", [])
            col = 0
            actions_sheet.write(row, col, action["group"])
            col += 1
            actions_sheet.write(row, col, organization.get("name", ""))
            col += 1
            actions_sheet.write(row, col, organization.get("type", ""))
            col += 1
            actions_sheet.write(row, col, organization.get("email", ""))
            col += 1
            actions_sheet.write(
                row, col, "Oui" if organization.get("accepts_newsletters") else "Non"
            )
            col += 1
            if is_actimmo:
                actions_sheet.write(
                    row,
                    col,
                    ", ".join(tag for tag in tags if tag[:4] in ACTIMMO_TAGS_PREFIXES),
                )
                col += 1
            actions_sheet.write(row, col, organization.get("address", ""))
            col += 1
            actions_sheet.write(row, col, organization.get("town", ""))
            col += 1
            actions_sheet.write(row, col, organization.get("zipcode", ""))
            col += 1
            actions_sheet.write_number(
                row, col, organization.get("nb_contacts", 0), number_format
            )
            col += 1
            actions_sheet.write(row, col, organization.get("referent", ""))
            col += 1
            actions_sheet.write(row, col, action["name"])
            col += 1
            actions_sheet.write(row, col, action["done_by"])
            col += 1
            if is_actimmo:
                actions_sheet.write(row, col, "À distance" if action["remote"] else "")
                col += 1
            actions_sheet.write_datetime(row, col, action["date"], date_format)
            col += 1

            if project_statistics["custom_display_fields"].get("duration"):
                duration = math.floor(60 * (action["duration"] or 0))
                if duration:
                    actions_sheet.write(row, col, duration, number_format)
                col += 1

            actions_sheet.write(row, col, action["contact"].get("name", ""))
            col += 1
            contact_pk = action["contact"].get("pk", -1)
            actions_sheet.write(
                row, col, organization.get("members", {}).get(contact_pk, "")
            )
            col += 1
            actions_sheet.write(row, col, action["document"])
            col += 1
            actions_sheet.write(row, col, action["message"])
            col += 1
            if is_actimmo:
                tags = [tag for tag in tags if tag[:4] not in ACTIMMO_TAGS_PREFIXES]

            # TODO (?) remove useless enumerate (see below also)
            max_number_tags = max(max_number_tags, len(tags))
            for tag_number, tag in enumerate(tags):
                actions_sheet.write(row, col + tag_number, tag)
        elif not is_actimmo and action["linked_object_type"] == "contact":
            col = 0

            # shorthand for normal write + increment col count
            def write(*args):
                nonlocal col
                actions_sheet.write(row, col, *args)
                col += 1

            contact = contacts.get(action["contact_pk"], {})
            write(action["group"])
            write(contact.get("name", ""))
            write(contact.get("type", ""))
            write(contact.get("email", ""))
            write("Oui" if contact.get("accepts_newsletters") else "Non")
            # The 'TAG Actimmo' column is skipped
            # --
            write(contact.get("address", ""))
            write(contact.get("town", ""))
            write(contact.get("zipcode", ""))
            # the number of contacts linked is not relevant
            actions_sheet.write_number(row, col, 0, number_format)
            col += 1
            write(contact.get("referent", ""))
            write(action["name"])
            write(action["done_by"])
            actions_sheet.write_datetime(row, col, action["date"], date_format)
            col += 1

            if project_statistics["custom_display_fields"].get("duration"):
                duration = math.floor(60 * (action["duration"] or 0))
                if duration:
                    actions_sheet.write(row, col, duration, number_format)
                col += 1

            write(action["contact"].get("name", ""))
            contact_pk = action["contact"].get("pk", -1)
            write(contact.get("members", {}).get(contact_pk, ""))
            write(action["document"])
            write(action["message"])
            tags = contact.get("tags", [])

            # TODO (?) remove useless enumerate, same as before
            max_number_tags = max(max_number_tags, len(tags))
            for tag_number, tag in enumerate(tags):
                actions_sheet.write(row, col + tag_number, tag)
        row += 1

    for tag_number in range(max_number_tags):
        actions_sheet.set_column(tag_column + tag_number, tag_column + tag_number, 10)
        actions_sheet.write(
            tag_row, tag_column + tag_number, f"Tag {tag_number+1 }", header_wrap_format
        )

    actions_sheet.write(tag_row, tag_column + max_number_tags, "", left_bordered)


def _write_actions_header(
    actions_sheet, header_wrap_format, is_actimmo, row, custom_display_fields
):
    actions_sheet.set_row(row, 60)
    col = 0
    actions_sheet.set_column(col, col, 20)
    actions_sheet.write(
        row,
        col,
        "Structure lauréate" if is_actimmo else "Structure utilisatrice",
        header_wrap_format,
    )
    col += 1
    actions_sheet.set_column(col, col, 15)
    if is_actimmo:
        column_name = "Nom de la structure"
    else:
        column_name = "Nom"
    actions_sheet.write(row, col, column_name, header_wrap_format)
    col += 1
    actions_sheet.set_column(col, col, 15)
    if is_actimmo:
        column_name = "Type de structure"
    else:
        column_name = "Type"
    actions_sheet.write(row, col, column_name, header_wrap_format)
    col += 1
    actions_sheet.write(row, col, "Email", header_wrap_format)
    col += 1
    actions_sheet.write(
        row, col, "Accepte de recevoir des newsletters", header_wrap_format
    )
    col += 1
    if is_actimmo:
        actions_sheet.set_column(col, col, 10)
        actions_sheet.write(row, col, "Tag actimmo", header_wrap_format)
        col += 1
    actions_sheet.set_column(col, col, 15)
    actions_sheet.write(row, col, "Adresse", header_wrap_format)
    col += 1
    actions_sheet.set_column(col, col, 10)
    actions_sheet.write(row, col, "Commune", header_wrap_format)
    col += 1
    actions_sheet.set_column(col, col, 6)
    actions_sheet.write(row, col, "Code postal", header_wrap_format)
    col += 1
    actions_sheet.set_column(col, col, 10)
    actions_sheet.write(
        row, col, "Nombre de contacts associés à la structure", header_wrap_format
    )
    col += 1
    actions_sheet.set_column(col, col, 15)
    if is_actimmo:
        column_name = "Compte associé structure lauréate"
    else:
        column_name = "Référent"
    actions_sheet.write(row, col, column_name, header_wrap_format)
    col += 1
    actions_sheet.set_column(col, col, 28)
    actions_sheet.write(row, col, "Action réalisée", header_wrap_format)
    col += 1

    actions_sheet.set_column(col, col, 20)
    actions_sheet.write(row, col, "Réalisée par", header_wrap_format)
    col += 1

    if is_actimmo:
        actions_sheet.set_column(col, col, 10)
        actions_sheet.write(row, col, "À distance ?", header_wrap_format)
        col += 1

    actions_sheet.set_column(col, col, 12)
    actions_sheet.write(row, col, "Date de réalisation", header_wrap_format)
    col += 1

    if custom_display_fields.get("duration"):
        actions_sheet.set_column(col, col, 12)
        actions_sheet.write(row, col, "Temps passé (minutes)", header_wrap_format)
        col += 1

    actions_sheet.set_column(col, col, 15)
    actions_sheet.write(row, col, "Contact concerné", header_wrap_format)
    col += 1
    actions_sheet.set_column(col, col, 15)
    actions_sheet.write(row, col, "Poste du contact concerné", header_wrap_format)
    col += 1
    actions_sheet.set_column(col, col, 15)
    actions_sheet.write(row, col, "Pièce jointe", header_wrap_format)
    col += 1
    actions_sheet.set_column(col, col, 20)
    actions_sheet.write(row, col, "Champ libre", header_wrap_format)
    col += 1
    tag_column = col
    tag_row = row
    max_number_tags = 0
    row += 1
    return max_number_tags, row, tag_column, tag_row


def generate_budget(  # NOQA: CFQ001,CFQ002
    budget_sheet,
    project_statistics,
    group,
    bold_center_format,
    bold_center_bordered_format,
    folder_name_format,
    header_bold_center_format,
    header_centered_format,
    header_wrap_format,
    left_bordered,
    number_format,
    percent_format,
    title_cell_format,
    top_bordered,
    euro_format,
    euro_format_bordered,
    euro_italic_format,
    date_format,
    italic_right_format,
):
    row = write_titles(
        group,
        project_statistics,
        budget_sheet,
        title_cell_format,
        "suivi budget actions",
    )

    budget = project_statistics["budget_tracking"]
    today = min(date.today(), budget["period_end"])

    budget_sheet.write(
        row,
        0,
        f"Estimation de la consommation du budget actions au {today.strftime('%d/%m/%Y')} :",
    )
    total_row = row
    row += 1
    subtotal_rows = []
    budget_sheet.write(row, 0, "Budget actions :")
    budget_sheet.write(row, 2, budget["total_envelope"], euro_format)
    row += 1
    budget_sheet.write(row, 0, "Consommation :")
    budget_sheet.write(
        row, 2, f"={_case(total_row, 2)}/{_case(row-1, 2)}", percent_format
    )

    # graph data
    row += 2
    budget_sheet.write(row, 0, "t", bold_center_bordered_format)
    row += 1
    budget_sheet.write(row, 0, "€", bold_center_bordered_format)
    for i, point in enumerate(budget["graph_data"]):
        col = i + 1
        budget_sheet.write_datetime(row - 1, col, point["date"], date_format)
        budget_sheet.write_number(
            row, col, point["cumulated_expenses"], euro_format_bordered
        )

    row += 2

    for folder_model in project_statistics["folder_models"].values():
        budget_sheet.set_row(row, 24)
        budget_sheet.write(row, 0, folder_model["name"], folder_name_format)
        row += 2

        start_row = row
        budget_sheet.set_row(start_row, 40)

        # list of rows corresponding to actions, used to generate the model subtotal formula
        action_rows = []

        # header
        budget_sheet.write(start_row, 0, "Action", header_bold_center_format)
        budget_sheet.write(start_row, 1, "Type de valorisation", header_wrap_format)
        budget_sheet.write(start_row, 2, "Nombre", header_centered_format)
        budget_sheet.write(start_row, 3, "Valorisation unitaire", header_wrap_format)
        budget_sheet.write(start_row, 4, "Total", header_wrap_format)
        budget_sheet.write(start_row, 5, "", left_bordered)

        # lines in table
        for category in folder_model["categories"]:
            row += 1
            budget_sheet.merge_range(
                row, 0, row, 4, category["name"], bold_center_format
            )
            budget_sheet.write(row, 5, "", left_bordered)

            for actions in category["actions"]:
                for i, type_valorization in enumerate(actions["type_valorizations"]):
                    row += 1
                    budget_sheet.write(row, 0, actions["name"])
                    budget_sheet.write(row, 1, type_valorization)
                    budget_sheet.write(row, 2, actions["quantity"][i], number_format)
                    budget_sheet.write(
                        row, 3, actions["unit_valorisation"][i], euro_format
                    )
                    budget_sheet.write(
                        row, 4, f"={_case(row, 2)}*{_case(row, 3)}", euro_format
                    )
                    budget_sheet.write(row, 5, "", left_bordered)
                    action_rows.append(row)

        row += 1
        for col in range(3):
            budget_sheet.write(row, col, "", top_bordered)

        subtotal_rows.append(row)
        budget_sheet.write(
            row, 3, f"Total {folder_model['name']} :", italic_right_format
        )
        budget_sheet.write(
            row,
            4,
            f"=SUM({'+'.join(_case(row, 4) for row in action_rows)})",
            euro_italic_format,
        )

        row += 2

    budget_sheet.write(
        total_row,
        2,
        f"=SUM({'+'.join(_case(subtotal_row, 4) for subtotal_row in subtotal_rows)})",
        euro_format,
    )


def generate_statistics(  # NOQA: CFQ002
    stats_sheet,
    project_statistics,
    group,
    bold_center_format,
    folder_name_format,
    header_bold_center_format,
    header_centered_format,
    header_wrap_format,
    left_bordered,
    number_format,
    number_format_null_dash,
    number_format_top,
    number_format_top_null_dash,
    percent_format,
    percent_format_top,
    percent_format_top_null_dash,
    table_title_format,
    title_cell_format,
    top_bordered,
):
    row = write_titles(
        group, project_statistics, stats_sheet, title_cell_format, "statistiques"
    )

    for folder_model in project_statistics["folder_models"].values():
        stats_sheet.set_row(row, 24)
        stats_sheet.write(row, 0, folder_model["name"], folder_name_format)
        row += 2

        row = statuses_table(
            row,
            stats_sheet,
            folder_model,
            header_bold_center_format,
            header_centered_format,
            header_wrap_format,
            left_bordered,
            number_format_top,
            number_format_top_null_dash,
            percent_format_top,
            percent_format_top_null_dash,
            table_title_format,
            top_bordered,
        )

        row = actions_table(
            row,
            stats_sheet,
            folder_model,
            bold_center_format,
            header_bold_center_format,
            header_centered_format,
            header_wrap_format,
            left_bordered,
            number_format,
            number_format_null_dash,
            percent_format,
            table_title_format,
            top_bordered,
        )


def write_titles(group, project_statistics, sheet, title_cell_format, sheet_name):
    # Widen the 2 first lines to make the text clearer.
    sheet.set_row(0, 30)
    sheet.set_row(1, 30)
    sheet.set_row(2, 30)
    # Widen the columns
    sheet.set_column(0, 0, 22)
    sheet.set_column(1, 20, 13)
    # Titles
    row = 0
    sheet.write(row, 0, f"{group}", title_cell_format)
    row += 1
    sheet.write(
        row, 0, f"{project_statistics['name']} : {sheet_name}", title_cell_format
    )
    row += 1
    if project_statistics["date_start"] and project_statistics["date_end"]:
        sheet.write(row, 0, "Du", title_cell_format)
        sheet.write(row, 1, f"{project_statistics['date_start']}", title_cell_format)
        sheet.write(row, 3, "au", title_cell_format)
        sheet.write(row, 4, f"{project_statistics['date_end']}", title_cell_format)
    row += 1
    sheet.write(row, 0, "Exporté le")
    sheet.write(row, 1, date.today().strftime("%d/%m/%Y"))
    row += 2
    return row


def actions_table(  # NOQA: CFQ002
    row,
    stats_sheet,
    folder_model,
    bold_center_format,
    header_bold_center_format,
    header_centered_format,
    header_wrap_format,
    left_bordered,
    number_format,
    number_format_null_dash,
    percent_format,
    table_title_format,
    top_bordered,
):
    stats_sheet.set_row(row, 18)
    stats_sheet.write(row, 0, "Actions réalisées", table_title_format)
    row += 1
    start_row = row
    stats_sheet.set_row(start_row, 40)
    if folder_model["has_action_objectives"]:
        last_col = 4
    else:
        last_col = 2
    # header
    stats_sheet.write(start_row, 0, "Action", header_bold_center_format)
    stats_sheet.write(start_row, 1, "Total", header_centered_format)
    if folder_model["has_action_objectives"]:
        stats_sheet.write(start_row, 2, "Objectifs", header_wrap_format)
        stats_sheet.write(start_row, 3, "Avancement", header_centered_format)
    stats_sheet.write(start_row, last_col, "", left_bordered)
    # lines in table
    for category in folder_model["categories"]:
        row += 1
        stats_sheet.merge_range(
            row, 0, row, last_col - 1, category["name"], bold_center_format
        )
        stats_sheet.write(row, last_col, "", left_bordered)

        for actions in category["actions"]:
            row += 1
            stats_sheet.write(row, 0, actions["name"])
            stats_sheet.write(row, 1, actions["total"], number_format)
            if folder_model["has_action_objectives"]:
                stats_sheet.write(row, 2, actions["objective"], number_format_null_dash)
                stats_sheet.write(
                    row,
                    3,
                    _if_divide_zero(f"={_case(row, 1)} / {_case(row, 2)}"),
                    percent_format,
                )
            stats_sheet.write(row, last_col, "", left_bordered)
    row += 1
    for col in range(last_col):
        stats_sheet.write(row, col, "", top_bordered)
    row += 1
    return row


def statuses_table(  # NOQA: CFQ002
    row,
    stats_sheet,
    folder_model,
    header_bold_center_format,
    header_centered_format,
    header_wrap_format,
    left_bordered,
    number_format_top,
    number_format_top_null_dash,
    percent_format_top,
    percent_format_top_null_dash,
    table_title_format,
    top_bordered,
):
    stats_sheet.set_row(row, 18)
    stats_sheet.write(row, 0, "Statuts", table_title_format)
    row += 1
    start_row = row
    stats_sheet.set_row(start_row, 40)
    if folder_model["has_status_objectives"]:
        last_col = 6
    else:
        last_col = 4
    # header
    stats_sheet.write(start_row, 0, "Statut", header_bold_center_format)
    stats_sheet.write(
        start_row, 1, "Ont ce statut (sur la période)", header_wrap_format
    )
    stats_sheet.write(start_row, 2, "% du nb total", header_centered_format)
    stats_sheet.write(start_row, 3, "Cumul", header_centered_format)
    if folder_model["has_status_objectives"]:
        stats_sheet.write(start_row, 4, "Objectifs", header_wrap_format)
        stats_sheet.write(start_row, 5, "Avancement", header_centered_format)
    stats_sheet.write(start_row, last_col, "", left_bordered)
    # lines in table
    for status in folder_model["statuses"]:
        row += 1
        stats_sheet.write(row, 0, status["name"], top_bordered)
        stats_sheet.write(row, 1, status["nb_status"], number_format_top)
        stats_sheet.write(
            row,
            2,
            _if_divide_zero(f"={_case(row, 1)} / {_case(start_row + 1, 3)}"),
            percent_format_top,
        )
        stats_sheet.write(
            row, 3, f"={_case(row, 1)} + {_case(row + 1, 3)}", number_format_top
        )
        if folder_model["has_status_objectives"]:
            stats_sheet.write(
                row, 4, status["objective"] or 0, number_format_top_null_dash
            )
            stats_sheet.write(
                row,
                5,
                _if_divide_zero(f"={_case(row, 3)} / {_case(row, 4)}"),
                percent_format_top_null_dash,
            )
        stats_sheet.write(row, last_col, "", left_bordered)
    row += 1
    for col in range(last_col):
        stats_sheet.write(row, col, "", top_bordered)
    row += 1
    return row
