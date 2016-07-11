# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 19:48:32 2016

functionality test
@author: Jimmy
"""

import json
import datetime
import statistics
import time

f=open('venmo-trans.txt','r') #load input
filelist=[];
for lines in f: #save input file results
    filelist.append(lines)
f.close() #close input file

#timeinput="2016-04-07T03:33:19Z" #test time
#dateobj_input=datetime.datetime.strptime(timeinput,'%Y-%m-%dT%H:%M:%SZ')#convert to datetime object

count0=0;
peopledict={} #initilize dictionary for assigning numbers to people
edgelist=[] #initialize graph storage (in edge list form)
newline='\n' #in case text file contains \n
resultslist=[] #store list of medians here
for i in range(len(filelist)): #assume each loop is one transaction: calculate using the last 60 seconds   
    lineouter=filelist[i]
    parsed_json_inp=json.loads(lineouter)
    dateobj_input=datetime.datetime.strptime(parsed_json_inp['created_time'],'%Y-%m-%dT%H:%M:%SZ')
    t1=time.time()    
    for j in range(i+1): #loop through every transaction prior to current
        line=filelist[j]
        if line !=newline: #in case text file contains \n
            parsed_json=json.loads(line) #convert json entry to dictionary
            
            #is within window?
            dateobj=datetime.datetime.strptime(parsed_json['created_time'],'%Y-%m-%dT%H:%M:%SZ')
            timedelta_test=dateobj-dateobj_input #time between target and 
            
            if (datetime.timedelta(seconds=60)>timedelta_test) and (timedelta_test>=datetime.timedelta(seconds=0)): #is value in the valid time window?
            
                if (parsed_json['actor'] in peopledict.keys())==False: #check if number is assigned to a person
                    nkeys=len(peopledict.keys()) #could also increment everytime an entry is added
                    peopledict[parsed_json['actor']]=nkeys+1 #add new entry from dictionary
                entry_actor=peopledict[parsed_json['actor']] #save actor from from transaction
                
                if (parsed_json['target'] in peopledict.keys())==False: #check if number is assigned to a person
                    nkeys=len(peopledict.keys()) #could also increment everytime an entry is added
                    peopledict[parsed_json['target']]=nkeys+1 #add new entry in dictionary
                entry_target=peopledict[parsed_json['target']] #save target from transaction
                
                edgelist.append([min(entry_actor,entry_target),max(entry_actor,entry_target)])#construct graph in edge list representation
        
    nodelist=set(val for sublist in edgelist for val in sublist) #flatten edge list and remove duplicates
        #count connections to each node
    t2=time.time()
    
    print(t2-t1)
    vertslist=[]
    edgelist=sorted(edgelist) #sort to help check for duplicates
    for i in nodelist: #loop through list of unique users
        count=0
        for j in range(len(edgelist)): #loop through transactions
            if j>0 and (edgelist[j]!=edgelist[j-1]): #check if duplicate
                if i in edgelist[j]: #check if user in question is involved in a transaction
                    count=count+1 #increment edge count
            elif j==0:
                if i in edgelist[j]:
                    count=count+1
        vertslist.append(count) #store count total
    roll_med_degree=round(statistics.median(vertslist),2) #calculate median
    count0=count0+1;
    print(count0)
    resultslist.append(roll_med_degree) #store valye
    
    
f=open('https://github.com/jmtwomey/JMTcodechall/insight_testsuite/tests/your-own-test/output.txt','w')
for i in resultslist:
    f.write(str(i)+'/n')
f.close()  
    
    
# graph visualization    
#import networkx as nx
#import matplotlib.pyplot as plt
#    #invert people dictionary to make edge labels
#    
#    peopledict_inv={peopledict[k] : k for k in peopledict}
#    nodelist_people=[peopledict_inv[x] for x in nodelist]#convert numbers to names
#    #edgelist_people=[peopledict_inv[x] for y in x for x in edgelist]#convert numbers to names
#    edgelist_people=[]
#    for i in edgelist:
#        edgelist_people.append([peopledict_inv[i[0]],peopledict_inv[i[1]]])
#    
#    def edgegraph(edgeinp,mapping):
#        #verts=set([n1 for n1, n2 in edgeinp]+[n2 for n1, n2 in edgeinp])
#        vertplot=nx.Graph()
#        vertplot.add_nodes_from(nodelist_people)
#        for edge in edgeinp:
#            vertplot.add_edge(edge[0],edge[1])
#        point=nx.shell_layout(vertplot)
#        nx.draw(vertplot,point)
#        #vertplot=nx.path_graph(len(nodelist_people))
#        #vertplot=nx.relabel_nodes(vertplot,mapping, copy=False)
#        plt.show()
#    edgegraph(edgelist_people,peopledict_inv)
            
