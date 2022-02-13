from datetime import date, timedelta
import requests
import json
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

    # These wiki functions grabs the historical information tied to the day and month.
    # Because it is pulling back way more information than what is specific to
    # the day/month/year, I'm going to use the extra data to include a "things
    # that happened on other years on this day" section to the app.

    # TODO: Remove the redundancy in wiki_events and wiki_births by creating a function that handles the seperation of current years and other years

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
                # I am taking into account if the API adds "AD" to the beginning or end of the year.
                if event["year"] in (
                    str(self.date.year),
                    f"{str(self.date.year)} AD",
                    f"AD {str(self.date.year)}",
                ):
                    events.append(event)
                # because the user can't enter BC dates, I don't want them displayed in the other_years_events list.
                elif "BC" in (event["year"][-2:], event["year"][2:]):
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
                # I am taking into account if the API adds "AD" to the beginning or end of the year.
                if birth["year"] in (
                    str(self.date.year),
                    f"{str(self.date.year)} AD",
                    f"AD {str(self.date.year)}",
                ):
                    births.append(birth)
                # Because the user can't enter BC dates, I don't want them displayed in the birthdays list.
                elif "BC" in (birth["year"][-2:], birth["year"][2:]):
                    continue
                # I only want to populate this with people born before the input date so that I can have a "birthdays" section
                # Since I've already dealt with BC dates, I don't need to consider them here.
                elif int(birth["year"]) < self.date.year:
                    birthdays.append(birth)
            if births:
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
                # I am taking into account if the API adds "AD" to the beginning or end of the year.
                if death["year"] in (
                    str(self.date.year),
                    f"{str(self.date.year)} AD",
                    f"AD {str(self.date.year)}",
                ):
                    deaths.append(death)
                # Because the user can't enter BC dates, I don't want them displayed in the birthdays list.
                elif "BC" in (death["year"][-2:], death["year"][2:]):
                    continue
            if deaths:
                self.date_data["deaths"] = deaths
            else:
                self.date_data["deaths"] = None
            pass

        # self.date_data["events"] = dictData

    # def wiki_births(self)

    # print(data)


test_date = date(year=1908, month=1, day=15)
date_information = DateInformation(test_date)
pass
