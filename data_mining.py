
from math import sqrt

def sim_distance(prefs, person1, person2):

  si={}
  for item in prefs[person1]:
    if item in prefs[person2]:
      si[item] = 1

  if len(si) == 0:
    return 0

  sum_of_squares = sum([math.pow(prefs[person1][item]-prefs[person2][item],2) for item in prefs[person1] if item in prefs[person2]])

  return 1/(1+math.sqrt(sum_of_squares))

def sim_pearson(prefs,p1,p2):
  si={}
  for item in prefs[p1]:
    if item in prefs[p2]:
      si[item]=1

  n=len(si)

  if n==0:  
    return 1

  sum1=sum([prefs[p1][it] for it in si])
  sum2=sum([prefs[p2][it] for it in si])

  sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
  sum2Sq=sum([pow(prefs[p2][it],2) for it in si])

  pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])

  num=pSum-(sum1*sum2/n)
  den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
  if den==0: 
    return 0

  r=num/den

  return r

def topMatches(prefs, person, n=5, similarity=sim_distance):
  scores = [(sim_distance(prefs, person, other), other) for other in prefs if other!=person]

  scores.sort();
  scores.reverse();
  return scores[0:n]

def getRecommendations(prefs, person, similarity=sim_distance):
  totals={}
  simSums={}
  for other in prefs:
    if other==person:
      continue
    sim = similarity(prefs, person, other)
	
    if sim<=0:
      continue
    for item in prefs[other]:
      if item not in prefs[person] or prefs[person][item]==0:
        totals.setdefault(item, 0)
        totals[item] += prefs[other][item]*sim

        simSums.setdefault(item, 0)
        simSums[item] += sim
                                
    rankings=[(total/simSums[item], item) for item, total in totals.items()]
	
    rankings.sort()
    rankings.reverse()
    return rankings

def getPredictRankings(prefs,person,similarity=sim_pearson):
  totals={}
  simSums={}
  temp = {}
	
  for other in prefs:
    if other==person:
      continue
    sim = similarity(prefs, person, other)

    #if sim<=0:
    #  continue
    for item in prefs[other]:
      if item not in prefs[person] or prefs[person][item]==0:
      totals.setdefault(item, 0)
      totals[item] += prefs[other][item]*sim

      simSums.setdefault(item, 0)
      simSums[item] += sim

    #rankings=[(total/simSums[item], item) for item, total in totals.items()]
	
    #rankings.sort()
    #rankings.reverse()
    #return rankings
	
    for item,total in totals.items():
      if simSums[item] == 0:
        temp[item] = 3
        #print "all 333333333333333333333333"
      else:
        temp[item] = total/simSums[item]
        #print total/simSums[item]

    for item in prefs[person]:
      temp[item] = prefs[person][item]

    return temp

def calculateMAE(predict, result):
  import math
  total = 0
  counter = 0
	
  for reader in result:
    readers = result.get(reader)
      for book in readers:
        score = readers.get(book)
        # it doesn't work when the counter changes to 1116 (ignore and get 19943 totally), 19965
        if predict[reader].has_key("377"):
          total += abs(float(score)-float(predict[reader]["377"]))
          counter += 1
       else:
         print "no key"

    print "counter = ", counter
    # MAE = 0.80490266773, sounds bad, and 0.646000366786 when counter==100
    return float(total)/counter

import time
startTime = time.time()

critics = {}
predict = {}
result = {}

trainFile = open("80train.txt", "r")
try:
  for line in trainFile:
    items = line.split("\t")
  if critics.has_key(items[0]):
    critics[items[0]][items[1]] = float(items[2]) 
  else:
    critics[items[0]] = {items[1]:float(items[2])}
  #print critics
finally:
  trainFile.close()
        
testFile = open("test.txt", "r")
try:
  for line in testFile:
    items = line.split("\t")
  if result.has_key(items[0]):
    result[items[0]][items[1]] = float(items[2]) 
  else:
    result[items[0]] = {items[1]:float(items[2])}
  #print result
finally:
  testFile.close()

books = []
cnt = 0
for people in result:
  for book in result[people]:
    if book not in books:
      cnt += 1
      books.append(book)
#print "test number = ", cnt

for everybody in critics:
  predict[everybody] = getPredictRankings(critics, everybody, sim_pearson)

#print len(predict)

print "MAE : ", calculateMAE(predict, result)

endTime = time.time()

print "Total time : %f" % (endTime - startTime)
