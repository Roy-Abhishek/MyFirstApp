from django.shortcuts import render
import requests
import json
import pyperclip
import pyshorteners as shortener
from .models import TypedUrls
from datetime import date, timedelta
from random import randint, sample
from urllib.parse import quote_plus

# sys.path.append("C:\\Users\\anirb\\anaconda3\\Lib\\site-packages\\prompt_toolkit\\clipboard\\pyperclip.py")


API_KEY_REBRANDLY = 'a5cd157211474acfbc37e5ac4042eb11'
API_KEY_NASA = 'dbVyQtEYBxopGCfcvRmCYjTGOceTDBjHU9NcPank'


def home_screen(request):
    return render(request, 'base.html')


def short_url_screen(request):
    IS_ERROR = False

    input_url = request.POST.get('input-url')
    tiny_url_input = f'{input_url}/'

    try:
        tiny_url = shortener.Shortener(domain='https://0x0.st').nullpointer.short(tiny_url_input)
    except:
        IS_ERROR = True
        tiny_url = 'https://0x0.st/Si'

    tiny_url_split_list = tiny_url.split('''
''')
    tiny_url_split = tiny_url_split_list[0]
    part_url = f'https://api.rebrandly.com/v1/links/new?apikey={API_KEY_REBRANDLY}&destination={tiny_url_split}'
    full_url = part_url + "&domain[fullName]=rebrand.ly"
    data = requests.get(full_url).text
    data_json = json.loads(data)
    data_json = data_json['shortUrl']
    # pyperclip.copy(data_json)

    try:
        TypedUrls.objects.create(entered_url=input_url, returned_url=data_json)
    except:
        pass

    stuff_for_frontend = {
        'IS_ERROR': IS_ERROR,
        'data_json': data_json,
        'input_url': input_url,
    }

    return render(request, 'myapp_app/new-url.html', stuff_for_frontend)


def bored_screen(request):
    yesterday = date.today() - timedelta(days=1)
    data = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={API_KEY_NASA}&date={yesterday}').text
    data_json = json.loads(data)
    data_json_description = data_json["explanation"]
    data_json_image = data_json["hdurl"]

    stuff_for_front_end = {
        'data_json_description': data_json_description,
        'data_json_image': data_json_image
    }

    return render(request, 'bored.html', stuff_for_front_end)


def bored_results_screen(request):
    global IS_NOTHING_NASA
    global url_numbers
    global IS_NOTHING_NUMBER_FACT
    global url_advice
    global ADVICE_IS_INT
    global IS_NOTHING_ADVICE
    global cat_facts
    global MAGIC_IS_INT
    global message
    global IS_NOTHING_JOKES
    global IS_NOTHING_NUMBER
    global IS_NOTHING_DOG
    global IS_DOG_ERROR
    global IS_NOTHING_CAT_PICS
    global IS_NOTHING_CAT_FACTS
    IS_NOTHING_NASA = False
    IS_NOTHING_NUMBER_FACT = False
    ADVICE_IS_INT = False
    IS_NOTHING_ADVICE = False
    IS_NOTHING_CAT_PICS = False
    IS_NOTHING_CAT_FACTS = False
    IS_DOG_ERROR = False
    IS_NOTHING_DOG = False
    MAGIC_IS_INT = False
    IS_NOTHING_NUMBER = False
    IS_NOTHING_JOKES = False
    jason_str = dict(request.POST.lists())
    try:
        input_number = int(jason_str['num-jokes'][0])
    except ValueError:
        input_number = 1
    input_dark_type = jason_str['type-jokes-dark'][0]
    input_misc_type = jason_str['type-jokes-misc'][0]
    try:
        magic_input = int(request.POST.get('8ball-number'))
        MAGIC_IS_INT = True
    except:
        magic_input = request.POST.get('8ball-number')
        MAGIC_IS_INT = False
    dog_input = request.POST.get('input-dogs')
    try:
        cat_pics = int(request.POST.get('input-cats-pic'))
    except:
        cat_pics = request.POST.get('input-cats-pic')
        IS_NOTHING_CAT_PICS = True
    cat_facts = request.POST.get('input-cats-fact')
    try:
        advice_query = int(request.POST.get('input-advice'))
        ADVICE_IS_INT = True
    except:
        advice_query = request.POST.get('input-advice').lower()
        ADVICE_IS_INT = False
    number_fact_query = request.POST.get('input-number-fact')
    try:
        nasa_input = int(request.POST.get('input-nasa'))
        IS_NOTHING_NASA = False
    except:
        nasa_input = request.POST.get('input-nasa')
        IS_NOTHING_NASA = True
    message = ""
    joke = []
    dogs = []
    cats_pictures = []
    cats_facts = ""

    # JOKES STUFF FROM HERE
    if input_dark_type.lower() == "yes" and input_misc_type.lower() == "yes":
        url_cats = f"https://sv443.net/jokeapi/v2/joke/Programming,Dark,Miscellaneous,Pun,Spooky,Christmas?blacklistFlags=nsfw,religious,political,racist,sexist&type=twopart&amount={input_number}"
    elif input_dark_type.lower() == "no" and input_misc_type.lower() == "yes":
        url_cats = f"https://sv443.net/jokeapi/v2/joke/Programming,Miscellaneous,Pun,Spooky,Christmas?blacklistFlags=nsfw,religious,political,racist,sexist&type=twopart&amount={input_number}"
    elif input_dark_type.lower() == "yes" and input_misc_type.lower() == "no":
        url_cats = f"https://sv443.net/jokeapi/v2/joke/Programming,Dark,Pun,Spooky,Christmas?blacklistFlags=nsfw,religious,political,racist,sexist&type=twopart&amount={input_number}"
    elif input_dark_type.lower() == "no" and input_misc_type.lower() == "no":
        url_cats = f"https://sv443.net/jokeapi/v2/joke/Programming,Pun,Spooky,Christmas?blacklistFlags=nsfw,religious,political,racist,sexist&type=twopart&amount={input_number}"
    else:
        url_cats = f"https://sv443.net/jokeapi/v2/joke/Programming,Pun,Spooky,Christmas?blacklistFlags=nsfw,religious,political,racist,sexist&type=twopart&amount={input_number}"

    data = requests.get(url_cats).text
    data_json = json.loads(data)
    if input_number == 1:
        pass
    else:
        data_json = data_json['jokes']

    if jason_str['num-jokes'][0] == "":
        joke.append("")
        IS_NOTHING_JOKES = True
    elif input_number == 1:
        joke.append(f'{data_json["setup"]}... {data_json["delivery"]}')
    else:
        for jokes in data_json:
            joke.append(f'{jokes["setup"]}... {jokes["delivery"]}')

    # 8-BALL STUFF FROM HERE
    if magic_input == "random":
        random_int = randint(1, 8)
    else:
        random_int = 10

    if magic_input == 1 or random_int == 1:
        message = "\"You are awesome and you know it. You just have to stop caring about other people's jealous opinions.\" ~ Anonymous"
    elif magic_input == 2 or random_int == 2:
        message = "\"Sometimes it's okay if the only thing you did today is breath.\" ~ Yumi Sakugawa"
    elif magic_input == 3 or random_int == 3:
        message = "\"Nobody wants to hear this, but sometimes the person you want the most, is the one you're best without.\" ~ Anonymous"
    elif magic_input == 4 or random_int == 4:
        message = "\"If people are doubting how far you go, go so far that you can't hear them anymore.\" ~ Michele Ruiz"
    elif magic_input == 5 or random_int == 5:
        message = "\"Everybody look at you strange. Say you changed. Like you worked that hard to stay the same. Uhh.\" ~ Jay-Z"
    elif magic_input == 6 or random_int == 6:
        message = "\"Sometimes I'm the mess. Sometimes I'm the broom. On the hardest days, I have to be both.\" ~ Ruby Francisco"
    elif magic_input == 7 or random_int == 7:
        message = "\"Tell yourself whatever you need to hear, you're the only one listening.\" ~ Gia Carangi"
    elif magic_input == 8 or random_int == 8:
        message = "\"We either make ourselves miserable or we make ourselves strong. The amount of work is the same.\" ~ Carlos Castaneda"
    elif magic_input != "random":
        message = ""
        IS_NOTHING_NUMBER = True

    # DOGS STUFF FROM HERE
    if dog_input.lower() == '':
        IS_NOTHING_DOG = True

    if dog_input.lower() != 'australian shepherd' and dog_input.lower() != 'random' and dog_input.lower() != "":
        dog_input_list = dog_input.split(" ")
        if len(dog_input_list) == 2 and dog_input_list[1] == 'shepherd' and dog_input.lower() == 'australian shepherd':
            pass
        else:
            dog_input_list = dog_input_list[::-1]
    elif dog_input.lower() == 'australian shepherd' and dog_input.lower() != 'random' and dog_input.lower() != "":
        dog_input_list = dog_input.split(" ")

    if dog_input.lower() == 'random':
        url_dog = f'https://dog.ceo/api/breeds/image/random'
    elif dog_input.lower() != '' and len(dog_input_list) == 2:
        url_dog = f'https://dog.ceo/api/breed/{dog_input_list[0]}/{dog_input_list[1]}/images'
    elif dog_input.lower() != '' and len(dog_input_list) == 1:
        url_dog = f'https://dog.ceo/api/breed/{dog_input_list[0]}/images'
    else:
        url_dog = f'https://dog.ceo/api/breeds/image/random'

    data_dogs = requests.get(url_dog).text
    data_dogs_json = json.loads(data_dogs)

    if data_dogs_json['status'] == 'error' in data_dogs_json:
        IS_DOG_ERROR = True
        dogs.append('')
    elif dog_input.lower() == 'random' and data_dogs_json['status'] != 'error':
        dogs.append(data_dogs_json['message'])
    elif dog_input.lower() != '' and data_dogs_json['status'] != 'error':
        try:
            for x in sample(data_dogs_json['message'], 3):
                dogs.append(x)
        except:
            dogs.append('Please enter a valid dog breed')
            IS_DOG_ERROR = True
    else:
        IS_DOG_ERROR = True

    # CATS STUFF FROM HERE
    random_cat_int = randint(1, 280)

    if cat_facts == "" and type(cat_pics) != type(1):
        cat_pics = 0
        IS_NOTHING_CAT_PICS = True
        IS_NOTHING_CAT_FACTS = True
    elif type(cat_pics) != type(1) or cat_pics > 10:
        cat_pics = 0
        IS_NOTHING_CAT_PICS = True
    elif cat_facts == "":
        IS_NOTHING_CAT_FACTS = True

    url_cats = "https://api.thecatapi.com/v1/favourites"

    payload = {}
    files = {}
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': '17d94b92-754f-46eb-99a0-65be65b5d18f'
    }

    data_cats_pics = requests.request("GET", url_cats, headers=headers, data=payload, files=files).text
    data_json_cats_pics = json.loads(data_cats_pics)
    data_cats_facts = requests.get('https://cat-fact.herokuapp.com/facts').text
    data_json_cats_facts = json.loads(data_cats_facts)

    if not IS_NOTHING_CAT_PICS:
        for number_cats in range(0, cat_pics):
            cats_pictures.append(data_json_cats_pics[number_cats]['image']['url'])
    else:
        cats_pictures.append('')

    if cat_facts.lower() == "yes":
        cats_facts = data_json_cats_facts['all'][random_cat_int]['text']
    else:
        IS_NOTHING_CAT_FACTS = True
        cat_facts = ""

    # ADVICE STUFF FROM HERE
    if not ADVICE_IS_INT and advice_query != "random" and advice_query != "yes":
        IS_NOTHING_ADVICE = True
    elif not ADVICE_IS_INT or advice_query == "random" or advice_query == "yes":
        IS_NOTHING_ADVICE = False
    elif ADVICE_IS_INT and type(advice_query) == type(1) and (advice_query <= 0 or advice_query >= 211):
        IS_NOTHING_ADVICE = True
    elif ADVICE_IS_INT and type(advice_query) == type(1) and (advice_query > 0 or advice_query < 211):
        IS_NOTHING_ADVICE = False

    url_advice = 'https://api.adviceslip.com/advice'

    if type(advice_query) == type(1) and not IS_NOTHING_ADVICE:
        url_advice = f'https://api.adviceslip.com/advice/{advice_query}'
    elif type(advice_query) == type('hello') and advice_query == "random" or "yes": # (not ADVICE_IS_INT and advice_query.lower() == "random") or (not ADVICE_IS_INT and advice_query.lower() == "yes")
        url_advice = f'https://api.adviceslip.com/advice'
    else:
        url_advice = f'https://api.adviceslip.com/advice'

    data_advice = requests.get(url_advice).text
    if type(advice_query) == type(1) and not IS_NOTHING_ADVICE:
        data_json_advice = json.loads(data_advice + "}")
    elif type(advice_query) == type('hello') and advice_query == "random" or "yes":
        data_json_advice = json.loads(data_advice)
    else:
        data_json_advice = json.loads(data_advice)

    try:
        advice = data_json_advice['slip']['advice']
    except:
        advice = "Your number seems to be out of range"

    # NUMBER FACTS STUFF FROM HERE
    if number_fact_query.lower() == 'random':
        url_numbers = 'http://numbersapi.com/random/math'
    elif number_fact_query.lower() == 'trivia':
        url_numbers = 'http://numbersapi.com/random/trivia'
    elif number_fact_query.lower() == 'year':
        url_numbers = 'http://numbersapi.com/random/year'
    elif number_fact_query.lower() == 'date':
        url_numbers = 'http://numbersapi.com/random/date'
    elif number_fact_query.lower() == 'math':
        url_numbers = 'http://numbersapi.com/random/math'
    else:
        url_numbers = 'https://www.google.com'
        IS_NOTHING_NUMBER_FACT = True

    data_number_facts = requests.get(url_numbers).text

    # ALL THE NASA INPUT STUFF FROM HERE
    if not IS_NOTHING_NASA and type(nasa_input) == type(1) and 0 <= nasa_input <= 91:
        yesterday = date.today() - timedelta(days=(1+nasa_input))
        data = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={API_KEY_NASA}&date={yesterday}').text
        data_json = json.loads(data)
        data_json_description = data_json["explanation"]
        data_json_image = data_json["hdurl"]
    elif IS_NOTHING_NASA:
        IS_NOTHING_NASA = True
        data_json_description = ""
        data_json_image = ""
    else:
        IS_NOTHING_NASA = True
        data_json_description = ""
        data_json_image = ""

    stuff_for_frontend = {
        'joke': joke,
        'MAGIC_IS_INT': MAGIC_IS_INT,
        'magic_input': magic_input,
        'random_int': random_int,
        'message': message,
        'IS_NOTHING_NUMBER': IS_NOTHING_NUMBER,
        'IS_NOTHING_JOKES': IS_NOTHING_JOKES,
        'IS_NOTHING_DOG': IS_NOTHING_DOG,
        'IS_DOG_ERROR': IS_DOG_ERROR,
        'dogs': dogs,
        'input_number': input_number,
        'dog_input': dog_input,
        'cats_facts': cats_facts,
        'cats_pictures': cats_pictures,
        'IS_NOTHING_CAT_PICS': IS_NOTHING_CAT_PICS,
        'IS_NOTHING_CAT_FACTS': IS_NOTHING_CAT_FACTS,
        'IS_NOTHING_ADVICE': IS_NOTHING_ADVICE,
        'advice': advice,
        'data_number_facts': data_number_facts,
        'IS_NOTHING_NUMBER_FACT': IS_NOTHING_NUMBER_FACT,
        'IS_NOTHING_NASA': IS_NOTHING_NASA,
        'data_json_description': data_json_description,
        'data_json_image': data_json_image,
    }

    return render(request, 'myapp_app/bored_results.html', stuff_for_frontend)
