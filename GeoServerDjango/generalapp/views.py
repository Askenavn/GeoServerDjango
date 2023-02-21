import json
from django.shortcuts import render
from django.http import JsonResponse, FileResponse, HttpResponse


fields = ['geonameid', 'name', 'asciiname', 'alternatenames', 'latitude', 'longitude', 'feature_class', 'feature_code',
          'country_code', 'cc2', 'admin1_code', 'admin2_code', 'admin3_code', 'admin4_code', 'population', 'elevation',
          'dem', 'timezone', 'modification_date']

def index(request):
    #First method use
    first_method = request.GET.get('geonameid', '')
    if first_method:
        return getinfo(request, geonameid=first_method)

    #Second method use
    second_method_page = request.GET.get('page', '')
    second_method_items = request.GET.get('items_on_page', '')
    if second_method_page and second_method_items:
        return getinfopage(request, page=int(second_method_page), items_on_page=int(second_method_items))

    #Third method use
    third_method_fst_city = request.GET.get('fstcity', '')
    third_method_snd_city = request.GET.get('sndcity', '')
    if third_method_snd_city and third_method_fst_city:
        return two_city_north(request, third_method_fst_city, third_method_snd_city)

    #Template of page with search
    return render(request, 'generalapp/index.html')


def getinfo(request, geonameid):
    find = False
    with open("RU.txt", mode='r', encoding='UTF-8', newline='\n') as file:
        for item, dataset in enumerate(file.readlines()):
            data = dataset[:-1].split(sep='\t')
            if data[0] == geonameid:
                find = True
                with open('jsonfile.json', 'w+') as fp:
                    dict = {name: data[i] for i, name in enumerate(fields)}
                    json.dump(dict, fp, indent=1, ensure_ascii=False)
    if not find:
        return page_not_found404(request)
    return FileResponse(open('jsonfile.json', 'rb'))


def getinfopage(request, page: int, items_on_page: int):
    page_data = {"page": page,
                 "items": []}
    iterations = 0
    with open("RU.txt", mode='r', encoding='utf-8', newline='\n') as file:
        for item, dataset in enumerate(file.readlines()):
            if (item/items_on_page) + 1 < page:
                pass
            else:
                data = dataset[:-1].split(sep='\t')
                dict = {name: data[i] for i, name in enumerate(fields)}
                page_data["items"].append(dict)
                iterations += 1
            if iterations == items_on_page:
                with open('jsonfile.json', 'w+') as fp:
                    json.dump(page_data, fp, indent=3, ensure_ascii=False)
                return FileResponse(open('jsonfile.json', 'rb'))


def two_city_north(request, namefstcity, namesndcity):
    matchedfstcities = []
    matchedsndcities = []
    page_data = {"items": [],
                 "norther is": None,
                 "same_time_zone": None}
    with open("RU.txt", mode='r', encoding='utf-8', newline='\n') as file:
        for item, dataset in enumerate(file.readlines()):
            data = dataset[:-1].split(sep='\t')
            for altername in data[3].split(sep=','):
                if namefstcity == altername:
                    matchedfstcities.append({name: data[i] for i, name in enumerate(fields)})
                elif namesndcity == altername:
                    matchedsndcities.append({name: data[i] for i, name in enumerate(fields)})
                else:
                    pass
        matched_city = None

        for city in matchedfstcities:
            if matched_city is not None:
                if int(city['population']) > int(matched_city['population']):
                    matched_city = city
            else:
                matched_city = city
        page_data['items'].append(matched_city)
        matched_city = None

        for city in matchedsndcities:
            if matched_city is not None:
                if int(city['population']) > int(matched_city['population']):
                    matched_city = city
            else:
                matched_city = city

    page_data['items'].append(matched_city)
    page_data['norther is'] = page_data['items'][0]["name"] if page_data['items'][0]["latitude"] > page_data['items'][1]["latitude"] \
        else page_data['items'][1]["name"]
    page_data['same_time_zone'] = True if page_data['items'][0]["timezone"] == page_data['items'][1]["timezone"] \
        else False

    with open('jsonfile.json', 'w') as fp:
        json.dump(page_data, fp, indent=3, ensure_ascii=False)
    return FileResponse(open('jsonfile.json', 'rb'))


def page_not_found404(request):
    return HttpResponse("<title>ERROR404</title>"
                        "<h1> ERROR 404 </h1>"
                        "Sorry, page not found\n"
                        "<h4>Please, go back to previous page and type existing or fitting request<h4>")
