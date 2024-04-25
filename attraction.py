import os
import pandas as pd
import sqlite3

from Utilities.DBUtilities import *

class Attraction:
  def __init__(self, name, openingHours, ticketPrice, capacityLimit):
    self.name = name
    self.openingHours = openingHours
    self.ticketPrice = ticketPrice
    self.capacityLimit = capacityLimit

  def AddAttraction(self):
    connection = DBUtils.InitializeDB()
    cursor = connection.cursor()
    try:
      cursor.execute('''
      INSERT INTO attraction 
      (attraction_name, attraction_openinghours, attraction_ticketprice, attraction_capacity) 
      VALUES (?, ?, ?, ?)
      ''', (self.name, str(self.openingHours), self.ticketPrice, self.capacityLimit))
      connection.commit()
    except sqlite3.IntegrityError:
        print(f"Attraction with name '{self.name}' already exists.")
    connection.close() 

  def GetAllAttractions():
    connection = DBUtils.InitializeDB()
    cursor = connection.cursor()
    cursor.execute('''
    SELECT a.attraction_id, a.attraction_name, a.attraction_openinghours, a.attraction_ticketprice, a.attraction_capacity,
    GROUP_CONCAT(f.feedback_content) AS feedback_list
    FROM attraction AS a
    LEFT JOIN feedback AS f ON f.attraction_id = a.attraction_id
    GROUP BY a.attraction_id, a.attraction_name, a.attraction_openinghours, a.attraction_ticketprice
    ORDER BY a.attraction_id ASC
    ''')
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    for i in range(len(rows)):
      rows[i] = list(rows[i])
      if rows[i][-1]:
        rows[i][-1] = rows[i][-1].split(',')
    return rows
  
  def SortAttractions(attractions, sortType):
    # Insertion Sorting
    try:
      if attractions:
        if sortType:
          if sortType == 'Ticket Price':
            for i in range(1, len(attractions)):
              key = attractions[i]
              j = i-1
              while j >= 0 and key[3] < attractions[j][3]:
                attractions[j + 1] = attractions[j]
                j -= 1
              attractions[j + 1] = key
            return attractions
          
          elif sortType == 'Capacity':
            for i in range(1, len(attractions)):
              key = attractions[i]
              j = i-1
              while j >= 0 and key[4] < attractions[j][4]:
                attractions[j + 1] = attractions[j]
                j -= 1
              attractions[j + 1] = key
            return attractions
          
        else:
          return attractions
      return []
    except Exception as e:
      return []
  
  def AddFeedback(attractionName, feedBack):
    connection = DBUtils.InitializeDB()
    cursor = connection.cursor()
    try:
      cursor.execute('''
      INSERT INTO feedback
      (feedback_content, attraction_id)
      VALUES (?, (SELECT DISTINCT attraction_id FROM attraction WHERE attraction_name = ?))
      ''', (feedBack, attractionName))
      connection.commit()
    except sqlite3.IntegrityError:
        print(f"Unable to add feedback to {attractionName}")
    connection.close() 

  def GetAllAttractionNames():
    connection = DBUtils.InitializeDB()
    cursor = connection.cursor()
    try:
      cursor.execute('''
      SELECT attraction_name
      FROM attraction
      ''')
      rows = cursor.fetchall()
      returnedTuple = tuple([i[0] for i in rows])
      connection.commit()
    except sqlite3.IntegrityError:
        print(f"Unable to get attraction names")
    connection.close() 
    return returnedTuple
        

if __name__ == '__main__':
  # a = Attraction("Mall of Egypt", "8-00", 100, 4000)
  # a.AddAttraction()
  # Attraction.AddFeedback('Mall of Egypt', 'Very fun experience!')
  # print(Attraction.GetAllAttractions())
  print(Attraction.SortAttractions(Attraction.GetAllAttractions(), 'Ticket Price'))
  # print(Attraction.SortAttractions(Attraction.GetAllAttractions(), 'Capacity'))
  # print(Attraction.GetAllAttractionNames())