from bs4 import BeautifulSoup
import requests
import re
import csv


source = requests.get('https://www.iplt20.com/results/men').text

soup = BeautifulSoup(source, 'lxml')

csv_file = open('IPL.csv', 'w')

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['team_1','team_2','team_1_score', 'team_2_score','venue'])


for whole in soup.find_all('div',class_=re.compile('js-match match-list__item result \w+')):
    count = 1
    for team in whole.find_all('p',class_='result__team-name'): #Team Names
        if count == 1:
            team_1 = team.text
        elif count == 2:
            team_2 = team.text
        count+=1

    win_count = 1
    for win_score in whole.find_all('span', class_='result__score'): #scores
        if win_count == 1:
            team_1_score = win_score.text.split('\n')[1]
        if win_count == 2:
            team_2_score = win_score.text.split('\n')[1]
        win_count+=1 #scores

    venue = whole.find('p', 'result__info u-show-phablet').text #venue
    venue = venue.split('\n')[-2].split(' ')[-1]


    csv_writer.writerow([team_1, team_2, team_1_score, team_2_score, venue])

csv_file.close()  #closing first CSV file

"""
Extracting match dates and day in separate csv file as match_dates,csv
"""

new_csv = open('match_dates.csv', 'w')
new_csv_writer = csv.writer(new_csv)

new_csv_writer.writerow(['match_date', 'match_day'])


for match_dat in soup.find_all('h3', class_='match-list__date js-date'):
    match_date = match_dat.text.split(' ')[1:3]
    match_day = match_dat.text.split(' ')[0]
    new_csv_writer.writerow([match_date, match_day])

new_csv.close()

