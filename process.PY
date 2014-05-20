import os, glob, json, random
from collections import Counter
'''
Only extract useful numeric data and save it to filename+'data.json'
Example: 
analyseData ('cocacola40796308305.json')

'''

def analyseData (filename):
    f=open(filename,'r')

    rawdata= json.load(f)

    data_list=[]

    for data in rawdata:
        data_dict={}
        data_dict['post_id']=data['post_id']
        data_dict['num_of_post_likes']=data['num_of_post_likes']
        data_dict['num_of_comments']=data['num_of_comments']       
        data_dict['num_of_shares']=data['num_of_shares']

        data_dict['comments']=[]
        for comment in data['comments']:
            comment_list=[]
            comment_list.append(comment[0])
            comment_list.append(comment[1])
            comment_list.append(comment[2])
            data_dict['comments'].append(comment_list)

        data_list.append(data_dict)

        fpath , fname = os.path.split( filename)
        fname=fname.split(r'.')[0]        
        dataFileName=fname+'data.json'
    json.dump(data_list, open(dataFileName, 'w')) 


'''
keep fb_ids of comments for each post and save it to fname+'preprocess.json'
Example: 
preprocessData ('cocacola40796308305')

'''
def preprocessData (fname):
    filename=fname+'data.json'
    f=open(filename,'r')

    rawdata= json.load(f)
    data_list=[]

    for data in rawdata:
        data_dict={}
        data_dict['post_id']=data['post_id']
        data_dict['num_of_post_likes']=data['num_of_post_likes']
        data_dict['num_of_comments']=data['num_of_comments']      
        data_dict['num_of_shares']=data['num_of_shares']

        data_dict['comments_fb_id']=[]     
        for comment in data['comments']:

            data_dict['comments_fb_id'].append(comment[1])           

        data_list.append(data_dict)
        preprocessFileName=fname+'preprocess.json'
    json.dump(data_list, open(preprocessFileName, 'w')) 



'''
keep fb_ids of comments for each post and save it to './post-comment/fname_threshold.txt'
Example: 
combineData ('cocacola40796308305')

'''
def combineData (fname, threshold):
    filename1=fname+'data.json'
    filename2=fname+'preprocess.json'

    f=open(filename1,'r')

    rawdata= json.load(f)
    data_list=[]
    data_list.append(len(rawdata))

    for data in rawdata:
        data_dict={}
        data_dict['post_id']=data['post_id']
        data_dict['num_of_post_likes']=data['num_of_post_likes']
        data_dict['num_of_comments']=data['num_of_comments']      
        data_dict['num_of_shares']=data['num_of_shares']
        data_list.append(data_dict)
    f.close()

    f=open(filename2,'r')

    rawdata= json.load(f)

    tail =len(rawdata)-1
    for data in rawdata:
        bottom=rawdata[tail]
        del rawdata[tail]
        # eliminate processed data
        head=0
        for data in rawdata:
            data_dict={}
            intersection_len=len(set(bottom['comments_fb_id']).intersection(set(data['comments_fb_id'])))


            if intersection_len>threshold:

                line_dict={}
                line_dict['tail']=tail
                line_dict['head']=head
                line_dict['num']=intersection_len
                data_list.append(line_dict)


            head=head+1

        tail =len(rawdata)-1
    outputFilePath='./post-comment/'+fname+'_'+str(threshold)+'.txt'
       
    json.dump(data_list, open(outputFilePath, 'w')) 


def main ():
    # manually set threshold 
    threshold_list=[10, 30, 50]
    fileList=glob.glob("./jsonData/*.json")
    for filename in fileList:
        # print filename    
        analyseData (filename)
        fpath , fname = os.path.split( filename)
        fname=fname.split(r'.')[0]
        # print fname

        preprocessData (fname)

        for threshold in threshold_list:
            combineData(fname, threshold)

main()





