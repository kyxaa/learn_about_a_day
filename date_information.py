from datetime import date, timedelta
import requests
from time import sleep


class DateInformation:
    def __init__(self, date: date):
        # TODO: Include support for BC dates using
        self.date = date
        self.date_data = {
            "events": [],
            "other_years_events": [],
            "births": [],
            "birthdays": [],
            "deaths": [],
        }
        self.wiki_events()
        self.wiki_births()
        self.wiki_deaths()

    # These wiki functions grabs the historical information tied to the day and month.
    # Because it is pulling back way more information than what is specific to
    # the day/month/year, I'm going to use the extra data to include a "things
    # that happened on other years on this day" section to the app.

    # TODO: Remove the redundancy between the wiki functions

    def wiki_events(self):
        r = requests.get(
            f"https://byabbe.se/on-this-day/{self.date.month}/{self.date.day}/events.json"
        )
        if not r.ok:
            # raise Exception("ERROR: Count not fetch results")
            self.date_data["events"] = None
            self.date_data["other_years_events"] = None
            # TODO: put some sort of error flag here
        else:
            data = r.json()
            events = []
            other_years_events = []

            for event in data["events"]:
                if event["year"]:
                    year = event["year"]
                    if self.is_edgecase_year(year):
                        continue
                    elif year == str(self.date.year):
                        events.append(event)
                    else:
                        other_years_events.append(event)
            if events:
                self.date_data["events"] = events
            else:
                self.date_data["events"] = None
            if other_years_events:
                self.date_data["other_years_events"] = other_years_events
            else:
                self.date_data["other_years_events"] = None

    def wiki_births(self):
        r = requests.get(
            f"https://byabbe.se/on-this-day/{self.date.month}/{self.date.day}/births.json"
        )
        if not r.ok:
            # raise Exception("ERROR: Count not fetch results")
            self.date_data["births"] = None
            self.date_data["birthdays"] = None
            # TODO: put some sort of error flag here
        else:
            data = r.json()
            births = []
            birthdays = []
            for birth in data["births"]:
                if birth["year"]:
                    year = birth["year"]
                    if self.is_edgecase_year(year):
                        continue
                    elif year == str(self.date.year):
                        births.append(birth)
                    # I only want to populate this with people born before the input date so that I can have
                    # a "birthdays" section
                    elif int(year) < self.date.year:
                        birthdays.append(birth)
            if len(births) > 0:
                self.date_data["births"] = births
            else:
                self.date_data["births"] = None
            if birthdays:
                self.date_data["birthdays"] = birthdays
            else:
                self.date_data["birthdays"] = None

    def wiki_deaths(self):
        r = requests.get(
            f"https://byabbe.se/on-this-day/{self.date.month}/{self.date.day}/deaths.json"
        )
        if not r.ok:
            # raise Exception("ERROR: Count not fetch results")
            self.date_data["deaths"] = None
            # TODO: put some sort of error flag here
        else:
            data = r.json()
            deaths = []
            for death in data["deaths"]:
                if death["year"]:
                    year = death["year"]
                    if self.is_edgecase_year(year):
                        continue
                    elif year == str(self.date.year):
                        deaths.append(death)
            if deaths:
                self.date_data["deaths"] = deaths
            else:
                self.date_data["deaths"] = None

    # There are some responses that return a year value that isn't only a number(AD 63, 53 BC, 60 BCE, etc.).
    # I'm choosing not to deal with any entry that is an example of this as it isn't worth the time to write
    # up the logic for each edge case.
    def is_edgecase_year(self, year):
        try:
            int(year)
            return False
        except:
            return True


# Testing logic each date within a range to ensure that this part of the app breaks.
# start_date = date(1960, 1, 1)
# end_date = date(1960, 12, 31)
# delta = timedelta(days=1)

# while start_date <= end_date:
#     print(start_date)
#     date_information = DateInformation(start_date)

#     start_date += delta
#     sleep(0.25)
