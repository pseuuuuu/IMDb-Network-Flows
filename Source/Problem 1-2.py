########################################################
# EE232E SPRING 2017 PROJECT 2 
# PROBLEM 1 2
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


print("(2/4)Actors Parsing ... ", end='\r') 
actors_m = open('actors_movies_merged.txt','r')
actors = open('actors_movies.txt','w')

line_count = 0 
for line in actors_m.readlines():
    if(line.count('\t\t')>4):
        actors.write(str(line))
    line_count+=1

actors_m.close()
actors.close()
print("Done!!")


print("(3/4)Movie & Actor Dictionary Build Up ... ", end='\r')
movieDict={}
movNO={}
actorDict={}
actNO={}

actors = open('actors_movies.txt', 'r')
movies = open('movie_genre.txt', 'r')

movieID=1
for line in movies.readlines():
    field = line.split('\t\t')
    field[0] = field[0].strip().replace('(as','\t\t').replace('(voice','\t\t').replace('(un','\t\t').replace('(arch','\t\t').replace('(attach','\t\t').replace('(add','\t\t').replace('(ru','\t\t').replace('{{','\t\t').split('\t\t')[0].strip()
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
            field[i]=movie[:end+6]

        field[i] = field[i].strip().replace('(as','\t\t').replace('(voice','\t\t').replace('(un','\t\t').replace('(arch','\t\t').replace('(attach','\t\t').replace('(add','\t\t').replace('(ru','\t\t').replace('{{','\t\t').split('\t\t')[0].strip()    
        if field[i] in movieDict:
            movieDict[field[i].strip()].append(actorID)
        else:
            movieDict[field[i].strip()]=[len(movieDict)+1]
            movNO[len(movieDict)]=field[i].strip()
            movieID+=1
            movieDict[field[i].strip()].append(actorID)
        actorDict[field[0].strip()].append(movieDict[field[i].strip()][0])        
    actorID+=1
print("Done!!")

actors.close()
movies.close()
print("Dictinary Finished!!")

'''
#moac = open('mov_act.txt', 'w')
#acmo = open('act_mov.txt', 'w')
for i in range(1, movieID):
    moac.write(' '.join(str(e) for e in movieDict[movNO[i]]))
    moac.write('\n')

for i in range(1, actorID):
    acmo.write(' '.join(str(e) for e in actorDict[actNO[i]]))
    acmo.write('\n')
#moac.close()
#acmo.close() 
'''
'''
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
'''

print("(4/4)Begin Graph Building ... ", end='\r')
net = open('act_directed_net.txt','w')

for i in range(1, actorID):
    w={}
    y={}
    movie=actorDict[actNO[i]]
    for j in range(1, len(movie)):
        coact=movieDict[movNO[movie[j]]]
        for k in range(1, len(coact)):
            w[coact[k]]=0
            y[coact[k]]=0
    for j in range(1, len(movie)):
        coact=movieDict[movNO[movie[j]]]
        for k in range(1, len(coact)):
            w[coact[k]]+=1
    for j in range(1, len(movie)):
        coact=movieDict[movNO[movie[j]]]
        for k in range(1, len(coact)):
            if(i!=coact[k] and y[coact[k]]==0):
                net.write('%d\t%d\t%f\n'%(i, coact[k], w[coact[k]]/(len(movie)-1)))
                y[coact[k]]=1
net.close()
print("Done!!")              
print("Graph Finished!!")
