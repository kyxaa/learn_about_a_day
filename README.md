# Learn About A Day

Learn About A Day takes a date and returns information about that day including major events, births, deaths, &amp; birthdays. It is using the [on-this-day API](https://byabbe.se/on-this-day/#/) for the fetching of the data.


## Tools Used

- Python 3.8.10
- Flask (Python Web Framework)
- Bootstrap (CSS Framework)
- VS Code (Code Editor)
- WSL2 (Linux Subsystem for Windows)
- Heroku (Hosting Service)
- See requirements.txt for the other Python libraries used.

## Usage

If you want to check out the app, you can visit it here:

[https://learn-about-a-day.herokuapp.com/](https://learn-about-a-day.herokuapp.com/)

If you want to run this locally, you will need to make sure you have a .env file in the directory with a Secret Key defined as `FLASK_APP_SECRET_KEY`. You can have pip install the needed libraries from the requirements.txt file.

## Known Issues

- An Internal Server error can occur when using the back button from the output and trying to submit again. Refreshing the page should resolve the issue. This has to do with the caching and will be resolved in a future version.

## Future Plans

- While on-this-day API has a lot of data, I would like to see how I could expand out my sources to ensure that each time a date is input that each section of the output page has data.
- Currently the form doesn't allow data before 1 AD, which works out as I didn't want to handle dates before then with this first iteration. I would like to implement the ability to ask about data before 1 AD in the future.
- Adding more color and more visual elements

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
