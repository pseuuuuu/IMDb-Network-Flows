########################################################
# EE232E SPRING 2017 PROJECT 2 
# PROBLEM 5
# AUTHOR: SILEI MA, HONGYANG LI, NIEN-JEN CHENG
########################################################


print("(1/2)Genre Dictionary Build Up ... ", end='\r')
movie = open('mov_list.txt','r')
genre = open('movie_genre.txt','r')
mov_gen = open('mov_gen_list.txt','w')
genDict={}
for line in genre.readlines():
    field = line.split('\t\t')
    field[0] = field[0].strip()
    field[1] = field[1].strip()
    genDict[field[0]]=field[1]
print("Done!!")    


print("(2/2)Writing Genre List ... ", end='\r')
for mov in movie.readlines():
    mov = mov.strip()
    if(mov in genDict):
        mov_gen.write(str(genDict[mov]))
        mov_gen.write('\n')
    else:
        mov_gen.write('Null\n')
      
movie.close()
genre.close()
mov_gen.close() 
print("Done!!")
