# AGPL 3.0+
# Odin Hørthe Omdal <odin.omdal@gmail.com>
# vim: encoding=utf8 ts=4 sws=4 expandtab
from stompservice import StompClientFactory
from twisted.internet import reactor, defer
from orbited import json
from func import mkslug
import cPickle
import sys, os

CONFERENCE_STORAGE = "conf/"
CHANNEL_NAME = "/topic/graph2"

conf = None
parts = []
ac_part = None

class Conference():
    name = ''
    slug = ''
    when = ''
    tag = ''
    active = False

    def __init__(self, name, tag, when='snart'):
        self.name = name
        self.tag = tag
        self.when = when

        self.slug = mkslug(self.name)

class Part():
    name = ''
    slug = ''
    when = ''
    active = False
    slides = 0
    slide = 0

    def __init__(self, name, slides, when='snart'):
        self.name = name
        self.slides = int(slides)
        self.when = when

        self.slug = mkslug(self.name)
	os.mkdir("htdocs/" + self.slug)
	os.mkdir("htdocs/" + self.slug + "/slides/")

        self.active = False
        self.slide = 0

    def slide_next(self):
        if self.slide < self.slides-1:
            self.slide += 1

    def slide_prev(self):
        if self.slide > 0:
            self.slide -= 1

    def slide_n(self, n):
        if self.slides > n >= 0:
            self.slide = n

    def json_equivalent(self):
        return self.__dict__

    def __str__(self):
        return '%s' % self.name


conferences = os.listdir(CONFERENCE_STORAGE)
for c in conferences:
    print "%s: %s" % (conferences.index(c), c)

con = raw_input("Kva for konferanse? ")

if con.isdigit():
    c = int(con)
    con = conferences[c]
    folder = CONFERENCE_STORAGE + con

    conf = cPickle.load(open(folder + "/conf.pickle", "rb"))
    parts = cPickle.load(open(folder + "/parts.pickle", "rb"))
else:
    folder = CONFERENCE_STORAGE + con
    os.mkdir(folder)

    tag = raw_input("mikrobloggtagg? ")
    kortid = raw_input("kor tid? ")
    conf = Conference(con, tag, kortid)

    fp = open(folder + "/conf.pickle", "wb")
    cPickle.dump(conf, fp, protocol=2)
    fp.close()

    fp = open(folder + "/parts.pickle", "wb")
    cPickle.dump(parts, fp, protocol=2)
    fp.close()


def part_new():

    namn = raw_input("namn: ").decode("utf-8")
    slides = raw_input("tal på slides: ")
    kortid = raw_input("kor tid: ")

    return Part(namn, slides, kortid)

#def part_active()
if not parts:
    print "Legg til ny del"
    parts.append(part_new())

fp = open("htdocs/" + conf.slug + "/first.json", "w")
fp.write(json.encode(conf.__dict__))
fp.close()

def chpart(part_no):
    global ac_part

    if ac_part:
        ac_part.active = False

    ac_part = parts[part_no]

    try:
        os.mkdir("htdocs/" + conf.slug + "/" + ac_part.slug)
    except OSError:
        pass

    try:
        os.unlink("htdocs/first.json")
    except OSError:
        pass

    fp = open("htdocs/" + conf.slug + "/" + ac_part.slug + "/first.json", "w")
    fp.close()

    os.symlink(conf.slug + "/" + ac_part.slug + "/first.json", "htdocs/first.json")

chpart(0)

for part in parts:
    print u"%d, %s: %s (%s slides, %s)" %           \
        (parts.index(part), part.when, part.name,   \
            part.slides, part.slug,)

class DataProducer(StompClientFactory):

    def recv_connected(self, msg):
        print 'Connected to %s' % CHANNEL_NAME
        self.send_data()
        reactor.callLater(0.1, self.output_loop)
        #self.timer = LoopingCall(self.send_data)
        #self.timer.start(1)

    def output_loop(self):
        global ac_part

        command = raw_input("%2d> " % ac_part.slide)
        if command == "n":
            ac_part.slide_next()
        elif command == "p":
            ac_part.slide_prev()
        elif command == "s":
            
            fp = open(folder + "/conf.pickle", "wb")
            cPickle.dump(conf, fp, protocol=2)
            fp.close()

            fp = open(folder + "/parts.pickle", "wb")
            cPickle.dump(parts, fp, protocol=2)
            fp.close()

            print "Lagra"

        elif command == "l":
            for part in parts:
                print u"%d, %s: %s (%s slides, %s)" %           \
                    (parts.index(part), part.when, part.name,   \
                        part.slides, part.slug,)
        elif command == "part":
            parts.append(part_new())
        elif command == "chpart":
            a = int(raw_input("delnummer: "))
            chpart(a)

        elif command == "activate":
            if ac_part.active == True:
                ac_part.active = False
                print "Deactivated " + ac_part.name
            else:
                ac_part.active = True
                print "Activated " + ac_part.name

        elif command.isdigit():
            ac_part.slide_n(int(command))
        else:
            print "'n' for neste, 'p' for førre eller t.d. 12 for direkte"

        self.send_data()
        reactor.callLater(0.1, self.output_loop)

    def recv_message(self,msg):
    	print msg

    def send_data(self):
	global ac_part, conf

	if isinstance(ac_part, Part):
            ting = {'part': ac_part.__dict__, 'conf': conf.__dict__}
            js = str(json.encode(ting))
        else:
            print "Ingen JS"
            js = ""
        self.send(CHANNEL_NAME, js)

	fp = open("htdocs/" + conf.slug + "/" + ac_part.slug + "/first.json", "w")
	fp.seek(0)
	fp.write(js)
	fp.flush()
	fp.close()

reactor.connectTCP('127.0.0.1', 61613, DataProducer())
reactor.run()

