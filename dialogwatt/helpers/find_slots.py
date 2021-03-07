# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from django.db.models import Prefetch, Q

import pytz

from accounts.models import Group, User

from dialogwatt.models import Appointment, Place
from dialogwatt.models import Slot


# Limit slot query size
HARD_SLOT_LIMIT = 1000


class FindSlots:
    def __init__(  # NOQA: CFQ002
        self,
        start_date,
        reason,
        inseecode=None,
        place=None,
        advisor_visibility=True,
    ) -> None:
        self.inseecode = inseecode
        self.start_date = start_date
        self.reason = reason
        self.place = place
        self.advisor_visibility = advisor_visibility

    def find_slots_without_appointment(
        self, duration: int, filter_advisors: list = None
    ) -> dict:
        """
        Return timetable of available slots without appointment
        """
        timetable = {}
        slots = self._available_slots().filter(visibility="without_reservation")

        if filter_advisors:
            slots = slots.filter(advisors__in=filter_advisors)

        tz_europe = pytz.timezone("Europe/Paris")

        for slot in slots[:HARD_SLOT_LIMIT]:
            date = slot.start_date.astimezone(tz_europe).date()
            data = {
                "start": slot.start_date.astimezone(tz_europe).time().strftime("%H:%M"),
                "end": slot.end_date.astimezone(tz_europe).time().strftime("%H:%M"),
                "group": slot.group.pk,
                "advisors": None,
                "place": slot.place.pk,
                "slot": slot.pk,
            }
            if slot.use_advisor_calendar:
                data["advisors"] = [x.pk for x in slot.advisors.all()]

            try:
                timetable[date].append(data)
            except KeyError:
                timetable[date] = [data]

        return timetable

    def find_free_time(self, duration: int, filter_advisors: list = None) -> dict:
        timetable = {}
        slots = self._available_slots().exclude(visibility="without_reservation")

        for slot in slots[:HARD_SLOT_LIMIT]:
            for time in self._free_time_in_slot(slot, duration, filter_advisors):
                data = {
                    "time": time,
                    "group": slot.group.pk,
                    "advisors": None,
                    "place": slot.place.pk,
                    "slot": slot.pk,
                }
                if slot.use_advisor_calendar:
                    data["advisors"] = [x.pk for x in slot.advisors.all()]

                try:
                    timetable[slot.start_date.date()].append(data)
                except KeyError:
                    timetable[slot.start_date.date()] = [data]

        return timetable

    def _available_slots(self):
        """
        Return a queryset of all active slots
        """
        slots = (
            Slot.selectable if self.advisor_visibility else Slot.selectable_for_public
        )

        slots = (
            slots.filter(
                reasons__in=[self.reason],
                start_date__date__gte=self.start_date.date(),
            )
            .order_by("start_date")
            .prefetch_related(
                Prefetch("place", queryset=Place.objects.only("pk").all())
            )
            .prefetch_related(
                Prefetch("advisors", queryset=User.advisors.only("pk").all())
            )
            .prefetch_related(
                Prefetch("group", queryset=Group.objects.only("pk").all())
            )
        )

        if self.place:
            slots = slots.filter(place=self.place)

        if self.inseecode:
            slots = slots.filter(catchment_area__territories__inseecode=self.inseecode)

        slots = slots.filter(
            pk__in=[
                slot.pk
                for slot in slots
                if slot.start_date.date()
                >= (self.start_date + relativedelta(hours=slot.deadline)).date()
            ]
        )

        return slots

    def _smallest_duration_for_slot(self, slot) -> int:
        """
        Return the smallest duration of the reasons for this slot
        """
        return min(x.duration for x in slot.reasons.all())

    def _all_chunks_for_slot_with_duration(
        self, start_time, end_time, duration
    ) -> list:
        """
        Return list of all existing timeslot
        ["09:00", "09:15", "09:30", "09:45"]

        start_time - datetime
        end_time - datetime
        duration - integer in minutes
        """
        current_date = start_time.astimezone(pytz.timezone("Europe/Paris"))
        chunks = []
        while current_date < end_time.astimezone(pytz.timezone("Europe/Paris")):
            start_time = (
                f"{current_date.time().hour:02}:{current_date.time().minute:02}"
            )
            chunks.append(start_time)
            current_date = current_date + relativedelta(minutes=duration)

        return chunks

    def _time_to_minutes(self, time) -> int:
        """
        convert Datetime.time to minutes
        """
        return time.hour * 60 + time.minute

    def _minutes_to_time(self, minutes: int) -> str:
        """
        convert minutes to time string "HH:MM"
        """
        return f"{int(minutes / 60):02}:{minutes % 60:02}"

    def _minutes_between(self, start: int, stop: int) -> list:
        """
        return a list of minutes between start and stop
        """
        return range(start, stop)

    def _get_advisors_for_slot(self, slot, filter_advisors: list = None) -> list:
        """
        return list of advisors assigned to the slot OR a list of integer if not
        slot.use_advisor_calendar in order to simulate advisors
        """
        if slot.use_advisor_calendar:
            if not filter_advisors:
                advisors = list(slot.advisors.all())
            else:
                advisors = list(
                    slot.advisors.filter(pk__in=[a.pk for a in filter_advisors])
                )
        else:
            advisors = range(slot.number_of_active_advisors)

        return advisors

    def _free_time_in_slot(  # NOQA: C901
        self, slot, duration: int, filter_advisors: list = None
    ) -> list:
        time_between_appointments = slot.time_between_slots
        slot_date = slot.start_date.date()
        timetable = []

        tz_europe = pytz.timezone("Europe/Paris")

        slot_start_minutes = self._time_to_minutes(
            slot.start_date.astimezone(tz_europe).time()
        )
        slot_end_minutes = self._time_to_minutes(
            slot.end_date.astimezone(tz_europe).time()
        )

        advisors = self._get_advisors_for_slot(slot, filter_advisors)

        minutes_in_slot = self._minutes_between(slot_start_minutes, slot_end_minutes)
        advisors_available_by_minutes_in_slot = {}

        for minute in minutes_in_slot:
            advisors_available_by_minutes_in_slot[minute] = list(advisors)

        # for each Appointment, remove time from advisors_available_by_minutes_in_slot
        for appointment in Appointment.active.filter(start_date__date=slot_date).filter(
            Q(slot__use_advisor_calendar=True, advisor__in=slot.advisors.all())
            | Q(slot=slot)
        ):
            appointment_start = appointment.start_date.astimezone(tz_europe).time()
            appointment_end = appointment.end_date.astimezone(tz_europe).time()

            appointment_start_minute = (
                self._time_to_minutes(appointment_start) - time_between_appointments
            )
            appointment_end_minute = (
                self._time_to_minutes(appointment_end) + time_between_appointments
            )

            for app_min in self._minutes_between(
                appointment_start_minute, appointment_end_minute
            ):
                if app_min in advisors_available_by_minutes_in_slot:
                    if slot.use_advisor_calendar:
                        try:
                            advisors_available_by_minutes_in_slot[app_min].pop(
                                advisors_available_by_minutes_in_slot[app_min].index(
                                    appointment.advisor
                                )
                            )
                        except ValueError:
                            pass
                    else:
                        if len(advisors_available_by_minutes_in_slot[app_min]) > 0:
                            advisors_available_by_minutes_in_slot[app_min].pop(0)

        # Given availibility of advisors, get time propositions
        ctime = slot_start_minutes
        available_minutes_set = {
            x
            for x in advisors_available_by_minutes_in_slot
            if len(advisors_available_by_minutes_in_slot[x]) > 0
        }
        while ctime + duration <= slot_end_minutes:
            chunk = self._minutes_between(ctime, ctime + duration)
            if set(chunk) <= available_minutes_set:
                timetable.append(self._minutes_to_time(ctime))
                ctime += duration + time_between_appointments
            else:
                ctime += 1

        return timetable
