Waybar weather plugin
=====================

This plugin uses the [One Call API from OpenWeatherMap.org](https://openweathermap.org/api/one-call-api).

## set your APIKEY and geo location in your shell

In your ~/.bashrc add the following definition and place your APIKEY in there

    # waybar weather settings:
    export WAYBAR_WEATHER_APIKEY="<YOUR OpenWeatherMap API KEY>"
    export WAYBAR_WEATHER_LAT="44.43"
    export WAYBAR_WEATHER_LON="26.02"
    export WAYBAR_WEATHER_UNITS="metric"
    export WAYBAR_WEATHER_EXCLUDE="minutely,hourly,daily"