########################################################
# EE232E SPRING 2017 PROJECT 2 
# PROBLEM 4
# AUTHOR: SILEI MA, HONGYANG LI, NIEN-JEN CHENG
########################################################

import re

print("(1/4)Actor and Actress Combine ... ", end='\r')
actor = open('actor_movies.txt','r')
actress = open('actress_movies.txt','r')
actors_m = open('actors_movies_merged.txt','w')

actor_n_actress=0
for line in actor.readlines():
    actors_m.write(str(line))
    actor_n_actress+=1
for line in actress.readlines():
    actors_m.write(str(line))
    actor_n_actress+=1

actor.close()
actress.close()
actors_m.close()    
print("Done!!")

'''
print("(2/4)Actors Parsing ... ", end='\r') 
actors_m = open('actors_movies_merged.txt','r')
actors = open('actors_movies.txt','w')

line_count = 0 
for line in actors_m.readlines():
    if(line.count('\t\t')>5):
        actors.write(str(line))
    line_count+=1

actors_m.close()
actors.close()
print("Done!!")
'''

print("(3/4)Movie & Actor Dictionary Build Up ... ", end='\r')
movieDict={}
movNO={}
actorDict={}
actNO={}

actors = open('actors_movies_merged.txt', 'r')
movies = open('movie_genre.txt', 'r')
#moac = open('mov_act.txt', 'w')
#acmo = open('act_mov.txt', 'w')

movieID=1
for line in movies.readlines():
    field = line.split('\t\t')
    field[0]=field[0].strip().replace(')  (',')\t\t').replace(') (',')\t\t').replace('{{','\t\t').replace(')\t(',')\t\t').split('\t\t')[0].strip()
    movieDict[field[0].strip()] = [movieID]
    movNO[movieID] = field[0].strip()
    movieID+=1

actorID=1
for line in actors.readlines():
    field = line.split('\t\t')
    actorDict[field[0].strip()] = [actorID]
    actNO[actorID] = field[0].strip()
    for i in range(1, len(field)):
        movie = field[i].strip()
        year = re.search(r'\(\d\d\d\d\)|\(\?\?\?\?\)',movie)
        if year:
            end=movie.find(year.group())
            field[i]=movie[:end+11]

        field[i]=field[i].strip().replace(')  (',')\t\t').replace(') (',')\t\t').replace('{{','\t\t').replace(')\t(',')\t\t').split('\t\t')[0].strip()
        if field[i].strip() in movieDict:
            movieDict[field[i].strip()].append(actorID)
        else:
            movieDict[field[i].strip()]=[len(movieDict)+1]
            movNO[len(movieDict)]=field[i].strip()
            movieID+=1
            movieDict[field[i].strip()].append(actorID)
        actorDict[field[0].strip()].append(movieDict[field[i].strip()][0])        
    actorID+=1
print("Done!!")

'''
for i in range(1, movieID):
    moac.write(' '.join(str(e) for e in movieDict[movNO[i]]))
    moac.write('\n')

for i in range(1, actorID):
    acmo.write(' '.join(str(e) for e in actorDict[actNO[i]]))
    acmo.write('\n')
'''

actors.close()
movies.close()
#moac.close()
#acmo.close()    
print("Dictinary Finished!!")


movlist=open("mov_list.txt",'w')
for i in range(1,movieID):
    movlist.write(str(movNO[i]))
    movlist.write('\n')
movlist.close()

actlist=open("act_list.txt",'w')
for i in range(1,actorID):
    actlist.write(str(actNO[i]))
    actlist.write('\n')
actlist.close()



print("(4/4)Begin Graph Building ... ")
net = open('mov_undirected_net.txt','w')

for i in range(1, movieID):
    w={}
    y={}
    leng={}
    actor=movieDict[movNO[i]]
    if(len(actor)>5):
        for j in range(1, len(actor)):
            comov=actorDict[actNO[actor[j]]]
            for k in range(1, len(comov)):
                w[comov[k]]=0
                y[comov[k]]=0
                leng[comov[k]]=len(movieDict[movNO[comov[k]]])-1
        for j in range(1, len(actor)):
            comov=actorDict[actNO[actor[j]]]
            for k in range(1, len(comov)):
                w[comov[k]]+=1
        for j in range(1, len(actor)):
            comov=actorDict[actNO[actor[j]]]
            for k in range(1, len(comov)):
                if(i<comov[k] and y[comov[k]]==0 and leng[comov[k]]>5):
                    net.write('%d\t%d\t%f\n'%(i, comov[k], w[comov[k]]/(len(movie)+leng[comov[k]]-w[comov[k]]-1)))
                    y[comov[k]]=1

net.close()
print("Done!!")              
print("Graph Finished!!")

