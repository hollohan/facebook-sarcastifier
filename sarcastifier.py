'''
    This code will add sarcastic comments to facebook
    https://github.com/rekanize/facebook-sarcastifier
'''

import facebook
from sys import argv
from random import randint



# takes two filenames and returns two lists of lines in files
def files2lists(transfname, saysfname):
    transitions = []
    sayings = []
    try:
        with open(transfname, 'r') as transfile, open(saysfname, 'r') as saysfile:
            for line in transfile:
                transitions.append(line.rstrip())
            for line in saysfile:
                sayings.append(line.rstrip())
    except Exception as e:
        print ('error working with sayings.txt or transitions.txt - ' + str(e))
        exit()
    return (transitions, sayings)



# return phrase created by combining title, transitions, sayings
def returnphrase(title, translist, sayslist):
    transguess = randint(0, len(translist)-1)
    saysguess = randint(0, len(sayslist)-1)
    # take chunk from title
    title = title.split()
    titlen = len(title)
    titlesnip = ''
    for i in range(int(titlen/2),titlen):
        titlesnip += title[i] + ' '
    return '...' + titlesnip.rstrip().lower() + '... ' + translist[transguess] + ' ' + sayslist[saysguess]



# check post id to see if we've already posted, if not return false and store id in file
def alreadyposted(id):
    ids = []
    try:
        with open('ids.txt', 'r') as idsfile:
            for line in idsfile: ids.append(line.rstrip())
        if id in ids: return True
    except Exception as e:
        print('will need to create ids.txt - ' + str(e))
    with open('ids.txt', 'a') as idsfile:
        idsfile.write(id + '\n')
    return False



# loads file named in agrgv[2], checks each line in file
# against msg, returning True if match is found
def filterout(msg, filtersfilename):
    try:
        with open(filtersfilename) as filtersfile:
            for line in filtersfile:
                if line.rstrip() in msg: return True
        return False
    except Exception as e:
        print ('error working with filters file - ' + str(e))
        return True



# writes entry to log file
def appendlog(entry):
    with open('comment.log', 'a') as logfile:
        logfile.write(entry + '\n')
        
        

# takes config filename and returns 1st and 2nd line as tuple
def loadconfig(filename):
    u = ''
    atoken = ''
    try:
        i = 0
        with open(filename, 'r') as accesstokenfile:
            for line in accesstokenfile:
                if i==0: u = line.rstrip()
                if i==1: at = line.rstrip()
                i += 1
    except Exception as e:
        print ('error working with access token file - ' + str(e))
        exit()
    
    
    return (u, at)



# check args
if len(argv)<2:
    print ('not enough args')

# setup variables
user, accesstoken = loadconfig(argv[1])
(translist, sayslist) = files2lists('transitions.txt', 'sayings.txt')

# get user's posts
try:
    graph = facebook.GraphAPI(accesstoken)
    oot = graph.get_connections(user, 'posts')
except Exception as e:
    print ('issue with user id or access token - ' + str(e))
    exit()


# loads/checks all posts, if a post id is found
# that is not in ids.txt then put comment and exit
for thing in oot['data']:
    msg = thing['message'].rstrip()
    id = thing['id'].rstrip()

    # skip to next if already posted or in filter file
    if alreadyposted(id): continue
    if len(argv) == 3:
        if filterout(msg, argv[2]): continue

    # create phrase
    phrase = returnphrase(str(msg), translist, sayslist)

    ''' uncomment this for troubleshooting
    try:
        print('-adding comment-' + phrase)
        appendlog(phrase)
    except:
        print(b'\t\tsomething skipped - ' + msg.encode('utf-8'))
        appendlog('\t\tsomething skipped - ')
    '''


    try:
        graph.put_comment(id, phrase)
    except e as Exception:
        print ('error while attempting to post comment = ' + str(e))

    break