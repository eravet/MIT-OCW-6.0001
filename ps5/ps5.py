# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        """Initializes a NewsStory object
        
        globally unique identifier (GUID) - a string
        title - a string
        description - a string
        link to more content - a string
        pubdate - a datetime
        """
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate.replace(tzinfo=pytz.timezone('EST'))
        
    def get_guid(self):
        """Used to safely access the guid of the article outside of the class
        
        Returns: self.guid (a string)
        """
        return self.guid
    
    def get_title(self):
        """Used to safely access the news story title outside of the class
        
        Returns: self.title (a string)
        """
        return self.title
    
    def get_description(self):
        """Used to safely access the description of the article outside of the class
        
        Returns: self.description (a string)
        """
        return self.description
    
    def get_link(self):
        """Used to safely access the link of the article outside of the class
        
        Returns: self.link (a string)
        """
        return self.link
    
    def get_pubdate(self):
        """Used to safely access the publication date of the article outside of the class
        
        Returns: self.pubdate (a datetime)
        """
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()
    
    def get_phrase(self):
        return self.phrase
    
    def is_phrase_in(self, text):
        """This methods returns True if the passed phrase is contained in the 
        passed text.
        
        Returns: boolean
        """
        #replace title puncuation with spaces
        for i in string.punctuation:
            text = text.replace(i, " ")
        
        spaced_text = " ",join(text.lower().split())
        
        return (self.get_phrase() + ' ') in (spaced_text + ' ')
    

# Problem 3
class TitleTrigger(PhraseTrigger):
    def __init__(self, title):
        PhraseTrigger.__init__(self, title)
    
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())

# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, description):
        PhraseTrigger.__init__(self, description)
        
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())
    
# TIME TRIGGERS

# Problem 5

class TimeTrigger(Trigger):
    def __init__(self, time):
        try:
            #datetime formatting according to format string, with EST standardized timezone
            self.time = datetime.strptime(time, "%d %b %Y %H:%M:%S").replace(tzinfo = pytz.timezone("EST"))
        except ValueError as e:
            raise(e)
            
    def get_time(self):
        return self.time
    
# Problem 6

class BeforeTrigger(TimeTrigger):
    def __init__(self, time):
        TimeTrigger.__init__(self, time)
        
    def evaluate(self, story):
        return self.get_time() > story.get_pubdate()

class AfterTrigger(TimeTrigger):
    def __init(self, time):
        TimeTrigger.__init__(self, time)
        
    def evaluate(self, story):
        return self.get_time() < story.get_pubdate()

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trig):
        self.trig = trig
        
    def evaluate(self, story):
        return not self.trig.evaluate(story)

# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trig1, trig2):
        self.trig1 = trig1
        self.trig2 = trig2
    
    def evaluate(self, story):
        return self.trig1.evaluate(story) and self.trig2.evaluate(story)
    
# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trig1, trig2):
        self.trig1 = trig1
        self.trig2 = trig2
        
    def evaluate(self, story):
        return self.trig1.evaluate(story) or self.trig2.evaluate(story)
#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    filtered_story = []
    
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered_story.append(story)
                break
            
    return filtered_story



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    trigger_dict = {'TITLE' : TitleTrigger, 'DESCRIPTION' : DescriptionTrigger, 'AFTER' : AfterTrigger, 'BEFORE' : BeforeTrigger, 'NOT' : NotTrigger, 'AND' : AndTrigger, 'OR' : OrTrigger}
    list_of_triggers = []
    
    for line in lines:
        split_line = line.split(',')
        name = split_line[0]
        if name != 'ADD':
            trigger_name = split_line[1]
            trigger_input1 = split_line[2]
            
            try:
                trigger_input2 = split_line[3]
            except:
                trigger_input2  = 'null'
            
            if trigger_name != 'AND' and 'OR':
                name = trigger_dict[trigger_name](trigger_input1)
            else:
                name = trigger_dict[trigger_name](trigger_input1, trigger_input2)
            print(name)
        else:
            for trig in split_line[1:]:
                list_of_triggers.append(trig)
        
    print(list_of_triggers)


        
SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

