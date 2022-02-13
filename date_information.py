from datetime import date, timedelta
import requests
import jsonpickle
from dotenv import load_dotenv
from os import getenv


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

    def toJSON(self):
        return jsonpickle.encode(self)

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
                year = self.output_year_without_ad(event["year"])
                if year == str(self.date.year):
                    events.append(event)
                # because the user can't enter BC dates, I don't want them displayed in the other_years_events list.
                elif "BC" in (year[-2:], year[:2]):
                    continue
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
                year = self.output_year_without_ad(birth["year"])
                # I am taking into account if the API adds "AD" to the beginning or end of the year.
                if year == str(self.date.year):
                    births.append(birth)
                # Because the user can't enter BC dates, I don't want them displayed in the birthdays list.
                elif "BC" in (year[-2:], year[:2]):
                    continue
                # I only want to populate this with people born before the input date so that I can have a "birthdays" section
                # Since I've already dealt with BC dates, I don't need to consider them here.
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
                year = self.output_year_without_ad(death["year"])
                if year == str(self.date.year):
                    deaths.append(death)
                # Because the user can't enter BC dates, I don't want them displayed in the birthdays list.
                elif "BC" in (death["year"][-2:], death["year"][:2]):
                    continue
            if deaths:
                self.date_data["deaths"] = deaths
            else:
                self.date_data["deaths"] = None
            pass

    def output_year_without_ad(self, year):
        if year[-3:] == " AD":
            output_year = year[:-3]
        elif year[:3] == "AD ":
            output_year = year[3:]
        else:
            output_year = year
        return output_year

        # self.date_data["events"] = dictData

    # def wiki_births(self)

    # print(data)


# test_date = date(year=2021, month=2, day=29)
# date_information = DateInformation(test_date)
# pass
