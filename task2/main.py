from datetime import datetime, timedelta
import argparse
from enum import Enum


# types of events, other is a fake event to finding the soonest date now
class EventType(Enum):
    begin = 1
    end = 2
    other = 3


format_data = "%Y-%m-%d %H:%M:%S"


class Event:
    def __init__(self, type, time):
        self.type = type
        self.time = time


class Period:
    def __init__(self, begin, end, people):
        self.begin = begin
        self.end = end
        self.people = people

    @property
    def duration(self):
        return self.end - self.begin


# function reading data from txt
def read_lines(calendars):
    for j in calendars:
        with open(j) as f:
            lines = f.read().splitlines()
    return lines


# function casting read strings from txt into datetime and adding them to Event objects
def read_events(lines):
    global format_data
    events = []
    for i in lines:
        if len(i) == 10:
            day = timedelta(days=1)
            begin = datetime.strptime(i + ' 00:00:00', format_data)
            end = datetime.strptime(i + ' 00:00:00', format_data) + day
        else:
            begin = datetime.strptime(i[0: 19], format_data)
            end = datetime.strptime(i[22:41], format_data)
        events.append(Event(EventType.begin, begin))
        events.append(Event(EventType.end, end))

    return events


# main function to finding date, checks if found available date is in future
def find_available_date(now, duration_in_minutes, minimum_people, person_count, lines):
    events = read_events(lines, now)

    delta = timedelta(minutes=int(duration_in_minutes))

    events.append(Event(EventType.other, now - delta))
    events.append(Event(EventType.other, now + delta))
    events.sort(key=lambda x: x.time)

    availability = get_availability(events, person_count, delta)

    merge_periods(availability, minimum_people)

    for a in availability:
        dur = a.duration
        if a.begin <= now <= a.end and a.people >= int(minimum_people) and a.end - now > delta:
            return now
        elif dur >= delta and a.people >= int(minimum_people) and a.begin >= now:
            return a.begin


# function to change events into periods and assign amount of available people during this period
def get_availability(events, person_count, delta):
    availability = []
    for e in range(0, len(events)):
        if events[e].type == EventType.end:
            person_count += 1
        elif events[e].type == EventType.begin:
            person_count -= 1

        # creates one last period after last event
        if e == len(events) - 1:
            end_period = events[e].time + delta
        else:
            end_period = events[e + 1].time

        start_period = events[e].time
        availability.append(Period(start_period, end_period, person_count))
    return availability


# function to merge periods where amount of available people are the same
def merge_periods(availability, minimum_people):
    for i in range(0, len(availability) - 1):
        if i + 1 > len(availability) - 1:
            break
        while availability[i].people >= int(minimum_people) and availability[i + 1].people >= int(
                minimum_people):
            availability[i].end = availability[i + 1].end
            availability[i].people = min(availability[i].people, availability[i + 1].people)
            del availability[i + 1]
            if i + 1 > len(availability) - 1:
                break


# adding arguments parser, setting current datetime
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--calendars', nargs='+', help="txt files with terms of being busy")
    parser.add_argument('--duration-in-minutes', nargs=1, help="duration of appointment in minutes")
    parser.add_argument('--minimum-people', nargs=1, help="minimum people needed during an appointment")
    args = parser.parse_args()

    now = datetime.now()
    today = now.strftime(format_data)
    today = datetime.strptime(today, format_data)

    events = read_lines(args.calendars)
    person_count = len(args.calendars)
    date = find_available_date(today, args.duration_in_minutes, args.minimum_people, person_count, events)

    print("found a term:")
    print(date)
