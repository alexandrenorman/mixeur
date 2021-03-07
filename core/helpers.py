# -*- coding: utf-8 -*-

import datetime
import locale
import unicodedata

from django.utils.translation import ugettext_lazy as _

import environ

import pytz


def restart_background_task(name, endpoint, repeat=5):
    """
    Delete an existing task from background_task.Task and run again

    :name: name of the task
    :endpoint: function to call
    :repeat: repeat delay in minutes
    """
    import logging

    logger = logging.getLogger(__name__)  # NOQA

    delete_background_task(name)

    logger.warning(f"Add task {name} on {repeat} minutes repeat delay")
    endpoint(repeat=60 * repeat)


def delete_background_task(name):
    """
    Delete an existing task from background_task.Task

    :name: name of the task
    :endpoint: function to call
    :repeat: repeat delay in minutes
    """
    from background_task.models import Task
    import logging

    logger = logging.getLogger(__name__)  # NOQA

    if Task.objects.filter(task_name=name).exists():
        logger.warning(f"{name} exists -> delete")
        Task.objects.filter(task_name=name).delete()


def is_jenkins_build():
    """
    Return True if running in jenkins build

    Test if DATABASE_URL == "None"
    """
    env = environ.Env()
    if env.str("DATABASE_URL", default="None") == "None":
        return True

    return False


def remove_diacritics(value):
    """
    Return string without diacritics (Épice => Epice)
    """
    return "".join(
        (
            c
            for c in unicodedata.normalize("NFD", value)
            if unicodedata.category(c) != "Mn"
        )
    )


def format_datetime_interval(dt1, dt2, include_time=True):  # NOQA: C901
    def get_time_format(dt):
        return dt.strftime("%H:%M")

    # TODO get timezone from config
    paris_tz = pytz.timezone("Europe/Paris")

    dt1 = dt1.astimezone(paris_tz)
    dt2 = dt2.astimezone(paris_tz)

    same_year = dt1.year == dt2.year
    same_month = dt1.month == dt2.month
    same_day = dt1.day == dt2.day
    current_year = dt1.year == datetime.date.today().year and same_year

    if include_time and (
        not isinstance(dt1, datetime.datetime) or not isinstance(dt2, datetime.datetime)
    ):
        include_time = False

    # Force locale - REWORK NEEDED
    locale.setlocale(locale.LC_ALL, "fr_FR.utf8")

    if same_year and same_month and same_day:
        if current_year:
            formatted = datetime.datetime.strftime(dt1, "%d %B")
        else:
            formatted = datetime.datetime.strftime(dt1, "%d %B %Y")
        if include_time:
            if dt1.hour == dt2.hour and dt1.minute == dt2.minute:
                return f"{formatted}, {get_time_format(dt1)}"
            else:
                return f"{formatted}, {get_time_format(dt1)} - {get_time_format(dt2)}"
        else:
            return _(f"le {formatted}")

    elif same_year and same_month and not include_time:
        if current_year:
            return (
                "du "
                + dt1.strftime("%d")
                + datetime.datetime.strftime(dt2, " au %d %B")
            )
        else:
            return (
                "du "
                + dt1.strftime("%d")
                + datetime.datetime.strftime(dt2, " au %d %B %Y")
            )

    elif same_year and not include_time:
        if current_year:
            return (
                "du "
                + datetime.datetime.strftime(dt1, "%d %B")
                + datetime.datetime.strftime(dt2, " au %d %B")
            )
        else:
            return (
                "du "
                + datetime.datetime.strftime(dt1, "%d %B")
                + datetime.datetime.strftime(dt2, " au %d %B %Y")
            )

    else:
        if include_time:
            if current_year:
                return f"du {datetime.datetime.strftime(dt1, '%d %B')}, {get_time_format(dt1)} au {datetime.datetime.strftime(dt2, '%d %B')}, {get_time_format(dt2)}"  # NOQA: E501
            else:
                return f"du {datetime.datetime.strftime(dt1, '%d %B %Y')}, {get_time_format(dt1)} au {datetime.datetime.strftime(dt2, '%d %B %Y')}, {get_time_format(dt2)}"  # NOQA: E501
        else:
            if current_year:
                return (
                    "du "
                    + datetime.datetime.strftime(dt1, "%d %B %Y")
                    + datetime.datetime.strftime(dt2, " au %d %B")
                )
            else:
                return (
                    "du "
                    + datetime.datetime.strftime(dt1, "%d %B %Y")
                    + datetime.datetime.strftime(dt2, " au %d %B %Y")
                )
