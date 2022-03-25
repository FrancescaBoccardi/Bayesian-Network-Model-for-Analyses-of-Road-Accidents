# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12:16:40 2022

@author: franc
"""

import pandas as pd
import numpy as np
import pathlib

def preprocessing():
    
    #---------------------------- Creating the dataset ----------------------------#
    
    # Loading crash_data dataset
    
    url_c = 'crashdata2021.csv'
    crash_data = pd.read_csv(url_c, sep=',')
    
    # Loading vehicle_crash_data dataset
    
    url_v = 'vehiclecrashdata2021.csv'
    vehicle_data = pd.read_csv(url_v, sep=',')
    
    # Summarizing crash speed information into a single 'Speed' column
    
    vehicle_data['Speed'] = np.where((vehicle_data['ViolationCodeDescription']=='Speeding') | 
                               (vehicle_data['OtherAssociatedFactor']=='Speeding'), 'over speed limits', 'under speed limits')
    
    # Dropping useless columns from crash_data and vehicle_data
    
    crash_data = crash_data.drop(['CrashFactId','TcrNumber', 'CityDamageFlag',
                'ShortFormFlag', 'Distance','PrimaryCollisionFactor', 'TrafficControl',
                'CollisionType','ProximityToIntersection', 'VehicleInvolvedWith', 'PedestrianDirectionFrom',
                'PedestrianDirectionTo', 'DirectionFromIntersection', 'Comment', 'PedestrianAction',
                'RoadwayCondition'], axis=1)
    
    vehicle_data = vehicle_data.drop(['Name','Sex','VehicleDamage','VehicleDirection','MovementPrecedingCollision',
                                  'PartyCategory', 'VehicleCount','ViolationCode','ViolationCodeDescription',
                                  'OtherAssociatedFactor'], axis=1)
    
    
    # Renaming the 'Name' column into 'CrashName' in order to merge the two datasets on 'CrashName' columns
    
    crash_data.rename( columns = ({'Name':'CrashName'}), inplace=True)
    
    # Doing the merge between crash_data and vehicle_data on 'CrashName' column

    data = pd.merge(vehicle_data, crash_data, on='CrashName', how='inner')

    
    #---------------------------- Cleaning and preprocessing data ----------------------------#
    
    # Renaming columns for a better comprehension of the features
    
    data.rename( columns = ({'Sobriety':'RoadUserConditions'}), inplace=True)
    data.rename( columns = ({'RoadwaySurface':'RoadConditions'}), inplace=True)
    data.rename( columns = ({'CrashDateTime':'CrashTime'}), inplace=True)
    
    
    # Quantizing 'Age' column
    
    data = data[data['Age']!=0].copy()
    bins_age = [0,15,20,30,40,50,60,70,80,100]
    labels_age = ['1-15','16-20','21-30','31-40','41-50','51-60','61-70','71-80','>80']
    data.loc[:,'Age'] = pd.cut(data['Age'],bins=bins_age,labels=labels_age, right=True)
    
    # Dropping missing values
    
    data = data[(data['RoadConditions']!='Unknown') & (data['Weather']!='Unknown') 
                 & (data['RoadUserConditions']!='Impairment Not Known') & (data['RoadUserConditions']!='Not Applicable')
                 & (data['PartyType']!='Unknown') & (data['Lighting']!='Unknown') & (data["Weather"] != "Other")]
    
    data = data.dropna()
        
    # Discretizing 'RoadUserConditions' column
    
    data = data.replace(to_replace = ['Had Been Drinking - Under Influence', 
                                      'Had Been Drinking - Impairment Unknown', 
                                      'Had Been Drinking - Not Under Influence'],
                        value = 'Had Been Drinking')
    
    data = data.replace(to_replace = ['Had Not Been Drinking'], value = 'Not Altered')
    
    # Preprocessing 'RoadConditions' column
    
    data = data.replace(to_replace = ['Slippery (Muddy Oily etc.)'], value = 'Slippery')
    
    # Preprocessing 'Lighting' column
    
    data = data.replace(to_replace = ['Dark - Street Light Not Functioning'], value = 'Dark - No Street Light')
    
    # Discretizing 'PartyType' column
    
    data = data.replace(to_replace = ['Bicycle', 'Pedestrian', 'Wheelchair', 'Skateboard', 'Other'], value = 'Vulnerable Users')
    data = data.replace(to_replace = ['Bus - Other', 'Bus - School'], value = 'Bus')
    data = data.replace(to_replace = ['Car With Trailer', 'Emergency Vehicle'], value = 'Car')
    data = data.replace(to_replace = ['Light Rail Vehicle'], value = 'Train')
    data = data.replace(to_replace = ['Motorcycle/Moped', 'Scooter Motorized'], value = 'Motorcycle')
    data = data.replace(to_replace = ['Semi Truck', 'Panel Truck'], value = 'Truck')
    
    # Quantizing 'CrashTime' column
    
    data['CrashTime'] = pd.to_datetime(data['CrashTime'], format='%m/%d/%Y %I:%M:%S %p').dt.hour
    data['CrashTime'] = data['CrashTime'].astype(str).replace(to_replace = ['0'], value = '24')
    bins_time = [0,6,12,17,21,24]
    labels_time = ['01-06','07-12','13-17','18-21','22-24']
    data.loc[:,'CrashTime'] = pd.cut(data['CrashTime'].astype(int),bins=bins_time,labels=labels_time, right=True)
    
    # Deriving the new feature 'Injuries', that takes the value 0 if the correspondent car crash causes minor injuries or if it doesn't 
    # cause injuries at all, 1 otherwise
    
    data['Injuries'] = np.where ((data['ModerateInjuries']>0) |
                                 (data['SevereInjuries']>0) | 
                                 (data['FatalInjuries']>0), 1, 0)
    
    data = data.drop(["CrashName","MinorInjuries","ModerateInjuries","SevereInjuries","FatalInjuries"],axis=1)
    

    # Saving the final dataset into a csv file
    
    project_cwd = pathlib.Path.cwd()
    data.to_csv(f'{project_cwd}/data.csv', index = False)
    
