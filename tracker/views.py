from django.shortcuts import render
import requests
import json
import locale
import datetime

# Create your views here.

def index(request):
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

    querystring = {"format": "json", "name": "bangladesh"}

    headers = {
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
        'x-rapidapi-key': "7be87834c4msh50d6f6176b86285p18e58ajsnef3f9a5da09a"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    country_data = json.loads(response.text)
    locale.setlocale(locale.LC_ALL, '')

    bangladesh_total_confirmed_today = country_data[0]['confirmed']
    bangladesh_total_recovered_today = country_data[0]['recovered']
    bangladesh_total_death_today = country_data[0]['deaths']

    #country todays data
    url = "https://covid-19-data.p.rapidapi.com/report/country/name"
    before_today_date = str(datetime.date.today() - datetime.timedelta(2))
    querystring = {"date-format": "YYYY-MM-DD", "format": "json", "date": before_today_date, "name": "Bangladesh"}

    headers = {
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
        'x-rapidapi-key': "7be87834c4msh50d6f6176b86285p18e58ajsnef3f9a5da09a"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    country_data = json.loads(response.text)
    locale.setlocale(locale.LC_ALL, '')

    bangladesh_total_confirmed_previousday = country_data[0]['provinces'][0]['confirmed']
    bangladesh_total_recovered_previousday = country_data[0]['provinces'][0]['recovered']
    bangladesh_total_death_previousday = country_data[0]['provinces'][0]['deaths']


    all_data ={
        'date':date,
        'world':{
            'confirmed':world_wide_data[0]['confirmed'],
            'deaths':world_wide_data[0]['deaths'],
            'recovered':world_wide_data[0]['recovered'],
        },
        'bd_total':{
            'confirmed':bangladesh_total_confirmed_today,
            'deaths':bangladesh_total_death_today,
            'recovered':bangladesh_total_recovered_today,
        },
        'bd_today':{
            'confirmed':(bangladesh_total_confirmed_today-bangladesh_total_confirmed_previousday),
            'deaths':(bangladesh_total_death_today-bangladesh_total_death_previousday),
            'recovered':(bangladesh_total_recovered_today-bangladesh_total_recovered_previousday),
        }
    }

    return render(request,"tracker/index.html",all_data)
