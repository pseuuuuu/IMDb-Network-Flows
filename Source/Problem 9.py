########################################################
# EE232E SPRING 2017 PROJECT 2 
# PROBLEM 9
# AUTHOR: SILEI MA, HONGYANG LI, NIEN-JEN CHENG
########################################################

import re

print("(1/5)Actor and Actress Combine ... ", end='\r')
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


print("(2/5)Movie & Actor Dictionary Build Up ... ", end='\r')
movieDict={}
movNO={}
actorDict={}
actNO={}

actors = open('actors_movies_merged.txt', 'r')
movies = open('movie_genre.txt', 'r')

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
actors.close()
movies.close()


print("(3/5)Movie Rating & Actor Score Dictionary Build Up ... ", end='\r')
rating = open('movie_rating.txt','r')
RatMov={}
for line in rating.readlines():
    field = line.split('\t\t')
    field[0]=field[0].strip()
    RatMov[field[0]] = float(field[1].strip())

ScoAct={}
for act in actorDict:
    score = 0
    count = 0
    for i in range(1, len(actorDict[act])):
        movieID = actorDict[act][i]
        movie = movNO[movieID]
        if movie in RatMov:
            score = score + RatMov[movie]
            count = count +1
    if count == 0 :
        actsco = 0
    else:
        actsco = score/count
    ScoAct[act] = actsco    
print("Done!!")
print("Dictinary Finished!!")


print("(4/5)Begin Rating Prediction of the New Movies ... ")
#movieId: 894354 779751 763763
for movID in [894354,779751,763763]:
    score = 0        
    rookie = 0
    normal = 0
    star = 0
    for i in range(1,len(movieDict[movNO[movID]])):
        actID = movieDict[movNO[movID]][i]
        actscore = ScoAct[actNO[actID]]
        if actscore != 0:
            if actscore > 7:
                score = score + 10*actscore                    
                star = star + 1
            elif actscore <= 7 and actscore > 5.5:
                score = score + 3*actscore 
                normal = normal + 1
            else:
                score = score + actscore 
                rookie = rookie + 1
    av_score = score/(rookie + 3*normal + 10*star)
    print("The Predicted Rating of Movie: "+str(movNO[movID])+" is %f"%(av_score))
print("Done!!")


print("(5/5)Begin Graph Building ... ")
net = open('act_mov_net.txt','w')

for i in range(1, actorID):
    movie=actorDict[actNO[i]]
    for j in range(1, len(movie)):
        net.write('%d\t%d\n'%(i,movie[j]))
net.close()
print("Done!!")              
print("Graph Finished!!")

