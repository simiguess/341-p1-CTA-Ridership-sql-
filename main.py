#
# header comment! Overview, name, etc.
#

import sqlite3
import numpy as np
import matplotlib.pyplot as plt


##################################################################  
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
  # basic queries to get generic stats
    dbCursor = dbConn.cursor()
    
    print("General stats:")
    
    dbCursor.execute("Select count(*) From Stations;")
    row = dbCursor.fetchone();
    print("  # of stations:", f"{row[0]:,}")
  
    dbCursor.execute("Select count(*) From Stops;")
    row = dbCursor.fetchone();
    print("  # of stops:", f"{row[0]:,}")

    dbCursor.execute("Select count(*) From Ridership;")
    row = dbCursor.fetchone();
    print("  # of ride entries:", f"{row[0]:,}")
  
    dbCursor.execute(" Select Substring ((min(Ride_Date)), 0, 11), Substring ((max(Ride_Date)), 0, 11) from Ridership ; ")
    row = dbCursor.fetchone();
    print("  date range:", row[0] ,"-", row[1]  )
  
    dbCursor.execute("select sum(Num_Riders) from Ridership; ")
    total = dbCursor.fetchone();
    print("  Total ridership:", f"{total[0]:,}")

    dbCursor.execute("    Select sum(Num_Riders) from Ridership where Type_of_Day = 'W'")
    weekday = dbCursor.fetchone(); 
    print("  Weekday ridership:", f"{weekday[0]:,}",f'({weekday[0]/total[0]*100:.2f}%)')   

    dbCursor.execute("   Select sum(Num_Riders) from Ridership where Type_of_Day = 'A'")
    saturday = dbCursor.fetchone();
    print("  Saturday ridership:", f"{saturday[0]:,}", f'({saturday[0]/total[0]*100:.2f}%)')

    dbCursor.execute(" Select sum(Num_Riders) from Ridership where Type_of_Day = 'U'")
    sholiday = dbCursor.fetchone();
    print("  Sunday/holiday ridership:", f"{sholiday[0]:,}", f'({sholiday[0]/total[0]*100:.2f}%)')
  
    dbCursor.close()

##################################################################  
#
# main
#
def func_1(dbConn):
 
  dbCursor = dbConn.cursor()
  print()
  inputf1= input("Enter partial station name (wildcards _ and %): ")
  sql1 = """ Select Station_Id, Station_Name 
  from Stations
  where Station_Name like ?
  order by Station_Name asc"""
  dbCursor.execute(sql1,[inputf1])
  answ1 = dbCursor.fetchall()
  # print( answ1[0])
  if len(answ1) == 0:
    print("**No stations found...")
    return None
  for row in answ1:
    print(row[0], ":", row[1])
  dbCursor.close()

def func_2(dbConn):

  dbCursor = dbConn.cursor()
  print("** ridership all stations **\n")
  
  dbCursor.execute("select sum(Num_Riders) from Ridership; ")
  total = dbCursor.fetchone();
  
  sql2 = """Select Stations.Station_Name,  sum(Ridership.Num_Riders)
  from Ridership join Stations
  ON Ridership.Station_ID = Stations.Station_ID
  GROUP BY Ridership.Station_ID
  order by Stations.Station_Name asc"""
  dbCursor.execute(sql2)
  answ2 = dbCursor.fetchall()

  for row in answ2:
    print(row[0], ":",  f"{row[1]:,}",f'({row[1]/total[0]*100:.2f}%)')
  dbCursor.close()

def func_3(dbConn):

  dbCursor = dbConn.cursor()
  print("** top-10 stations **")
  
  dbCursor.execute("select sum(Num_Riders) from Ridership; ")
  total = dbCursor.fetchone();
  
  sql3 = """  SELECT Stations.Station_Name ,
SUM(Ridership.Num_Riders)
   FROM Ridership JOIN Stations
   ON Ridership.Station_ID = Stations.Station_ID
  GROUP BY Station_Name
   order by SUM(Num_Riders) desc
  limit 10"""
  dbCursor.execute(sql3)
  answ3 = dbCursor.fetchall()

  for row in answ3:
    print(row[0], ":",  f"{row[1]:,}",f'({row[1]/total[0]*100:.2f}%)')
  dbCursor.close()


def func_4(dbConn):

  dbCursor = dbConn.cursor()
  print("** least-10 stations **")
  
  dbCursor.execute("select sum(Num_Riders) from Ridership; ")
  total = dbCursor.fetchone();
  
  sql4 = """  SELECT   Stations.Station_Name ,
SUM(Ridership.Num_Riders)
   FROM Ridership JOIN Stations
   ON Ridership.Station_ID = Stations.Station_ID
  GROUP BY Station_Name
   order by SUM(Num_Riders) asc
  limit 10"""
  dbCursor.execute(sql4)
  answ4 = dbCursor.fetchall()

  for row in answ4:
    print(row[0], ":",  f"{row[1]:,}",f'({row[1]/total[0]*100:.2f}%)')
  dbCursor.close()

def func_5(dbConn):

  dbCursor = dbConn.cursor()
  print()
  input5 = input("Enter a line color (e.g. Red or Yellow): ")

  sql5 = """ Select Stops.Stop_Name, Stops.Direction, Stops.ADA
  from Stops join StopDetails on Stops.Stop_ID =  StopDetails.Stop_ID
  join Lines on StopDetails.Line_ID = Lines.Line_ID  
  where Lines.Color like  ? 
  order by Stops.Stop_Name asc"""
  dbCursor.execute(sql5, [input5])
  answ5 = dbCursor.fetchall()
  if len(answ5) == 0:
    print("**No such line...")
    return None
  for row in answ5:
    if row[2] == 1:
      print(row[0], ": direction =", row[1], "(accessible? yes)")
    else :
       print(row[0], ": direction =", row[1], "(accessible? no)")
    
  dbCursor.close()
  
  
def func_6(dbConn):

  dbCursor = dbConn.cursor()
  print("** ridership by month **")

  sql6 = """ SELECT strftime('%m', Ride_Date), sum(Num_Riders) FROM Ridership 
  GROUP BY strftime('%m', Ride_Date)
  
  """
  dbCursor.execute(sql6)
  answ6 = dbCursor.fetchall()

  for row in answ6:
      print( row[0], ":", f"{row[1]:,}")

  print()
  input52 = input("Plot? (y/n)")
  if input52 == 'y':
      x = []    # create 2 empty vectors/lists
      y = []
      labels = ['01','02','03','04','05','06','07','08','09','10','11','12']
      month = 1 
      for row in answ6: # append each (x, y) coordinate that you want to plot x.append(...)
         x.append(month)
         y.append(row[1])
         month = month+1
        
      plt.xlabel("month")
      plt.ylabel("number of riders(x*10^8)")
      plt.title("monthly ridership")
      plt.plot(x, y)
      plt.xticks(x, labels)
      plt.show(block = False)

      
    
  else : 
    mman = 3
  dbCursor.close()
  
  

def func_7(dbConn):

  dbCursor = dbConn.cursor()
  print("** ridership by year **")

  sql7 = """ 
  SELECT strftime('%Y', Ride_Date) As Year,SUM(Num_Riders)
  from Ridership
  group by Year
  order by Year asc
  
  """
  dbCursor.execute(sql7)
  answ7 = dbCursor.fetchall()

  for row in answ7:
      print( row[0], ":", f"{row[1]:,}")

  print()
  input52 = input("Plot? (y/n)")
  if input52 == 'y':
      x = []    # create 2 empty vectors/lists
      y = []
      labels = ['01','02','03','04','05','06','07','08','09','10','11','12', '13', '14','15','16','17','18','19','20','21' ]
      month = 1 
    
      for row in answ7: # append each (x, y) coordinate that you want to plot x.append(...)
         x.append(month)
         y.append(row[1])
         month = month+1
        
      plt.xlabel("year")
      plt.ylabel("number of riders(x*10^8)")
      plt.title("yearly ridership")
      plt.plot(x, y)
      plt.xticks(x, labels)
      plt.show(block = False)

      
    
  else : 
    mman = 3
  dbCursor.close()
  
def func_8(dbConn):
  dbCursor = dbConn.cursor()
  print()
  input1= input("Year to compare against? ")
  print()
  input2= input("Enter station 1 (wildcards _ and %): ")
  sql1 = """ SELECT Stations.Station_ID, Stations.Station_Name, Substring (Ridership.Ride_Date, 0, 11), Ridership.Num_Riders
  from Ridership JOIN Stations ON Ridership.Station_ID = Stations.Station_ID
  Where strftime('%Y', Ridership.Ride_Date) like ? AND Stations.Station_Name like ?
  order by Ridership.Ride_Date asc  """
  dbCursor.execute(sql1, [input1, input2])
  answ1 = dbCursor.fetchall()
  
  if len(answ1 )== 0:
     print(" **No station found...")
     return None
  if answ1[0][1]!= answ1[1][1]:
     print(" **Multiple stations found...")
     return None
 
  sql2 = """  SELECT Stations.Station_ID, Stations.Station_Name, Substring (Ridership.Ride_Date, 0, 11), Ridership.Num_Riders
  from Ridership JOIN  Stations ON Ridership.Station_ID = Stations.Station_ID
  Where strftime('%Y', Ridership.Ride_Date) like ? AND  Stations.Station_Name like ?
  order by Ridership.Ride_Date desc """
  dbCursor.execute(sql2, [input1, input2])
  answ2 = dbCursor.fetchall()
  if len(answ2 )== 0:
     print(" **No station found...")
     return None
  if answ2[0][1]!= answ2[1][1]:
    print(" **Multiple stations found...")
    return None
  print()
  input3= input("Enter station 2 (wildcards _ and %):")
  sql3 = """   SELECT Stations.Station_ID, Stations.Station_Name, Substring (Ridership.Ride_Date, 0, 11), Ridership.Num_Riders
  from Ridership JOIN Stations ON Ridership.Station_ID = Stations.Station_ID
  Where strftime('%Y', Ridership.Ride_Date) like ? AND  Stations.Station_Name like  ?
  order by Ridership.Ride_Date asc   """
  dbCursor.execute(sql3, [input1, input3])
  answ3 = dbCursor.fetchall()
  if len(answ3 )== 0:
     print(" **No station found...")
     return None
  if answ3[0][1]!= answ3[1][1]:
    print(" **Multiple stations found...")
    return None
  sql4 = """  SELECT Stations.Station_ID, Stations.Station_Name, Substring (Ridership.Ride_Date, 0, 11), Ridership.Num_Riders
  from Ridership JOIN  Stations ON Ridership.Station_ID = Stations.Station_ID
  Where strftime('%Y', Ridership.Ride_Date) like ? AND  Stations.Station_Name like ?
  order by Ridership.Ride_Date desc """ 
  dbCursor.execute(sql4, [input1, input3])
  answ4 = dbCursor.fetchall()
  if len(answ4)== 0:
     print(" **No station found...")
     return None
  if answ4[0][1]!= answ4[1][1]:
    print(" **Multiple stations found...")
    return None
  else:
    print(" Station 1:", answ1[0][0], answ1 [0][1])
    iterator1 = answ1[0:5]
    for row in iterator1:
        print( row[2], row[3])
   
    iterator2= answ2[0:5]
    iterator2.reverse()
    for row in iterator2:
        print( row[2],  row[3])
    print("Station 2:", answ3[0][0], answ3 [0][1])
    iterator3 = answ3[0:5]
    for row in iterator3:
        print( row[2], row[3])
   
    iterator4 = answ4[0:5]
    iterator4.reverse()
    for row in iterator4:
        print( row[2], row[3])
  print()
  input52 = input("Plot? (y/n) ")
  if input52 == 'y':
      x = []
      x2 = []
      y= []
      y2= []
      month = 1
      month2 = 1
      for row in answ1: # append each (x, y) coordinate that you want to 
          x.append(month)
          y.append(row[3])
          month = month+1
      for row in answ3: # append each (x, y) coordinate that you want to 
          x2.append(month2)
          y2.append(row[3])
          month2 = month2+1
      plt.xlabel("day")
      plt.ylabel("number of riders")
      message = f"riders each day of {input1}"
      plt.title(message)
      plt.plot(x, y, )
      plt.plot(x2, y2)
      plt.xticks( np.arange(0, 366, 50))
      plt.show(block = False)
  if input52 != 'y':
    mman = 3
  dbCursor.close()
  
def func_9(dbConn):

  dbCursor = dbConn.cursor()
  print()
  input5 = input("Enter a line color (e.g. Red or Yellow): ")
  input5.lower()
  sql5 = """ Select Stations.Station_Name,  Stops.Longitude, Stops.Latitude
  from Stops join StopDetails on Stops.Stop_ID =  StopDetails.Stop_ID
  join Lines on StopDetails.Line_ID = Lines.Line_ID  
  join Stations on Stations.Station_ID = Stops.Station_ID
  where Lines.Color like  ? 
  group by  Stops.Latitude
  order by Stations.Station_Name asc"""
  dbCursor.execute(sql5, [input5])
  answ5 = dbCursor.fetchall()
  if len(answ5) ==0:
     print("**No such line...")
     return None
  for row in answ5:
      
      print(row[0], ": ("+ str(row[2]) +", "+ str(row[1])+")") 

  print()
  input52 = input("Plot? (y/n) ")
 
  if input52 == 'y':


     #
    # populate x and y lists with (x, y) coordinates --- note that longitude # are the X values and latitude are the Y values
    #
    x = []
    y = []

    
    for row in answ5: # append each (x, y) coordinate that you want to 
        x.append(row[1])
        y.append(row[2])
     
  
    image = plt.imread("chicago.png")
    xydims = [-87.9277, -87.5569, 41.7012, 42.0868] # area covered by the map: 
    plt.imshow(image, extent=xydims)
    plt.title(input5 + " line")

    #
    # color is the value input by user, we can use that to plot the
    # figure *except* we need to map Purple-Express to Purple: #
    if (input5.lower() == "purple-express"):
              input5="Purple"  # color="#800080"
    plt.plot(x, y, "o", c=input5)
    #
    # annotate each (x, y) coordinate with its station name: #
    for row in answ5:
      plt.annotate(row[0], (row[1], row[2])) 
    plt.xlim([-87.9277, -87.5569])
    plt.ylim([41.7012, 42.0868])
    plt.show(block = False)
  
  
   
    
  if input52 != 'y':
    mman = 3


      
  dbCursor.close()

print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

print_stats(dbConn) 


while  True:
  print()
  print("Please enter a command (1-9, x to exit): ", end = '')
  input1 = input()
  if input1 == "1" :
    func_1(dbConn )
  elif input1 == "2" :
    func_2(dbConn )
  elif input1 == "3" :
    func_3(dbConn )
  elif input1 == "4" :
    func_4(dbConn )
  elif input1 == "5" :
    func_5(dbConn )
  elif input1 == "6" :
    func_6(dbConn )
  elif input1 == "7" :
    func_7(dbConn )
  elif input1 == "8" :
    func_8(dbConn )
  elif input1 == "9" :
    func_9(dbConn )
  elif input1 == "x" :
    break
  else :
    print("**Error, unknown command, try again...")

dbConn.close()
#
# done
#
