import datetime
import json
import os

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


SCOPES = 'https://www.googleapis.com/auth/calendar'  # Setup the Calendar API
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('/Users/thomsuykerbuyk/GitHub/AmphiaBot/Agenda/client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))


def get_month(month):
    """Open the csv-file for a specific month and returns a dictionary with date and shift."""
    with open('/Users/thomsuykerbuyk/GitHub/AmphiaBot/Roosters/' + month + '/' + month + '.csv', 'r') as new_file:
        lines = new_file.readlines()
        lines = [line.split(',') for line in lines]

    agenda = {}  # saving all information in dictionary called agenda
    for line in lines:
        agenda[line[0]] = line[1][:-1]  # line[0] == date, line[1] == shift
    return agenda


def insert_events(month):
    """Insert all events for a specific month. Event consists out of
    day to work and shift"""
    agenda = get_month(month)
    for datum, shift in agenda.items():
        with open('/Users/thomsuykerbuyk/GitHub/AmphiaBot/Roosters/' + month + '/' + datum + '.json', 'r') as new_file:
            lines = new_file.readlines()
            lines = [json.loads(line) for line in lines]
            lines = lines[0]
        description = []
        for co_worker_name, shift_worker in lines.items():
            if co_worker_name != 'NaN' or co_worker_name != '--':
                description.append((co_worker_name + "\tDienst: " + shift_worker))
        if shift == '4':
            start_time = 'T06:30:00'
            end_time = 'T15:00:00'
        elif shift == '3' or shift == '9' or shift == '12':
            start_time = 'T07:00:00'
            end_time = 'T15:00:00'
        elif shift == '10' or shift == '11' or shift == '13':
            start_time = 'T10:00:00'
            end_time = 'T18:30:00'
        elif shift == 'BH2':
            start_time = 'T14:30:00'
            end_time = 'T18:30:00'
        else:
            start_time = 'T08:00:00'
            end_time = 'T16:30:00'
        event = {
            'summary': 'Amphia dienst: ' + shift,
            'location': 'Amphia Hospital, Molengracht 21, 4818 CK Breda',
            'description': '\n'.join(description),
            'start': {
                'dateTime': datum + start_time + '+02:00',
                'timeZone': 'Europe/Amsterdam',
            },
            'end': {
                'dateTime': datum + end_time + '+02:00',
                'timeZone': 'Europe/Amsterdam',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 60},
                ],
            },
        }

        # add event to calendar
        event = service.events().insert(calendarId='primary', body=event).execute()
        # shows event has been created
        print('Bot created the event: %s' % (event.get('htmlLink')))


def get_month_dates(get_dates):
    """Returns the right format for a month"""
    now = datetime.datetime.now()
    months = {'januari': [str(now.year + 1) + "-01-01", str(now.year + 1) + "-02-01"],
              'februari': [str(now.year) + "-02-01", str(now.year) + "-03-01"],
              'maart': [str(now.year) + "-03-01", str(now.year) + "-04-01"],
              'april': [str(now.year) + "-04-01", str(now.year) + "-05-01"],
              'mei': [str(now.year) + "-05-01", str(now.year) + "-06-01"],
              'juni': [str(now.year) + "-06-01", str(now.year) + "-07-01"],
              'juli': [str(now.year) + "-07-01", str(now.year) + "-08-01"],
              'augustus': [str(now.year) + "-08-01", str(now.year) + "-09-01"],
              'september': [str(now.year) + "-09-01", str(now.year) + "-10-01"],
              'oktober': [str(now.year) + "-10-01", str(now.year) + "-11-01"],
              'november': [str(now.year) + "-11-01", str(now.year) + "-12-01"],
              'december': [str(now.year) + "-12-01", str(now.year + 1) + "-01-01"]}

    start_month = months[get_dates][0] + 'T01:00:00Z'
    end_month = months[get_dates][1] + 'T01:00:00Z'
    return start_month, end_month


def delete_events(month):
    """Delete all events in the Roosters/'month' folder and all events for
    specific month in the agenda
    """
    start_month, end_month = get_month_dates(month)
    # agenda = get_month(month)
    page_token = None
    ids_to_delete = []
    while True:
        events = service.events().list(calendarId='primary', pageToken=page_token,
                                       timeMin=start_month, timeMax=end_month).execute()
        for event in events['items']:
            ids_to_delete.append(event['id'])
        page_token = events.get('nextPageToken')
        if not page_token:
            break
    for id_to_delete in ids_to_delete:
        service.events().delete(calendarId='primary', eventId=id_to_delete).execute()

    folder = '/Users/thomsuykerbuyk/GitHub/AmphiaBot/Roosters/' + month
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as problem:
            print(problem)
