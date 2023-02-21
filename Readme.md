
# Тестовое задание для стажера на позицию «Программист на языке Python»
___

## Сервер реализован с помощью:
* Python версии 3.8.10
* Django версии 4.1.6
___
## БД использована не была, все данные берутся напрямую из текстового файла *RU.txt*
___
### Первый метод: Метод принимает идентификатор geonameid и возвращает информацию о городе.
 ```python

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

``` 

Метод принемает запрос GET и ID объекта, после чего открывается файл RU.txt в котором перебираются строки, к которым применяется метод split() для разделения полей. Первый элемент получившегося списка полей сравнивается с введенным пользователем индификатором и, если они совпали, информация записывается в JSON формат и отображается на странице, если же индефикатор так и не был найден - возвращается "Страница не найдена".
___

### Второй метод: Метод принимает страницу и количество отображаемых на странице городов и возвращает список городов с их информацией. 

 ``` python
 def getinfopage(request, page: int, items_on_page: int):
    page_data = {"page": page,
                 "items": []}
    iterations = 0
    with open("RU.txt", mode='r', encoding='utf-8', newline='\n') as file:
        for item, dataset in enumerate(file.readlines()):
            if item/items_on_page + 1 < page:
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
 ``` 
Этот метод получает от позьзователя две переменных(страницу и количество элементов на странице), аналогично открывается текстовый файл с данными и построчно перебирается. Деля количество пройденных элементов *__item__* на количество заданных *__items_on_page__*, получается количество пройденных страниц, а так как отсчет страниц обычно начинается с первой, то прибавляем к этому числу 1.

Как нужная страница была найдена, аналогично прошлому методу разделяем строку на поля и формируем список с элементами, в последствии формуриется *Json-файл* и возвращается пользователю для отображения

---
### Третий метод: Метод принимает названия двух городов (на русском языке) и получает информацию о найденных городах, а также дополнительно: какой из них расположен севернее и одинаковая ли у них временная зона (когда несколько городов имеют одно и то же название, разрешать неоднозначность выбирая город с большим населением; если население совпадает, брать первый попавшийся)

 ``` python
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
 ``` 
Этот метод получает названия двух городов, и аналогично прошлым методам читает файл, разбивает строки на поля. Метод сравнивает названия введенные пользователем с альтернативными названиями объекта, если они подходят, то добавляются в список "подходящих городов".

Чтобы выбрать подходящий объект, сравнивается его население (*__population__*), и город с первым повавшимся из наибольших по населению объектов считается подходящим. 

Для определения какой объект расположен севернее сравниваются их широта (*__latitude__*), а так же их временная зона (*__timezone__*) для определения, в одном ли временом поясе они находятся.

После чего формируется Json-файл и отправляется пользователю

___


