import unittest
import main
from datetime import datetime as dt

now = dt(2022, 5, 12, 12, 0, 0)


class TestFindAvailableDate(unittest.TestCase):
    def tests_date_with_begin_and_end(self):
        lines = ['2022-05-12 00:00:00 - 2022-05-12 15:00:00']

        result = main.find_available_date(now=now, duration_in_minutes=30, minimum_people=2, person_count=2, lines=lines)

        self.assertEqual(dt(2022, 5, 12, 15, 0, 0), result)

    def tests_one_begin_date(self):
        lines = ['2022-05-12']

        result = main.find_available_date(now, 30, 2, 2, lines)

        self.assertEqual(dt(2022, 5, 13, 0, 0, 0), result)

    def tests_two_dates_with_the_same_beginning(self):

        lines = ['2022-05-12 00:00:00 - 2022-05-12 12:00:00',
                 '2022-05-12 00:00:00 - 2022-05-12 14:00:00']

        result = main.find_available_date(now, 30, 2, 2, lines)

        self.assertEqual(dt(2022, 5, 12, 14, 0, 0), result)

    def tests_if_appointment_can_be_in_too_short_period(self):
        lines = ['2022-05-12 00:00:00 - 2022-05-12 12:00:00',
                 '2022-05-12 12:15:00 - 2022-05-12 14:00:00']

        result = main.find_available_date(now, 30, 2, 2, lines)

        self.assertEqual(dt(2022, 5, 12, 14, 0, 0), result)

    def tests_being_busy_for_a_period_longer_than_a_day(self):
        lines = ['2022-05-12 00:00:00 - 2022-07-13 12:00:00',
                 '2022-05-12 12:15:00 - 2022-05-12 14:00:00']

        result = main.find_available_date(now, 30, 2, 2, lines)

        self.assertEqual(dt(2022, 7, 13, 12, 0, 0), result)

    def tests_if_date_is_in_future(self):
        lines = ['2022-05-11 00:00:00 - 2022-05-11 12:00:00',
                 '2022-05-11 13:00:00 - 2022-05-11 14:00:00']

        result = main.find_available_date(now, 30, 2, 2, lines)

        self.assertEqual(dt(2022, 5, 12, 12, 0, 0), result)

    def tests_availability_for_time_longer_than_a_day(self):
        lines = ['2022-05-12',
                 '2022-05-15']

        result = main.find_available_date(now, 1500, 2, 2, lines)

        self.assertEqual(dt(2022, 5, 13, 0, 0, 0), result)

    def tests_term_for_less_people_than_maximum(self):
        lines = ['2022-05-12']

        result = main.find_available_date(now, 1500, 1, 2, lines)

        self.assertEqual(dt(2022, 5, 12, 12, 0, 0), result)

