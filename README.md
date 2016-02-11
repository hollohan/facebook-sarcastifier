
#Facebook Sarcastifier

This program will post a sarcastic comment on a Facebook friends post.

###Requirements:
	- the Facebook friends user id (http://findmyfbid.com)
	- a Facebook user access token (http://developers.facebook.com)

###Usage:
	'python ./sarcastifier.py <config file> [filters file]'

###Config File:
	This file must contain two lines of text in this order:
		1. Facebook friends user id
		2. Facebook user access token

###Filters File:
	Each post will be check against every line in this file.  If a match 
	is found, then that post will be disregarded.

###Good to Know:
	- This program will create a file called 'ids.txt'.  This file keeps 
		track of which posts we've already commented.  If a post is already 
		on the list then we will not add a comment.
	- If parts of the code are uncommented then this program may also create 
		a file called 'comment.log'.  This file is used to for 
		troubleshooting.  If enabled, each phrase will be logged in 
		this file.