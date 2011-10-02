import re
import time
import random
import urllib2
import urllib
import copy
from xgoogle.BeautifulSoup import BeautifulSoup,BeautifulStoneSoup
from xgoogle.search import GoogleSearch




VIDEO_PREFIX = "/video/icefilms"

NAME = L('Title')

# make sure to replace artwork with what you want
# these filenames reference the example files in
# the Contents/Resources/ folder in the bundle
ART  = 'art-default.jpg'
PREFS_ICON = 'prefs.png'
ICEFILMS = 'logo.jpg'

ICEFILMS_URL = "http://www.icefilms.info/"
ICEFILMS_AJAX = ICEFILMS_URL+'membersonly/components/com_iceplayer/video.phpAjaxResp.php'
ICEFILMS_REFERRER = 'http://www.icefilms.info'
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

ACCOUNT_STATUS="NONE"

####################################################################################################

def Start():

    ## make this plugin show up in the 'Video' section
    ## in Plex. The L() function pulls the string out of the strings
    ## file in the Contents/Strings/ folder in the bundle
    ## see also:
    ##  http://dev.plexapp.com/docs/mod_Plugin.html
    ##  http://dev.plexapp.com/docs/Bundle.html#the-strings-directory
    Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, NAME, ICEFILMS, ART)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

    ## set some defaults so that you don't have to
    ## pass these parameters to these object types
    ## every single time
    ## see also:
    ##  http://dev.plexapp.com/docs/Objects.html
    MediaContainer.title1 = NAME
    MediaContainer.viewGroup = "InfoList"
    MediaContainer.art = R(ART)

    MediaContainer.userAgent = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-GB; rv:1.9.2.17) Gecko/20110420 Firefox/3.6.17"
    MediaContainer.userAgent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3"   
	
    DirectoryItem.thumb = R(ICEFILMS)
    VideoItem.thumb = R(ICEFILMS)
    
    HTTP.CacheTime = 2000000
    HTTP.Headers['Accept'] = 'text/plain,text/html,*/*;q=0.3'
    HTTP.Headers['Accept-Encoding'] = '*;q=0.1'
    HTTP.Headers['TE'] = 'trailers'
    HTTP.Headers['Connection'] = 'TE'
 
# see:
#  http://dev.plexapp.com/docs/Functions.html#ValidatePrefs
def ValidatePrefs():
    u = Prefs['username']
    p = Prefs['password']
    ## do some checks and return a
    ## message container
    if( u and p ):
	Authenticate()
        return MessageContainer(
            "Success",
            "User and password provided ok"
        )
    else:
        return MessageContainer(
            "Error",
            "You need to provide both a user and password"
        )

  


#### the rest of these are user created functions and
#### are not reserved by the plugin framework.
#### see: http://dev.plexapp.com/docs/Functions.html for
#### a list of reserved functions above

def Authenticate():
  #HTTP.ClearCookies()
  accountStatus="None"
  u = Prefs['username']
  p = Prefs['password']

  
  # Only when username and password are set
  if (u and p):
    
   try:
    
    credentials={"username":u,"password":p,"login":"1"}
    
    response = HTTP.Request('http://www.megaupload.com/?c=login',credentials)
    response = str(response)
    accountNameText = re.search("flashvars\.username = \"(.*?)\"", str(response)).group(1)
    welcomeText = re.search("flashvars\.welcometxt = \"(.*?)\"", str(response)).group(1)
    accountStatus =re.search("flashvars\.status = \"(.*?)\"", str(response)).group(1)
    if(accountNameText==u and welcomeText=='Welcome'):
	ACCOUNT_STATUS=accountStatus
    
      
   except:
      Dict['loggedIn']=False
      Log.Exception("Login Failed")

  return accountStatus

#
# Example main menu referenced in the Start() method
# for the 'Video' prefix handler
#

def VideoMainMenu():
    
    
    Authenticate()
    
    # Container acting sort of like a folder on
    # a file system containing other things like
    # "sub-folders", videos, music, etc
    # see:
    #  http://dev.plexapp.com/docs/Objects.html#MediaContainer
    dir = MediaContainer(viewGroup="InfoList",httpCookies=HTTP.GetCookiesForURL('http://www.megaupload.com/'))
    

    # see:
    #  http://dev.plexapp.com/docs/Objects.html#DirectoryItem
    #  http://dev.plexapp.com/docs/Objects.html#function-objects
    dir.Append(
        Function(
            DirectoryItem(
                 Movies,
                "Movies",
                subtitle="HD Movies",
                summary="Watch High Quality Movie in SD and HD formats. Your one stop shop for DVD and BluRay releases.",
                thumb=R(ICEFILMS),
                art=R(ART)
            )
        )
    )
    
    dir.Append(
        Function(
            DirectoryItem(
                TV,
                "TV Shows",
                subtitle="TV Shows & Episodes",
                summary="Collection of TV Shows and Episodes",
                thumb=R(ICEFILMS),
                art=R(ART)
            )
        )
    )
  
    a = ""
    # Part of the "search" example 
    # see also:
    #   http://dev.plexapp.com/docs/Objects.html#InputDirectoryItem
    dir.Append(
        Function(
            InputDirectoryItem(
                SearchResults,
                "Search title",
                "Search subtitle",
                summary="Search for a title using this feature",
                thumb=R(ICEFILMS),
                art=R(ART)
            )
        )
    )

  
    # Part of the "preferences" example 
    # see also:
    #  http://dev.plexapp.com/docs/Objects.html#PrefsItem
    #  http://dev.plexapp.com/docs/Functions.html#CreatePrefs
    #  http://dev.plexapp.com/docs/Functions.html#ValidatePrefs 
    dir.Append(
        PrefsItem(
            title="Preferences",
            subtile="Set your Megaupload Credentials here",
            summary="If you have an account at Megaupload, use this feature to store the credentials",
            thumb=R(PREFS_ICON)
        )
    )
	
	
    # ... and then return the container
    
    
    return dir
def TV(sender):
    dir = MediaContainer(viewGroup="InfoList",httpCookies=HTTP.GetCookiesForURL('http://www.megaupload.com/'))
    
    dir.Append(
     Function(
	 DirectoryItem(
	      AZList,
	     "A-Z List",
	     subtitle="Complete TV Collection",
	     summary="Watch High Quality TV Shows.",
	     thumb=R(ICEFILMS),
	     art=R(ART)
	 ),
	 mode="tv"
     )
    )
    
    dir.Append(
     Function(
	 DirectoryItem(
	      ShowMoviesAndTV,
	     "All TV Shows",
	     subtitle="Complete TV Show Collection",
	     summary="Watch High Quality TV Shows.",
	     thumb=R(ICEFILMS),
	     art=R(ART)
	 ),
	 HD="All",
	 mode="tv"
     )
    )
    
   
    
    return dir

def Movies(sender):
    dir = MediaContainer(viewGroup="InfoList",httpCookies=HTTP.GetCookiesForURL('http://www.megaupload.com/'))
    
    dir.Append(
     Function(
	 DirectoryItem(
	      AZList,
	     "A-Z List",
	     subtitle="Complete Movie Collection",
	     summary="Browse High Quality Movie in SD and HD formats. Your one stop shop for DVD and BluRay releases.",
	     thumb=R(ICEFILMS),
	     art=R(ART)
	 ),
	 mode="movies"
     )
    )
    
    dir.Append(
     Function(
	 DirectoryItem(
	      ShowMoviesAndTV,
	     "All Movies",
	     subtitle="Complete Movie Collection",
	     summary="Watch High Quality Movie in SD and HD formats. Your one stop shop for DVD and BluRay releases.",
	     thumb=R(ICEFILMS),
	     art=R(ART)
	 ),
	 HD="All",
	 mode="movies"
     )
    )
    
    
    
    dir.Append(
     Function(
	 DirectoryItem(
	      ShowMoviesAndTV,
	     "HD Movies",
	     subtitle="720p Movie Collection",
	     summary="Watch High Quality Movies in HD format. Your one stop shop for  BluRay releases.",
	     thumb=R(ICEFILMS),
	     art=R(ART)
	 ),
	 HD="HD",
	 mode="movies"
     )
    )
    
    return dir

def AZList(sender,mode):
    mc = MediaContainer( viewGroup = "/video/icefilms/TV" ,httpCookies=HTTP.GetCookiesForURL('http://www.megaupload.com/'))
    azList = ['#1234','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    
    
    func_name=""
    if(mode=="movies"):
	func_name=ShowAlphaListForMovies
    elif(mode=="tv"):
	func_name=ShowAlphaListForTV
    
    for value in azList:
	  mc.Append(
	    Function(
		DirectoryItem(
		    func_name,
		   value,
		   subtitle="Complete  Collection arranged alphabetically",
		   summary="Browse High Quality TV/Movie collection",
		   thumb=R(ICEFILMS),
		   art=R(ART)
		),
		alpha=value,
		mode=mode
	    )
	)
	  
    return mc


def ShowMoviesAndTV(sender,HD=None,mode=None):
    
    mc = MediaContainer( viewGroup = "/video/icefilms/TV" ,httpCookies=HTTP.GetCookiesForURL('http://www.megaupload.com/'))
    func_name=""
    
    if (HD =="HD" and mode=="movies"):
     func_name=Movies_HD
    elif (HD =="All" and mode=="movies"):
     func_name=Movies_All
    elif(mode=="tv"):
     func_name=TV_All
    
     
    
    mc.Append(
     Function(
	 DirectoryItem(
	      func_name,
	     "Popular",
	     subtitle="All Movies",
	     summary="List of most popular movies",
	     thumb=R(ICEFILMS),
	     art=R(ART)
	 ),
	mode="popular"
     )
    )
    
    mc.Append(
     Function(
	 DirectoryItem(
	      func_name,
	     "Highly Rated",
	     subtitle="All Movies",
	     summary="List of Highly Rated Movies",
	     thumb=R(ICEFILMS),
	     art=R(ART)
	 ),
	 mode='rating'
     )
    )
    
    mc.Append(
     Function(
	 DirectoryItem(
	      func_name,
	     "Latest Releases",
	     subtitle="All Movies",
	     summary="List of latest releases",
	     thumb=R(ICEFILMS),
	     art=R(ART)
	 ),
	 mode='release'
     )
    )
    
    mc.Append(
     Function(
	 DirectoryItem(
	      func_name,
	     "Recently Added",
	     subtitle="All Movies",
	     summary="List of recently added movies",
	     thumb=R(ICEFILMS),
	     art=R(ART)
	 ),
	 mode='added'
     )
    )
    
    return mc


def ShowAlphaListForMovies(sender,alpha=None,mode=None):

    ## you might want to try making me return a MediaContainer
    ## containing a list of DirectoryItems to see what happens =)
        
	
	mc = MediaContainer( viewGroup = "/video/icefilms/TV" ,httpCookies=HTTP.GetCookiesForURL('http://www.megaupload.com/'))
	
	if(alpha=='#1234') :
	    alpha='1'
	
	 
	tv_page = HTTP.Request( ICEFILMS_URL+"movies/a-z/"+ alpha )
	tv_page = str(tv_page)
	tv_matches = re.findall( "<a href=(/ip.php.*?)>(.*?)</a>", tv_page )
	
	
	#for tv_match in sorted( tv_matches , key=lambda tv_match: tv_match[1] ):
        for urlMatch,titleMatch in tv_matches:
	    title = titleMatch.replace( "&#x27;" , "'" )
	    url = urlMatch
	    mc.Append(
	    Function(
	    DirectoryItem(
	    Movie_Data,
	    title,
	    subtitle="",
	    summary=""
	    #,thumb=TV_thumb(url)
	    ),
	    title = title,
	    url = url
		)
	)


	return mc
def ShowAlphaListForTV(sender,alpha=None,mode=None):

    ## you might want to try making me return a MediaContainer
    ## containing a list of DirectoryItems to see what happens =)

	mc = MediaContainer( viewGroup = "/video/icefilms/TV" )
	
	
	tv_page = HTTP.Request( ICEFILMS_URL+ "tv/a-z/"+ alpha )
	tv_page = str(tv_page)
	tv_matches = re.findall( "<a href=(/tv/series/.*?)>(.*?)</a>", tv_page )
	
	#for tv_match in sorted( tv_matches , key=lambda tv_match: tv_match[1] ):

	for urlMatch,titleMatch in tv_matches:
		title = titleMatch.replace( "&#x27;" , "'" )
		url = urlMatch
		mc.Append(
			Function(
				DirectoryItem(
					TV_Episodes,
					title,
					subtitle="",
					summary=""
					#,thumb=TV_thumb(url)
				),
				title = title,
				url = url
			)
		)


	return mc
    

def Movies_All(sender,mode=None):

    ## you might want to try making me return a MediaContainer
    ## containing a list of DirectoryItems to see what happens =)
        
	
	mc = MediaContainer( viewGroup = "/video/icefilms/TV" ,httpCookies=HTTP.GetCookiesForURL('http://www.megaupload.com/'))
	
	
	tv_page = HTTP.Request( ICEFILMS_URL+"movies/"+ mode+"/1" )
	tv_page = str(tv_page)
	tv_matches = re.findall( "<a href=(/ip.php.*?)>(.*?)</a>", tv_page )
	
	
	#for tv_match in sorted( tv_matches , key=lambda tv_match: tv_match[1] ):

	for urlMatch,titleMatch in tv_matches:
	    title = titleMatch.replace( "&#x27;" , "'" )
	    url = urlMatch
	    mc.Append(
	    Function(
	    DirectoryItem(
	    Movie_Data,
	    title,
	    subtitle="",
	    summary=""
	    #,thumb=TV_thumb(url)
	    ),
	    title = title,
	    url = url
		)
	)


	return mc
    


def Movies_HD(sender,mode=None):

    ## you might want to try making me return a MediaContainer
    ## containing a list of DirectoryItems to see what happens =)
        
	mc = MediaContainer( viewGroup = "/video/icefilms/TV",httpCookies=HTTP.GetCookiesForURL('http://www.megaupload.com/') )
	
	
	tv_page = HTTP.Request( ICEFILMS_URL+"movies/" + mode + "/hd" )
	tv_page = str(tv_page)
	tv_matches = re.findall( "<a href=(/ip.php.*?)>(.*?)</a>", tv_page )
	
	
	#for tv_match in sorted( tv_matches , key=lambda tv_match: tv_match[1] ):

	for urlMatch,titleMatch in tv_matches:
	    title = titleMatch.replace( "&#x27;" , "'" )
	    url = urlMatch
	    mc.Append(
	    Function(
	    DirectoryItem(
	    Movie_Data,
	    title,
	    subtitle="",
	    summary=""
	    #,thumb=TV_thumb(url)
	    ),
	    title = title,
	    url = url,
	    HD = True
		)
	)


	return mc
    


def TV_All(sender,mode=None):

    ## you might want to try making me return a MediaContainer
    ## containing a list of DirectoryItems to see what happens =)

	mc = MediaContainer( viewGroup = "/video/icefilms/TV" )
	
	
	tv_page = HTTP.Request( ICEFILMS_URL+"tv/"+mode+"/1" )
	tv_page = str(tv_page)
	tv_matches = re.findall( "<a href=(/tv/series/.*?)>(.*?)</a>", tv_page )
	
	#for tv_match in sorted( tv_matches , key=lambda tv_match: tv_match[1] ):

	for urlMatch,titleMatch in tv_matches:
		title = titleMatch.replace( "&#x27;" , "'" )
		url = urlMatch
		mc.Append(
			Function(
				DirectoryItem(
					TV_Episodes,
					title,
					subtitle="",
					summary=""
					#,thumb=TV_thumb(url)
				),
				title = title,
				url = url
			)
		)


	return mc
    
    
def TV_Episodes(sender,title,url):
    mc = MediaContainer( viewGroup = "/video/icefilms/TV/" + url )
    show_page = HTTP.Request( ICEFILMS_URL+"" + url )
    show_page = str(show_page)
    seasons_html = re.compile('<span class=list>(.+?)</span>').findall(show_page)
 
    seasonNames  = re.compile('<h4>(.+?)</h4>').findall(seasons_html[0])
    
   
    searchSource = seasons_html[0]+"<h4>"
   
    for seasonName in seasonNames :
	episodeTitle=seasonName
	
	if re.search('\(',seasonName) is not None:
         seasonName = str((re.split('\(+', seasonName))[0])
	
	filter = '<h4>'+seasonName+'.+?</h4>(.+?)<h4>'
	
	seasonSource = re.compile(filter).findall(searchSource)
	mc.Append(
			Function(
				DirectoryItem(
					TV_Show,
					episodeTitle,
					subtitle="",
					summary=""
					,thumb=TV_thumb(url)
				),
				title = title,
				show_page = seasonSource[0]
			)
		)
    return mc


def TV_Show( sender , title , show_page ):
        
	
	mc = MediaContainer( viewGroup = "/video/icefilms/TV/")

	
	show_matches = re.findall( "<img class=star><a href=(/ip.php?[^>]+?)>([^<]+?)</a>" , show_page )
	for show_match in show_matches:
	
		episode_Title = show_match[1].replace( "&#x27;" , "'" )
		url = show_match[0]
	
		#Log( "A = " + title + " B = " + url )
		
		mc.Append(
				Function(
					DirectoryItem(
						TV_Data,
						title = episode_Title,
						subtitle = title
						#,thumb=TV_thumb(url)
						
					),
					title = title + " -- " + episode_Title,
					url = url
				)
			)
		
	return mc

def TV_Data( sender , title , url ):

	t=""
	secret=""
	id=""
	cap="B3H9"
	
	try:
	    accountStatus = ""
	    accountStatus = Authenticate()
    
	    mc = MediaContainer( viewGroup = "/video/icefilms/TV/" + url + "2" ,httpCookies=HTTP.GetCookiesForURL('http://www.megaupload.com/'))
	    data_page = HTTP.Request( ICEFILMS_URL + url , cacheTime = 5 )
	    data_page = str(data_page)
    
	    plotSummary = ""
	    description_match = re.findall('<tr><th>Description:</th><td>(.+?)<a',data_page)
	    for description in description_match :
	     plotSummary = description
	     
	    data_matches = re.findall( "\"(/membersonly/components/com_iceplayer/.*?)\"" , data_page )
	    if len(data_matches) > 0 :
		
		
		data_page = HTTP.Request( ICEFILMS_URL+ data_matches[0] , cacheTime = 5 )
		data_page = str(data_page)
	    
    
		args = {
		  'iqs': '',
		  'url': '',
		  'cap': ''
		}
    
		sec = re.search("f\.lastChild\.value=\"([^']+)\",a", data_page).group(1)
		t   = re.search('"&t=([^"]+)",', data_page).group(1)
    
		args['sec'] = sec
		args['t'] = t
    
		#mc = MediaContainer( viewGroup = "/video/icefilms/TV/" + url + "1")
		
		defcat=re.compile('<div class=ripdiv><b>DVDRip / Standard Def</b>(.+?)</div>').findall(data_page)
		for scrape in defcat:
		 mc = SOURCE(data_page, scrape,mc,title,plotSummary,accountStatus,url)
	       
		if(len(mc) >0) :
		 return mc
		else:
		 return MessageContainer(
		  "Sources Not Found",
		  "No Source can be retrieved for the Title \"" + title + "\"" 
		 )
		return mc
	except:
	    return MessageContainer(
	    "   ",
	    "Apparently, something unfortunate has \nhappened. Your request cannot be  \ncarried out at this time. \n Please Try later"
	)
def Movie_Data( sender , title , url ,HD=None):

	
	t=""
	secret=""
	id=""
	cap="B3H9"
	accountStatus = ""
        accountStatus = Authenticate()
	
	try:
	
	    mc = MediaContainer( viewGroup = "/video/icefilms/TV/" + url + "2" ,httpCookies=HTTP.GetCookiesForURL('http://www.megaupload.com/'))
	    data_page = HTTP.Request( ICEFILMS_URL + url , cacheTime = 5 )
	    data_page = str(data_page)
	    
	    plotSummary = ""
	    description_match = re.findall('<tr><th>Description:</th><td>(.+?)<a',data_page)
	    for description in description_match :
	     plotSummary = description
	     
	    data_matches = re.findall( "\"(/membersonly/components/com_iceplayer/.*?)\"" , data_page )
	    if len(data_matches) > 0 :
		
		
		data_page = HTTP.Request( ICEFILMS_URL + data_matches[0] , cacheTime = 5 )
		data_page = str(data_page)
	    
    
		args = {
		  'iqs': '',
		  'url': '',
		  'cap': ''
		}
    
		sec = re.search("f\.lastChild\.value=\"([^']+)\",a", data_page).group(1)
		t   = re.search('"&t=([^"]+)",', data_page).group(1)
    
		args['sec'] = sec
		args['t'] = t
    
		#mc = MediaContainer( viewGroup = "/video/icefilms/TV/" + url + "1")
		if HD is True:
		    defcat=re.compile('<div class=ripdiv><b>HD 720p</b>(.+?)</div>').findall(data_page)
		elif HD is None:
		    defcat=re.compile('<div class=ripdiv>(.+?)</div>').findall(data_page)
		
		for scrape in defcat:
		 mc = SOURCE(data_page, scrape,mc,title,plotSummary,accountStatus,url)
		
		
		if(len(mc) >0) :
		    return mc
		else:
		    return MessageContainer(
		     "Sources Not Found",
		     "No Source can be retrieved for the Title \"" + title + "\"" 
		    )
	    
		
		return mc
	except:
	    return MessageContainer(
	    "   ",
	    "Apparently, something unfortunate has \nhappened. Your request cannot be  \ncarried out at this time. \n Please Try later"
	)
    
def SOURCE(page, sources,mc,title,plotSummary,accountStatus,thumbURL):
          
          args = {
              'iqs': '',
              'url': '',
              'cap': ''
          }

          sec = re.search("f\.lastChild\.value=\"([^']+)\",a", page).group(1)
          t   = re.search('"&t=([^"]+)",', page).group(1)

          args['sec'] = sec
          args['t'] = t
          

          # create a list of numbers: 1-21
          num = 1
          numlist = list('1')
          while num < 21:
              num = num+1
              numlist.append(str(num))

          #for every number, run PART.
          #The first thing PART does is check whether that number source exists...
          #...so it's not as CPU intensive as you might think.

          for thenumber in numlist:
               mc = PART(sources,thenumber,args,mc,title,plotSummary,accountStatus,thumbURL)

	  return mc
def PART(scrap,sourcenumber,args,mc,title,plotSummary,accountStatus,thumbURL):
     #check if source exists
     
     sourcestring='Source #'+sourcenumber
     checkforsource = re.search(sourcestring, scrap)
     
     #if source exists proceed.
     if checkforsource is not None:
          #print 'Source #'+sourcenumber+' exists'
          
          #check if source contains multiple parts
          multiple_part = re.search('<p>Source #'+sourcenumber+':', scrap)
          
          if multiple_part is not None:
               #print sourcestring+' has multiple parts'
               #get all text under source if it has multiple parts
               multi_part_source=re.compile('<p>Source #'+sourcenumber+': (.+?)PART 1(.+?)</i><p>').findall(scrap)

               #put scrape back together
               for sourcescrape1,sourcescrape2 in multi_part_source:
                    scrape=sourcescrape1+'PART 1'+sourcescrape2
                    pair = re.compile("onclick='go\((\d+)\)'>PART\s+(\d+)").findall(scrape)
                    for id, partnum in pair:
                     url = GetSource(id, args)
                        # check if source is megaupload or 2shared, and add all parts as links
                        #ismega = re.search('\.megaupload\.com/', url)
                     partname='Part '+partnum +' -- 720P High Def'
		     
                     fullname=sourcestring +' || '+ partname
                     
		     mc=AddMediaItem(fullname,url,mc,title,plotSummary,accountStatus,thumbURL)
                        
          # if source does not have multiple parts...
          elif multiple_part is None:
               # print sourcestring+' is single part'
               # find corresponding '<a rel=?' entry and add as a one-link source
               source5=re.compile('<a\s+rel='+sourcenumber+'.+?onclick=\'go\((\d+)\)\'>Source\s+#'+sourcenumber+':').findall(scrap)
               # print source5
               for id in source5:
                    url = GetSource(id, args)
                    
                    # print 'Source #'+sourcenumber+' is hosted by megaupload'
                    fullname=sourcestring   +' || ' + ' Full -- DVDRip '
		    
		    mc=AddMediaItem(fullname,url,mc,title,plotSummary,accountStatus,thumbURL)
     return mc              


def GetSource(id, args):
    m = random.randrange(100, 300) * -1
    s = random.randrange(5, 50)
    params = copy.copy(args)
    params['id'] = id
    params['m'] = m
    params['s'] = s
 
    body = GetFinalURL(params)
    url=body
    
    return url



def GetFinalURL(post_values):
    
    next_page = HTTP.Request( ICEFILMS_URL+"membersonly/components/com_iceplayer/video.phpAjaxResp.php", post_values , { "User-Agent" : "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3" , "Referer" : "http://www.icefilms.info" } )
    next_page = str(next_page)
    
  

    next_next_page = HTTP.Request( ICEFILMS_URL + next_page )
    next_next_page = str(next_next_page)
    

    data_matches = re.findall( "(http://www.megaupload.com/.*?)\"" , next_next_page )
    if len(data_matches) > 0:
     return data_matches[0]
    
    
     


def AddMediaItem(name,url,mc,title,plotSummary,accountStatus,thumbURL):
    
    if url is not None:
      if(accountStatus=='None') :
	 name=name+" (Wait 45 Secs) "
      elif(accountStatus==''):
	 name=name+" (Wait 25 Sec) "
      
    mc.Append(
	    Function(
		    DirectoryItem(
			    get_stream,
			    title = name,
			    subtitle = title,
			    summary=plotSummary
			    ,thumb=TV_thumb(thumbURL)
			    
		    ),
		    title = title ,
		    url = url,
		    accountStatus=accountStatus
	    )
    )
             
    return mc




def get_stream( sender , title , url ,accountStatus):
     
     mc = MediaContainer( viewGroup = "/video/icefilms/TV/" + url + "2" ,httpCookies=HTTP.GetCookiesForURL('http://www.megaupload.com/'))
     #Log("URL = " + url)
     HTTP.ClearCookies()
     data_page = HTTP.Request( url,cacheTime=0)
     data_page = str(data_page)
  
     data_matches = re.compile('<a href="(.+?)" class="down_ad_butt1">').findall(data_page)
   
     if str(data_matches)=='[]':
      match2=re.compile('id="downloadlink"><a href="(.+?)" class=').findall(data_page)
      finalurl=match2[0]
     else:
      finalurl=match1[0]
     
     #Log("Download Link " + finalurl)
     
     mc.Append(VideoItem(finalurl, "Play Now : "+title,subtitle=title))
     if(accountStatus=='premium'):
       time.sleep(float(3))
       return mc
     elif(accountStatus=='None'):
       time.sleep(float(47))
       return mc
     else:
       time.sleep(float(27))
       return mc
    
def GetURL(url, params = None, referrer = ICEFILMS_REFERRER, cookie = None, save_cookie = False):
     # print 'GetUrl: ' + url
     # print 'params: ' + repr(params)
     # print 'referrer: ' + repr(referrer)
     # print 'cookie: ' + repr(cookie)
     # print 'save_cookie: ' + repr(save_cookie)

     if params:
        req = urllib2.Request(url, params)
        # req.add_header('Content-type', 'application/x-www-form-urlencoded')
     else:
         req = urllib2.Request(url)

     req.add_header('User-Agent', USER_AGENT)

     # as of 2011-06-02, IceFilms sources aren't displayed unless a valid referrer header is supplied:
     # http://forum.xbmc.org/showpost.php?p=810288&postcount=1146
     if referrer:
         req.add_header('Referer', referrer)

     if cookie:
         req.add_header('Cookie', cookie)

     # avoid Python >= 2.5 ternary operator for backwards compatibility
     # http://wiki.xbmc.org/index.php?title=Python_Development#Version
     response = urllib2.urlopen(req)
     body = response.read()

     if save_cookie:
         setcookie = response.info().get('Set-Cookie', None)
         print "Set-Cookie: %s" % repr(setcookie)
         if setcookie:
             setcookie = re.search('([^=]+=[^=;]+)', setcookie).group(1)
             body = body + '<cookie>' + setcookie + '</cookie>'

     response.close()
     return body


def SEARCH(mc,search):
     #kb = xbmc.Keyboard('', 'Search Icefilms.info', False)
     #kb.doModal()
     #if (kb.isConfirmed()):
          
          if search != '':
             
             DoEpListSearch(mc,search)
             DoSearch(mc,search,0)
             DoSearch(mc,search,1)
             DoSearch(mc,search,2)
             #delete tv show name file, do the same for season name file
             
               
                               
def DoSearch(mc,search,page):        
	gs = GoogleSearch('site:'+ICEFILMS_URL+'ip '+search+'')
        gs.results_per_page = 25
        gs.page = page
        results = gs.get_results()
	
        for res in results:
                name=res.title.encode('utf8')
                name=CLEANSEARCH(name)
                url=res.url.encode('utf8')
		index=url.index("/ip")
		match=url[index:len(url)]
		
		addSearchResult(mc,name,match,'Movie')

def DoEpListSearch(mc,search):
               tvurl=ICEFILMS_URL+'tv/series'              

               # use urllib.quote_plus() on search instead of re.sub ?
               searcher=urllib.quote_plus(search)
               #searcher=re.sub(' ','+',search)
               url='http://www.google.com/search?hl=en&q=site:'+tvurl+'+'+searcher+'&btnG=Search&aq=f&aqi=&aql=&oq='
               link=GetURL(url)

               match=re.compile('<h3 class="r"><a href="'+tvurl+'(.+?)"(.+?)">(.+?)</h3>').findall(link)
               
	       
               for myurl,interim,name in match:
                 
		    #if len(interim) < 80:
			
		 name=CLEANSEARCH(name)                              
		 hasnameintitle=re.search(search,name,re.IGNORECASE)
		 #Log(name)
		 if hasnameintitle is not None:
		     myurl=tvurl+myurl
	       
		     myurl=re.sub('&amp;','',myurl)
		 
		     #match = re.compile('ICEFILMS_URLip.php?(.*?)').findall(url)
		     index=myurl.index("/tv")
		     match=myurl[index:len(url)]
		    
		     #addDir(name,myurl,12,'')
		     addSearchResult(mc,name,match,'TV')

     
def CLEANSEARCH(name):        
        name=re.sub('<em>','',name)
        name=re.sub('</em>','',name)
        name=re.sub('DivX - icefilms.info','',name)
        name=re.sub('</a>','',name)
        name=re.sub('<b>...</b>','',name)
        name=re.sub('- icefilms.info','',name)
        name=re.sub('.info','',name)
        name=re.sub('- icefilms','',name)
        name=re.sub(' -icefilms','',name)
        name=re.sub('-icefilms','',name)
        name=re.sub('icefilms','',name)
        name=re.sub('DivX','',name)
        name=re.sub('-  Episode  List','- Episode List',name)
        name=re.sub('-Episode  List','- Episode List',name)
        #name=re.sub('&#39;',"'",name)
        #name=re.sub('&amp;','&',name)
        return name


def addSearchResult(mc,name,url,mode):
    
    if mode is 'TV':
	mc.Append(
	 Function(
	  DirectoryItem(
	   TV_Episodes,
	   title = name,
	   thumb=TV_thumb(url)
	  ),
	  title = name,
	  url = url
	 )
	)
    elif mode is 'Movie':
	mc.Append(
	 Function(
	  DirectoryItem(
	   Movie_Data,
	   title = name,
	   thumb=TV_thumb(url)
	  ),
	  title = name,
	  url = url
	 )
	)

    
def TV_thumb(url):
	

	tv_show_page = HTTP.Request(ICEFILMS_URL + url,cacheTime=100000 );
	tv_show_page = str(tv_show_page)
	
	tv_show_matches = re.findall( "<a class=noref target=_blank href=/noref.php\?url=([^ ]+)>" , tv_show_page )
	if len(tv_show_matches) > 0:
		return tv_show_matches[0]
		
	tv_show_matches = re.findall( "<img width=200 src=([^ ]+) " , tv_show_page )
	if len(tv_show_matches) > 0:
		return tv_show_matches[0]
	
	
		
	return ""


		
# Part of the "search" example 
# query will contain the string that the user entered
# see also:
#   http://dev.plexapp.com/docs/Objects.html#InputDirectoryItem
def SearchResults(sender,query=None):
    
    mc = MediaContainer( viewGroup = "/video/icefilms/TV/Search"  + "1" ,httpCookies=HTTP.GetCookiesForURL('http://www.megaupload.com/'))
    SEARCH(mc,query)
    if(len(mc) >0) :
	return mc
    else:
	return MessageContainer(
	    "Zero Matches",
	    "No results found for your query \"" + query + "\""
	)
    
  
