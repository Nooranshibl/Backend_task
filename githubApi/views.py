from django.shortcuts import render

import requests
import datetime


def index(request):
    past_days = 10
    current_date = datetime.datetime.today()
    desired_date = current_date - datetime.timedelta(days=past_days)
    desired_date_str = desired_date.strftime('%Y-%m-%d')

    api_url = f"https://api.github.com/search/repositories?q=created%3E{desired_date_str}&sort=stars&order=desc"
    response = requests.get(api_url)
    content = response.json()
    total_count = content['total_count']

    languages = {}
    # Get 3 Trending Repos
    for i in range(0, 3):
        repo = content['items'][i]
        repo_language = repo['language']
        if repo_language is not None:
            if repo_language not in languages:
                languages[repo_language] = 1
            else:
                languages[repo_language] + 1

    if len(languages.keys()) == 0:
        raise Exception("All three trending repos don't have any languages.")

    item_per_page = 30
    total_pages = int(total_count / item_per_page) + 2
    for page in range(1, total_pages):
        api_url = f"https://api.github.com/search/repositories?q=created%3E{desired_date_str}" \
            f"&sort=stars&order=desc&page={page}"
        response = requests.get(api_url)
        content = response.json()
        for item in content['items']:
            #print(item['language'])
            if item['language'] in languages:
                languages[item['language']] = languages[item['language']] + 1

    #print(languages)
    return render(request, 'github.html', {'languages': languages})
