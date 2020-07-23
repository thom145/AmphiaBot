from datetime import datetime

import calendar
import json
import numpy
import os, sys, shutil
import pandas as pd

def get_schedule(month):
    """Open .xls file and return data without NaN values."""
    dfs = pd.read_excel('  ../R/Roosters/' + month + '/' + month + '.xls', sheet_name=None)
    data = dfs['Master schedule ESS']
    data = data.dropna(how='all')
    return data


def get_position_from_roster(data):
    """Get the position of user and return this poistion."""
    position = 0
    for i in data['Unnamed: 1']:
        position += 1
        if i == 'Suijkerbuijk, T.':
            break
    return position


def create_csv(data, position, month):
    """Get days to work and shifts from .xls and save to a csv file

    Keyword arguments:
    data = data in .xls file
    position = users position in .xls
    month = month to use
    """
    data.columns = data.iloc[4] # set datum column as header

    days_to_work = data.iloc[position] # get days to work
    days_to_work = days_to_work.dropna() # remove na values
    # store days to work and shifts in csv file
    days_to_work.to_csv('/Users/thomsuykerbuyk/GitHub/AmphiaBot/Roosters/' + month + '/' + month + '.csv')


def run_all(month):
    """Runs all functions to create csv file containting
    days to work and shifst for a specific month"""
    data = get_schedule(month) # get schedule (=.xls)
    position = get_position_from_roster(data) # get users position in .xls
    create_csv(data, position, month) # creates csv file from .xls


def get_month(month):
    """Returns information in .csv as a dictionary"""
    with open('/Users/thomsuykerbuyk/GitHub/AmphiaBot/Roosters/' + month + '/' + month + '.csv', 'r') as new_file:
        lines = new_file.readlines()
        lines = [line.split(',') for line in lines]

    agenda = {} # contains days to work and shifts
    for line in lines:
        agenda[line[0]] = line[1][:-1] # agenda[line[0]] == day, line[1][:-1] == shift
    return agenda


def get_days_to_work(month):
    """Returns all days the user has to work in a specific month"""
    list_days = []
    days = get_month(month) # days to work
    for day, shift in days.items():
        list_days.append(day)
    return days


def change_data_columns(month):
    """Setting the datums as column, returns this dataframe"""
    schedule = get_schedule(month)
    days = []
    days_to_convert = schedule.loc[9]
    x = list(days_to_convert)
    for item in x:
        if isinstance(item, numpy.float64):
            days.append('0')
        elif isinstance(item, float):
            days.append('0')
        else:
            days.append(item.strftime("%Y-%m-%d"))
    schedule.columns = days
    return schedule


def get_name_and_shift(shift, month):
    """Get the name corresponding to a shift"""
    position = []
    name_shift = []
    schedule = get_schedule(month)
    dictionary = shift.to_dict()
    new_dict = {}
    for key, item in shift.to_dict().items():
        position.append(key-1)
        print(key, item)
    # if len of position == 0 shift is not present on that day
    if len(position) > 0:
        # if len of position > 1 more than 1 person has that shift
        if len(position) > 1:
            for item in position:
                name_shift.append((list(schedule.loc[[item]]['Unnamed: 1']), dictionary[item+1]))
        else:
            name_shift.append((list(schedule.loc[[position[0]]]['Unnamed: 1']), dictionary[position[0]+1]))
    for people in name_shift:
        new_dict[people[0][0]] = people[1]
    return new_dict


def get_co_workers(month):
    """Get the name of the coworkers (and shifts) that user
    works with on that day. Save information in a datum.json file
    """
    schedule = change_data_columns(month)
    days_to_work = list(get_days_to_work(month))
    for day in days_to_work:
        datetime_object = datetime.strptime(day, '%Y-%m-%d')
        weekday = calendar.day_name[datetime_object.weekday()]
        if weekday == 'Sunday':
            clean_schedule = schedule[day].dropna()
            shift_3 = clean_schedule[clean_schedule == '3']
            d_3 = get_name_and_shift(shift_3, month)

            shift_12 = clean_schedule[clean_schedule == '12']
            d_12 = get_name_and_shift(shift_12, month)

            shift_13 = clean_schedule[clean_schedule == '13']
            d_13 = get_name_and_shift(shift_13, month)

            shift_bh2 = clean_schedule[clean_schedule == 'BH2']
            d_bh2 = get_name_and_shift(shift_bh2, month)

            all_shifts = dict(list(d_3.items()) + list(d_12.items()) +
                                list(d_13.items()) + list(d_bh2.items()) )
            with open('/Users/thomsuykerbuyk/GitHub/AmphiaBot/Roosters/' + month + '/' + day + '.json', 'w') as new_file:
                new_file.write(json.dumps(all_shifts))

        elif weekday == 'Saturday':
            clean_schedule = schedule[day].dropna()
            shift_4 = clean_schedule[clean_schedule == '4']
            d_4 = get_name_and_shift(shift_4, month)

            shift_9 = clean_schedule[clean_schedule == '9']
            d_9 = get_name_and_shift(shift_9, month)

            shift_10 = clean_schedule[clean_schedule == '10']
            d_10 = get_name_and_shift(shift_10, month)

            shift_11 = clean_schedule[clean_schedule == '11']
            d_11 = get_name_and_shift(shift_11, month)

            all_shifts = dict(list(d_4.items()) + list(d_9.items()) +
                                list(d_10.items()) + list(d_11.items()))
            with open('/Users/thomsuykerbuyk/GitHub/AmphiaBot/Roosters/' + month + '/' + day + '.json', 'w') as new_file:
                new_file.write(json.dumps(all_shifts))
        else:
            clean_schedule = schedule[day].dropna()

            shift_1 = clean_schedule[clean_schedule == 'VD1']
            d_1 = get_name_and_shift(shift_1, month)

            shift_2 = clean_schedule[clean_schedule == 'VD2']
            d_2 = get_name_and_shift(shift_2, month)

            shift_3 = clean_schedule[clean_schedule == 'VD3']
            d_3 = get_name_and_shift(shift_3, month)

            shift_4 = clean_schedule[clean_schedule == 'VD4']
            d_4 = get_name_and_shift(shift_4, month)

            shift_5 = clean_schedule[clean_schedule == 'VD5']
            d_5 = get_name_and_shift(shift_5, month)

            shift_algemeen = clean_schedule[clean_schedule == '1']
            shift_steriel = clean_schedule[clean_schedule == '8']

            d_alg = get_name_and_shift(shift_algemeen, month)
            d_str = get_name_and_shift(shift_steriel, month)

            all_shifts = dict(list(d_pb_1.items()) + list(d_pb_1_plus.items()) +
                                list(d_pb_2.items()) + list(d_alg.items()) +
                                list(d_str.items()) + list(d_1.items()) +
                                list(d_2.items()) + list(d_3.items()) +
                                list(d_4.items()) + list(d_5.items()))
            with open('/Users/thomsuykerbuyk/GitHub/AmphiaBot/Roosters/' + month + '/' + day + '.json', 'w') as new_file:
                new_file.write(json.dumps(all_shifts))
