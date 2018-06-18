import sys
import os
class ting:
	wrd=''
	spamcnt=0
	count=0
	smle=0.0
	xhmle=0.0
def mle(x,wordbank):
	#x.smle=float(x.count)/(float(x.spamcnt)+float(len(wordbank)))
	x.smle=float(x.spamcnt)/float(x.count)
	x.hmle=float(x.count-x.spamcnt)/float(x.count)
	#x.hmle=float(x.count)/(float(x.count-x.spamcnt)+float(len(wordbank)))

path=sys.argv[1]
slash="\\"
filelist = os.listdir(path)

wordbank=[]
for i in filelist:
    if i.endswith(".txt"):
        with open(path+ slash+ i, 'r') as f:
			print f.name
			for line in f:
				parts=line.strip().split(" ")
				for word in parts:
					if(len(word)<=2 or word.isdigit()):
						continue
					if(not any(x.wrd==word for x in wordbank)):
						temp=ting()
						temp.wrd=word
						if(i.endswith(".spam.txt")):
							temp.spamcnt+=1
							temp.count+=1
						else:
							temp.count+=1
						wordbank.append(temp)
					else:
						for x in wordbank:
							if(x.wrd==word):
								if(i.endswith(".spam.txt")):
									x.spamcnt+=1
									x.count+=1
								else:
									x.count+=1

for w in wordbank:
	mle(w,wordbank)
out=open("out.txt",'w')
for w in wordbank:
	if(w.count>2):
		#word,spamCount,totalcount,(spamCount/totalcount),(totalcount-spamCount/totalcount)
		out.write(w.wrd)
		out.write(",")
		out.write(str(w.spamcnt))
		out.write(",")
		out.write(str(w.count))
		out.write(",")
		out.write(str(w.smle))
		out.write(",")
		out.write(str(w.hmle))
		out.write("\n")
		#print("%s,%d,%d,%f,%f" %(w.wrd,w.spamcnt,w.count,w.smle,w.hmle))
out.close()
	