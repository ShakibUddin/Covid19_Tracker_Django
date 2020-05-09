from django.shortcuts import render
from django.http import HttpResponseRedirect
import requests
import json
import locale
import datetime

# Create your views here.

def index(request):
    country="Bangladesh"
    #todays datetime
    date= datetime.datetime.now().strftime("%A,%B %d,%Y")
    #world data
    url = "https://covid-19-data.p.rapidapi.com/totals"

    querystring = {"format": "json"}

    headers = {
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
        'x-rapidapi-key': "7be87834c4msh50d6f6176b86285p18e58ajsnef3f9a5da09a"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    world_wide_data = json.loads(response.text)
    locale.setlocale(locale.LC_ALL, '')

    #country total data
    url = "https://covid-19-data.p.rapidapi.com/country"

    querystring = {"format": "json", "name": country}

    headers = {
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
        'x-rapidapi-key': "7be87834c4msh50d6f6176b86285p18e58ajsnef3f9a5da09a"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    country_data = json.loads(response.text)
    locale.setlocale(locale.LC_ALL, '')

    country_total_confirmed = country_data[0]['confirmed']
    country_total_recovered = country_data[0]['recovered']
    country_total_death = country_data[0]['deaths']

    #country todays data
    url = "https://covid-19-data.p.rapidapi.com/report/country/name"
    before_today_date = str(datetime.date.today() - datetime.timedelta(1))
    querystring = {"date-format": "YYYY-MM-DD", "format": "json", "date": before_today_date, "name": country}

    headers = {
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
        'x-rapidapi-key': "7be87834c4msh50d6f6176b86285p18e58ajsnef3f9a5da09a"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    country_data = json.loads(response.text)
    locale.setlocale(locale.LC_ALL, '')

    is_there_data = False
    #check if there is data
    if len(country_data[0]['provinces'][0]) > 1:
        is_there_data = True
        country_total_confirmed_previousday = country_data[0]['provinces'][0]['confirmed']
        country_total_death_previousday = country_data[0]['provinces'][0]['deaths']
        country_total_recovered_previousday = country_data[0]['provinces'][0]['recovered']


        today_confirmed = (country_total_confirmed-country_total_confirmed_previousday)
        today_deaths = (country_total_death-country_total_death_previousday)
        today_recovered = (country_total_recovered-country_total_recovered_previousday)
    else:
        today_confirmed = 0
        today_deaths = 0
        today_recovered = 0

        country_total_confirmed_previousday = country_total_confirmed
        country_total_recovered_previousday = country_total_death
        country_total_death_previousday = country_total_recovered

    #country yesterday
    url = "https://covid-19-data.p.rapidapi.com/report/country/name"
    day_before_previous_day = str(datetime.date.today() - datetime.timedelta(2))

    querystring = {"date-format": "YYYY-MM-DD", "format": "json", "date": day_before_previous_day, "name": country}

    headers = {
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
        'x-rapidapi-key': "7be87834c4msh50d6f6176b86285p18e58ajsnef3f9a5da09a"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    country_data = json.loads(response.text)
    locale.setlocale(locale.LC_ALL, '')

    country_total_confirmed_before_previousday = country_data[0]['provinces'][0]['confirmed']
    country_total_death_before_previousday = country_data[0]['provinces'][0]['deaths']
    country_total_recovered_before_previousday = country_data[0]['provinces'][0]['recovered']


    if is_there_data == True:
        confirmed_yesterday = (country_total_confirmed_previousday-country_total_confirmed_before_previousday)
        death_yesterday = (country_total_death_previousday-country_total_death_before_previousday)
        recovered_yesterday = (country_total_recovered_previousday-country_total_recovered_before_previousday)
    else:
        confirmed_yesterday = country_total_confirmed - country_total_confirmed_before_previousday
        death_yesterday = country_total_death - country_total_death_before_previousday
        recovered_yesterday = country_total_recovered - country_total_recovered_before_previousday


    all_data ={
        'country':country,
        'date':date,
        'world':{
            'confirmed':world_wide_data[0]['confirmed'],
            'deaths':world_wide_data[0]['deaths'],
            'recovered':world_wide_data[0]['recovered'],
        },
        'bd_total':{
            'confirmed':country_total_confirmed,
            'deaths':country_total_death,
            'recovered':country_total_recovered,
        },
        'bd_today':{
            'confirmed':today_confirmed,
            'deaths':today_deaths,
            'recovered':today_recovered,
        },
        'bd_yesterday':{
            'confirmed':confirmed_yesterday,
            'deaths':death_yesterday,
            'recovered':recovered_yesterday,
        },
    }

    return render(request,"tracker/index.html",all_data)
