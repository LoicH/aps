import numpy as np
import time
import modifTexte


def fusion_words(list_dic_freq) : # needs dictionnary list. One dictionnary[word : frequency] per document
    list_words=[];                # return all different worlds in all documents
    for dic in list_dic_freq :
        for word in dic :
            if word not in list_words :
                list_words.append(word);
    return list_words

#def compute_idf(list_dic_freq, word) :
#    S = 0;
#    for dic in list_dic_freq :
#        if dic(word) != 0 :
#            S = S+1
#    return np.log(len(list_dic_freq)/S)
        
        
#def compute_tfidf(list_dic_freq,word, doc) :
#    idf = compute_idf(list_dic_freq, word)
#    dic = list_dic_freq[doc]
#    tf = dic(word)
#    tfidf= tf*np.log(idf)
#    return tfidf

def linkWordDocFreq(list_dic_freq, list_titles) : # needs : - dictionnary list. One dictionnary[word : frequency] per document. 
                                                  #         - titles list 
    dict_origin_words = dict()                    # returns one dictionnary[word : dictionnary : [ doc where this word is : word frequency in this doc]]
    dict_pdf_occur = dict()                       # To put it simply, for each world we have access to his frequency in each doc where the word is.
    list_words = fusion_words (list_dic_freq)
    for word in list_words :
        dict_pdf_occur = dict()
        for i in range(len(list_dic_freq)) :
            if word in list_dic_freq[i] :
                dict_pdf_occur[list_titles[i]]=list_dic_freq[i][word]
        dict_origin_words[word]=dict_pdf_occur
    return dict_origin_words


def compute_tfidf(linkWordDocFreq, word, title, list_titles) : # computes tfidf from the dictionnary which associates words and their frequencies in each document
    if title in linkWordDocFreq[word] :
        tf = linkWordDocFreq[word][title]
    else :          # if the word in not in this doc : tf = 0 --> tfidf = 0
        return 0
    idf= float(len(list_titles))/len(linkWordDocFreq[word])
    return tf*np.log(idf)
    
#def create_matrix(dic_mot_doc_occurence, list_titles) :
#    list_not_null_values = []
#    list_columns = []
#    list_lines = []
#    list_words = []
#    i = 0
#    tfidf = 0
#    for word in dic_mot_doc_occurence :
#        for j in range(len(list_titles)) :
#            title = list_titles[j]
#            tfidf = compute_tfidf2(dic_mot_doc_occurence, word, title, list_titles)
#            if tfidf != 0 :
#                list_not_null_values.append(tfidf)
#                list_columns.append(i)
#                list_words.append(word)
#                list_lines.append(j)
#        i=i+1
#    return [list_not_null_values, list_columns, list_words, list_lines]
    
#def create_matrix2(dic_mot_doc_occurence, list_titles) :
#    list_not_null_values = []
#    dic_columns = dict()
#    dic_lines = dict()
#    i = 0
#    tfidf = 0
#    for word in dic_mot_doc_occurence :
#        for j in range(len(list_titles)) :
#            title = list_titles[j]
#            tfidf = compute_tfidf2(dic_mot_doc_occurence, word, title, list_titles)
#            if tfidf != 0 :
#                list_not_null_values.append(tfidf)
#                dic_columns[i] = word
#                dic_lines[j] = title
#        i=i+1
#    return [list_not_null_values, dic_columns, dic_lines]
    
def create_matrix(linkWordDocFreq, list_titles) :
    matrix = np.zeros((len(linkWordDocFreq),len(list_titles)),float) # matrix initialization : words in ligns, columns in lines
    i = 0
    j = 0
    linkWordLine = dict()
    linkDocColumn = dict()
    for title in list_titles :
        linkDocColumn[title]=i
        i=i+1
    for word in linkWordDocFreq :
        linkWordLine[word]=j
        j=j+1
    
    for word in linkWordDocFreq:
        for title in linkWordDocFreq[word]:            
            matrix[linkWordLine[word]][linkDocColumn[title]]=compute_tfidf(linkWordDocFreq,word,title, list_titles)

    return matrix, linkWordLine, linkDocColumn
    
def accessMatrix(matrix, i, j) :
    return matrix[i][j]


def index2(list, i) :
    pos = []
    j = 0
    for a in list :
        if a == i :
            pos.append(j)
        j+=1
    return pos

def create_matrix2(linkWordDocFreq, list_titles) :
    listNonNullValues = []
    listLines = []
    listColumns = []
    i = 0
    j = 0
    linkDocLine = dict()
    linkWordColumn = dict()
    
    for title in list_titles :
        linkDocLine[title]=i
        i=i+1
    for word in linkWordDocFreq :
        linkWordColumn[word]=j
        j=j+1
    
    for word in linkWordDocFreq:
        for title in linkWordDocFreq[word]:   
            tfidf = compute_tfidf(linkWordDocFreq,word,title, list_titles)
            if tfidf != 0 :
                listNonNullValues.append(tfidf)
                listLines.append(linkDocLine[title])
                listColumns.append(linkWordColumn[word])

    return listNonNullValues, listLines, listColumns, linkDocLine, linkWordColumn
    
def accessMatrix2(matrix, i, j) :
    for k in range(len(matrix[1])) :
        if matrix[1][k] == i :
            if matrix[2][k] == j :
                return matrix[0][k]
    return 0


def accessMatrix2(matrix, i, j) :
    for k in range(len(matrix[1])) :
        if matrix[1][k] == i :
            if matrix[2][k] == j :
                return matrix[0][k]
    return 0
    
#dic_freq1 = dict()
#dic_freq2 = dict()
#dic_freq3 = dict()
#
#dic_freq1["poisson"] = 0.5
#dic_freq1["a"]=0.4
#dic_freq1["b"]=0.6
#
#dic_freq2["viande"] = 0.6
#dic_freq2["a"]=0.7
#dic_freq2["b"]=0.8
#
#dic_freq3["oeuf"] = 0.4
#dic_freq3["a"]=0.7
#dic_freq3["c"]=0.2
#
#list_dic_freq = [dic_freq1, dic_freq2, dic_freq3] 
#list_titles= ["ninja", "samourai", "wasabi"]
#dic = linkWordDocFreq(list_dic_freq, list_titles)
#
#u = create_matrix(dic, list_titles)
#m=u[0]
#n = create_matrix2(dic, list_titles)
#
#
#t0 = time.clock()
#for i in range(len(m)):
#    for j in range(len(m[0])) :
#        print(accessMatrix(m,i,j))
#print("La premiere methode met en secondes :")
#print time.clock() - t0
#
#t0 = time.clock()
#for i in range(len(m)):
#    for j in range(len(m[0])) :
#        print(accessMatrix2(n,i,j))
#print("La deuxieme methode met en secondes :")
#print time.clock() - t0


weiser = textToDictionnary("""an important step toward ensuring
that our infrastructure research is
robust and scalable in the: face of the
details of the real world.
The idea of ubiquitous computing
first arose from contemplating the
place of today's computer in actual
activities of everyday life. In particular,
anthropological studies of work
life [14, 22] teach us that people primarily
work in a world of shared situations
and unexamined technological
skills. The computer today is
isolated from the overall situation,
however, and fails to get out of the
way of the work. In other words,
rather than being a tool through
which we work, and thus disappearing
from our awareness, the computer
too often remains the focus of
attention. And this is true throughout
the domain of personal computing
as currently implemented and
discussed tsar the future:, whether
one thinks of personal computers,
palmtops, or dynabooks. The characterization
of the future computer as
the "intimate computer" [12], or
"rather like a human assistant" [25]
makes this attention to the machine
itself particularly apparent.
Getting the computer out of the
way is not easy. This is not a graphical
user interface (GUI) problem, but
is a property of the whole context of
usage of the machine and the attributes
of its physical properties: the
keyboard, the weight and desktop
position of '.screens, and so on. The
problem is not one of "interface."
For the same reason of context, this
is not a multimedia problem, resulting
from any particular deficiency in
the ability to display certain kinds of
real-time data or integrate them into
applications. (Indeed, raultimedia
tries to grab attention, the opposite
of the ubiquitous computing ideal of
invisibility.) The challenge is to create
a new kind of relationship of people
to computers, one in which the
computer would have to take the
lead in becoming vastly better at getting
out of the way, allowing people
to just go about their live,;.
In 1988, when I started PARC's
work on ubiquitous computing, virtual
reality (VR) came the closest to
enacting the principles we believed
important. In its ultimate envisionment,
VR causes the computer to
-I{-E.ILL.
become effectively invisible by taking
over the human sensory and affector
systems [19]. VR is extremely useful
in scientific visualization and entertainment,
and will be very significant
for those niches. But as a tool for
productively changing everyone's
relationship to computation, it has
two crucial flaws: first, at the present
time (1992), and probably for decades,
it cannot produce a simulation
of significant verisimilitude at reasonable
cost (today, at any cost). This
means that users will not be fooled
and the computer will not be out of
the way. Second, and most important,
it has the goal of fooling the
user--of leaving the everyday physical
world behind. This is at odds with
the goal of better integrating the
computer into human activities, since
humans are of and in the everyday
world.
Ubiquitous computing is exploring
quite different ground from personal
digital assistants, or the idea
that computers should be autonomous
agents that take on our goals.
The difference can be characterized
as follows: Suppose you want to lift a
heavy object. You can call in your
strong assistant to lift it for you, or
you yourself can be made effortlessly,
unconsciously, stronger and
just lift it. There are times when both
are good. Much of the past and current
effort for better computers has
been aimed at the former; ubiquitous
computing aims at the latter.
The approach I took was to attempt
the definition and construction
of new computing artifacts for
use in everyday life. I took my inspiration
from the everyday objects
found in offices and homes, in particular
those objects whose purpose is
to capture or convey information.
The most ubiquitous cu .... t infnr_
mational technology el
artifacts is the use of writ
primarily words, but in,
pictographs, clocks, and
of symbolic communical
than attempting to repr
objects inside the virtu;
world, leading to another "desktop
model" [2], I wanted to put the new
kind of computer out in this world of
concrete information conveyers.
Since these written artifacts occur in
many different sizes and shapes, with
malay different qualities, I wanted
the computer embodiments to be of
many sizes and shapes, including tiny
inexpensive ones that could bring
computing to everyone.
The physical world comes in all
sizes and shapes. For practical reasons
our ubiquitous computing work
begins with just three different sizes
of devices: enough to give some
scope, not enough to deter progress.
The first size is the wall-sized interactive
surface, analogous to the office
whiteboard or the home magnetcovered
refrigerator or bulletin
board. The second size. is the notepad,
envisioned not as a personal
computer but as analogous to scrap
paper to be grabbed and used easily,
with many being used by a person at
one time. The cluttered office desk
or messy front-hall table are real-life
examples. Finally, the third size is the
tiny computer, analogous to tiny individual
notes or Post-it notes, and
also similar to the tiny little displays
of words found on book spines, light
switches, and hallways. Again, I saw
this not as a personal computer, but
as a pervasive part of everyday life,
with many active at all times. I called
these three sizes of computers
boards, pads, and tabs, and adopted
the slogan that, for each person in an
office, there should be hundreds of
tabs, tens of pads, and one or two
boards. Specifications for some prototypes
of these three sizes in use at
PARC are shown in Figure 1.
This then is Phase I of ubiquitous
computing: to construct, deploy, and
76 July 1993/Vol.361 No.7 ClOMMUN|q~AVlOMS OF THIE ACM 
-RoE-A-L*
learn from a computing environment
consisting of tabs, pads, and
boards. This is only Phase I, because
it is unlikely to achieve optimal invisibility.
(Later phases are yet to be determined.)
But it is a start down the
radical direction, for computer science,
away from emphasis on the
machine and back to the person and
his or her life in the world of work,
play, and home.
Hardware Prototypes
New hardware systems design for
ubiquitous computing has been oriented
toward experimental platforms
for systems and applications of
invisibility. New chips have been less
important than combinations of existing
components that create experimental
opportunities. The first ubiquitous
computing technology to be
deployed was the Liveboard [6],
which is now a Xerox product. Two
other important pieces of prototype
hardware supporting our research at
PARC are the Tab and the Pad.
Tab
The ParcTab is a tiny information
doorway. For user interaction it has a
pressure-sensitive screen on top of
the display, three buttons positioned
underneath the natural finger positions,
and the ability to sense its position
within a building. The display
and touchpad it uses are standard
commercial units.
The key hardware design problems
affecting the pad are physical
size and power consumption. With
several dozens of these devices sitting
around the office, in briefcases, in
pockets, one cannot change their batteries
every week. The PARC design
uses the 8051 chip to control detailed
interactions, and includes software
that keeps power usage down. The
major outboard components are a
small analog/digital converter for the
pressure-sensitive screen, and analog
sense circuitry for the IR receiver.
Interestingly, although we have been
approached by several chip manufacturers
about our possible need for
custom chips for the Tab, the Tab is
not short of places to put chips. The
display size leaves plenty of room,
and the display thickness dominates
total size. Off-the-shelf components
are more than adequate for exploring
this design space, even with our
severe size, weight, and power constraints.

A key part of our design philosophy
is to put devices in everyday use,
not just demonstrate them. We can
only use techniques suitable for
quantity 100 replication. This excludes
certain techniques that could
make a huge difference, such as the
integration of components onto the
display surface itself. This technology
is being explored at PARC, as
well as other research organizations.
While it is very promising, it is not yet
ready for replication.
The Tab architecture incorporates
a careful balance of display size,
bandwidth, processing, and memory.
For instance, the small display means
that even the tiny processor is capable
of providing a four-frames-persecond
video rate, and the IR bandwidth
is capable of delivering this.
The bandwidth is also such that the
processor can actually time the pulse
widths in software timing loops. Our
current design has insufficient storage,
and we are increasing the
amount of nonvolatile RAM in future
tabs from 8K to 128K. The tab's
goal of casual use similar to that of
Post-it notes puts it into a design
space generally unexplored in the
commercial or research sector.
Pad
The pad is really a family of notebook-sized
devices. Our initial pad,
the ScratchPad, plugged into a Sun
SBus card and provided an
X-Window-system-compatible writing
and display surface. This same
design was used inside our first wallsized
displays, the liveboards, as well.
Our later untethered pad devices,
the XPad and MPad, continued the
system design principles of
X-compatibility, ease of construction,
and flexibility in software and hardware
expansion.
As I write this article, at the end of
1992, commercial portable pen devices
have been on the market for
two years, although most of the early
companies have now gone out of
business. Why should a pioneering
research lab build its own such device?
Each year we ask ourselves the
same question, and so far three
things always drive us to continue to 
design our own pad hardware:
First, we need the correct balance
of features--this is the essence of
systems design. The commercial devices
all aim at particular niches, balancing
their design to that niche. For
research we need a rather different
balance, particularly for ubiquitous
computing. For instance, can the
device communicate simultaneously
along muh-iple channels? Does the
operating system support multiprocessing?
What about the potential for
high-speed tethering? i[s there a
high-quality pen? Is there a highspeed
expansion port sufficient for
video in and out? Is sound in/out and
ISDN connectivity available? Optional
keyboard? Any or,e commercial
device tends to satisfy some of
these needs, ignore others, and
choose a balance of the ones it does
satisfy, optimizing its niche, rather
than ubiquitous com]?uting-style
scrap computing. The ba)lance for us
emphasizes communication, system
memory, multimedia, and expansion
ports.
Second, apart from balance of features
are the requirements for particular
features. Key among these are
a pen emphasis, connection to research
envJironments such as Unix,
and communication emphasis. A
high-speed (>64KB/sec) wireless
capability is not built into any commercial
devices, and they do not generally
have a sufficiently high-speed
port to add such a radio. Commercial
devices generally come with DOS or
Penpoint, and while we have developed
in both, they are nor our favorite
researc]h vehicles because they
lack full access and customizability.
The third factor driving our own
pad design,; is ease of expansion and
modification. We need full hardware
specifications, complete operating
system source code, and the ability to
remove anti replace both hardware
and software component.,;. Naturally
these goals are opposed to best price
in a niche market, which orients the
documentation to the end user, and
keeps prices down by integrated
rather than modular design.
We have built and used three generations
of Pad designs. Six scratchpads
were built, three XPads, and 13
MPads, the latest. The M]?ad uses an
FPGA for almost all random logic,
giving extreme flexibility. For instance,
changing the power control
functions and adding high-quality
sound were relatively simple FPGA
changes. The MPad has both IR (tab
compatible) and radio communication
built-in and includes sufficient
uncommitted space for adding new
circuit boards later. It can be used
with a tether that provides it with
recharging and operating power and
an Ethernet connection. The operating
system is a standalone version of
the public-domain Portable Common
Runtime developed at PARC [28].
The Computer Science of
Ublcomp
To construct and deploy tabs, pads,
and boards at PARC, we found ourselves
having to readdress some of
the well-worked areas of existing
computer science. The fruitfulness
of ubiquitous computing for new
computer science problems justified
our belief in the ubiquitous computing
framework.
The following subsections "ascend"
the levels of organization of a
computer system, from hardware to
application. One or two examples of
computer science work required by
ubiquitous computing are described
for each level. Ubicomp is not yet a
coherent body of work, but consists
of a few scattered communities. The
point of this article is to help others
understand some of the new research
challenges in ubiquitous computing,
and inspire them to work on
them. This is more akin to a tutorial
than a survey, and necessarily selective.
The areas included are hardware
components (e.g., chips), network
protocols, interaction substrates
(e.g., software for screens and
pens), applications, privacy, and
computational methods.
Issues of Hardware
Components
In addition to the new systems of
tabs, pads, and boards, ubiquitous
computing necessitates some new
kinds of devices. Examples of three
new kinds of hardware devices are
very low-power computing, lowpower
high-bits/cubic-meter communication,
and pen devices.
LOW Power
In general the need for high performance
has dominated the need for
low-power consumption in processor
design. However, recognizing the
new requirements of ubiquitous
computing, a number of people have
begun work in using additional chip
area to reduce power rather than to
increase performance [16]. One key
approach is to reduce the clocking
frequency of their chips by increasing
pipelining or parallelism. Then,
by running the chips at reduced voltage,
the effect is a net reduction in
power, because power falls off as the
square of the voltage, while only
about twice the area is needed to run
at half the clock speed.
Power = CL*Vdd2*f
where CL is the gate capacitance,
Vdd the supply voltage,
and f the clocking frequency.
This method of reducing power
leads to two new areas of chip design:
circuits that will run at low power,
and architectures that sacrifice area
for power over performance. The
second requires some additional
comment, because one might suppose
one would simply design the
fastest possible chip, and then run it
at reduced clock and voltage. However,
as Lyon illustrates, circuits in
chips designed for high speed generally
fail to work at low voltages. Furthermore,
attention to special circuits
may permit operation over a much
wider range of voltage operation, or
achieve power savings via other special
techniques, such as adiabatic
switching [16].
Wireless
A wireless network capable of accommodating
hundreds of high-speed
devices for every person is well beyond
the commercial wireless systems
planned for the next 10 years
[20], which are aimed at one lowspeed
(64kb/sec or voice) device per
person. Most wireless work uses a
figure of merit of bits/sec x range,
and seeks to increase this product.
We believe that a better figure of
merit is bits/sec/meter 3. This figure
of merit causes the optimization of
total bandwidth throughout a 3D
space, leading to design points of
very tiny cellular systems.
Because we felt the commercial
world was ignoring the proper figure""", [] )






newell = textToDictionnary("""cited. Wc wish to speak oFcolnputcr science as empirical
inqttily.
()u~ view is only one of Jmu~y; thc prcx.ious lc'ctures
m:xkc th~,l clc~r. }lowcvcr, c,/cn takeli together tile ice
[kl[cs fail ~o cover the whole scope of our science. Many
Rmdamcntai aspucts of" it have not bccn represcutcd h~
thcsu tun ~ts~ards, Aml il' the time cvcr arrives, surely
lie( booi!, whcll the cOill[)ass has bcc~] boxed~ w)le~l colnptm:r
sck'uce has b(c~l discussed Fronl every side, it will
bc tinnt t~ Start tile cycIe ;l~xliN. t::;oy the hsYc ~ts lectiltcr
s'~ili l~avc to nmk~: ~.tt~ annual sprim to o~ert~.~kc the
cumulation of srmdt, i~}cremcntal gains tiu~t the tortoise
of' scientific und tcchnic~ll development i~as achieved ill
his stcudy murch, }]ach war will create a r~ew gap a~rcl
caU For :x new sprint, For irt science there is rio ihml word.
(;omputcr science is un empirical discipline. We would
havu called it arl cxperJtncntal science, but like ashonou~y,
cc'~u~omk:s, :rod gcolo.gy, some of its uuiquc
forms of obscrvation and experience do not fit a marrow
stereotype of the expcrimc'ntal meGod. None thc less,
they arc uxpt'rimcuts. }}uch new nmchinc that is built is
an experiment. Actu~Aly cons/ructi~g the machine poses
~1 qucStioI1 to ~l,.'Htlre; atld we listen for the a~Jswer by
observing thc machhle irl operation and analyzing it by
~dl amdytic:~l amt me,inurement mcuns available. Kach
nuw progr:.~m that is built is :u~l cxpcrmient, It poses a
ctucsticm h) ~ra:h~ic. a~rd its bchuvior oflkxs cities to arl
u,swcr. Nuithcr machi~lcs nor progr,:m~s are black
boxes: they arc artiIi~cl.s that have bccn dcsigi~cd, both
hi~rdwarc ',ill<:] SO]'{w;~ue, alld we ,ca~r open thorn up arid
look hlsidc, Wc can relate their structure to their bchuvi,,n'
.and draw many lessons Frout a single experiment.
\~c don't have to build I00 copies of, say, a thcoreln
prover, to dcmorsshate statistically that it has not overcome
the combim~toria] explosion of search in the way
hoped t)r. Inspection of the program in the light of a
R:w runs reveals the flaw and lets us proceed to file next
a ttcntpt.
We build computers and prograrns f'or many reasons.
Wc build thern to serve society and as tools For carrying
out the ccJoi} ([)[~ ic tasks of society. But as basic scientists
wc build machines and programs .as a way of discovering
new phenomena and analyzing phenome~m we already
know about. Society often becomes confused about this,
believing dial computers and programs are to be constructed
only tk}r the economic use that can be made of
them (or as intermediate items in a developmental
sequence leading to such use). It needs to understand
that the phenomena surrounding computers are deep
and obscure, requiring much experimentation to assess
their nature, It needs to understand that, as in any
114
science, fine gains thut accrue from stlch experimentatio~l
and unclerstandir~g pay off in the permanent acquisition
oF ncw techniques; and that it is these techniques that
will create the instruments to help society in achieving
its goals.
Our purpose here, however, is not to plead for
understanding f'rom an outside world, ill is to examine
one aspect of our science, the development of' new basic
uuderstandhlg by empirical inquiry. 7his is best done:
by illustrations. We will be pardoned if, presuming upon
the occasion, we choose our examples Qom the area of
our own research. As will become apparent, these
examples involve the whole development off artificial
intelligence, especially in its early years. 3f'hey rest on
much more than our own personal co~tributions. And
even where we have made direct contributions, this has
bee~r doue in cooperation witin others. Our collaborators
have included especially Cliff Shaw, with whom wc
Formed a team of" three through the exciting period of
tire late fifties. But we have also w.orked with a great
many colleagues and students at Carnegie-Mellon
U n ivcrsity.
Time permits taking up just two examples. The first
is the development of the notion off a symbolic system.
The second is die development of the notion of heuristic
search. Both conceptions have deep significance for
uuclerstal~ding how information is processed and how
intelligence is achieved. However, they do not come
close to exhausting the flull scope of artificial intelligence,
though they seem to us to be useful for exhibiting
the nature of fundamental knowledge in this part of
computer science.
I. Symbols and Physical Symbol Systems
One of tile fundamental contributions to knowledge
of computer science has been to explain, at a rather
basic level, what symbols are. This explanation is a
scientific proposition about Nature. It is empirically
derived, with a long and gradual development.
Symbols lie at the root of intelligent action, which
is, of course, the primary topic of artificial intelligence.
For that matter, it is a primary question for all of computer
science. For all information is processed by computers
in the service of ends, and we measure the intelligence
of a system by its ability to achieve stated
ends in the face of variations, difficulties and complexities
posed by the task environment. This general
investment of computer science in attaining intelligence
is obscured when the tasks being accomplished are
Communications March 1976
of Volume 19
the ACM Number 3 
limited in scope, for then the full variations in the environment
car? be accurately foreseen. It becomes more
obvious as we extend cornpttters to more global, complex
and k]~owledgeintensive tasks as we attempt to
nlake them our agents, capable of handling on their
own tile full contingencies of the natura[ world.
Our understanding of tile systems requirements for
intelligent action cnnerges slowly. It is composite, for
no single elementary thing accounts for intelligence in
all its m.anifcstations. There is no "intelligence principle,"
just as there is no "vital principle" that conveys
by its very nature the essence of life. But the lack of a
simple does not imply that there are
no structural requirements for intelligence. One such
requirement is the ability to store and manipulate
symbols. To put the scientific question, we may para:
phrase the title of a famous paper by Warren McCulloch
[1961]: What is a symbol, that intelligence may
use it, and intelligence, that it may use a symbol?
Laws of Qualitative Structure
All sciences characterize the essential nature of the
systems they study. These characterizations are invariably
qualitative in nature, for they set the terms
within which more detailed knowledge can be developed.
Their essence can often be captured in very
short, very general statements. One might judge these
general laws, due to their limited specificity, as making
relatively little contribution to the sum of a science,
were it not for the historical evidence that shows them
to be results of the greatest importance.
The Cell Doctrine in Biology~ A good example of a
law of qualitative structure is the cell doctrine in biology,
which states that the basic building block of all
living organisms is the cell. Cells come in a large variety
of forms, though they all have a nucleus surrounded
by protoplasm, the whole encased by a membrane. But
this internal structure was not, historically, part of the
specification of the cell doctrine; it was subsequent
specificity developed by intensive investigation. The
cell doctrine can be conveyed almost entirely by the
statement we gave above, along with some vague
notions about what size a cell can be. The impact of
this law on biology, however, has been tremendous,
and the lost motion in the field prior to its gradual
acceptance was considerable.
Plate Tectonics in Geology. Geology provides an interesting
example of a qualitative structure law, interesting
because it has gained acceptance in the last decade
and so its rise in status is still fresh in memory. The
theory of plate tectonics asserts that the surface of the
globe is a collection of huge plates--a few dozen in
all which move (at geological speeds) against, over,
and under each other into tile center of the earth,
where they lose their identity. 't"he movements of the
plates account for the shapes and relative locations of
tile continents arid oceans, for tile areas of volcanic
and earthquake activity, for the deep sea ridges, arid
so on. With a few additional particulars as to speed
and size, the essential theory has been specified, it was
of course not accepted until it succeeded in exphfining
a number of details, all of which hung together (e.g.
accounting for flora, fauna, and stratification agreements
between West Africa and Northeast South
America). The plate tectonics theory is highly qualitative,
Now that it is accepted, the whole earth seems to
offer evidence for it everywhere, for we see the world
in its terms.
The Germ Theory of Disease. It is little more than a
century since Pasteur enunciated the germ theory of
disease, a law of qualitative structure that produced a
revolution in medicine. The theory proposes that most
diseases are caused by tile presence and multiplication
in the body of tiny single-celled living organisms, and
that contagion consists :in the transmission of these
organisms from one host to another. A large part of
the elaboration of the theory consisted in identifying
the organisms associated with specific diseases, describing
them, and tracing their life histories. The fact
that the law has many exceptions--that many diseases
are not produced by germs--does not detract from its
importance. The law tells us to took for a particular
kind of cause; it does not insist that we will always
find it.
The Doctrine of Atomism. The doctrine of atomism
offers an interesting contrast to the three laws of qualitative
structure we have just described. As it emerged
from the work of Dalton and his demonstrations that
the chemicals combined in fixed proportions, the law
provided a typical example of qualitative structure:
the elements are composed of small, uniform particles,
differing from one element to another. But because the
underlying species of atoms are so simple and limited
in their variety, quantitative theories were soon formulated
which assimilated all the general structure in
the original qualitative hypothesis. With ceils, tectonic
plates, and germs, the variety of structure is so great
that the underlying qualitative principle remains distinct,
and its contribution to the total theory clearly
discernible.
115 Communications March 1976
of Volume 19
the ACM Number 3 
Co~elusion. Laws of qualitative structure are seen
everywhere in science. Some o[" our greatest scientific
discoveries are to be found among them. As the examples
illustrate, they often set the terms on which a
whole science operates,
Physical Symbol Systems
Let us retur~ to the topic of symbols, and define a
!~04ice/ symbol s3",slem. The adjective "physical" tienotes
two hnportant features: (1) Such systems clearly
obey the laws o{ physics they are realizable by engineered
systems made of engineered cornponerlts; (2)
although our use of the term "symbol" prefigures our
intended interpretation, it is not restricted to human
symbol systems.
A physical symbol system consists of a set o[ entides,
called symbols, which arc physical patterns that
can occur as components of another type of entity
called an expression (or symbol structure). Thus, a
symbol structure is corn.posed of'a number o[' instances
(or tokens) of" symbols related in some physical way
(such as ore: token being next to another). At any
i~stant of time the system will contain a collection of'
d~c, se symbol structures. Besides these structures, tile
system also contains a collectiml of' processes that
operate o~t, expressions to produce other expressions:
process,cs of creation, modification, reproduction and
destructi<m. A physical symbol system is a machine
d~at produces through time an evolving collection of
syntbot structures. Such a system exists in a world of"
objects wider than just these symbolic expressions
themselves.
Two notions are central to this structure o[ expressions,
symbols, and objects: designation and
interprctatio,~.
Desig,talion. An expression designates an object
if, given the e:xpression, the system can either
affect the object itself' or behave in ways dependent
,.m the ,object.
1~ either case, access to tile object via. the expression
has been obtained, which is the essence of
designation.
lnterpre/alimt. The systern can interpret an expression
iI' the express!on designates a process
and if, given the expression, tile system can
carry out the process.
E'~terpretation implies a special form o{" dependent
action : given an expression the system, cart perform the
indicated process, which is to say, it can evoke and
execute its own processes from expressions that designate
them,
A system capable of designation and interpretation,
in the sense just indicated, must also meet a number of
adctitiona] requirenmnts, of completeness and closure.
We will have space only to mention these briefly; all
116
of them are important and have
quences.
(t) A symbol may be used to designate any expres_
sion whatsoever. That is, given a symbol, it is not
prescribed a priori what expressions it can designate.
This arbitrariness pertains only to symbols; the symbol
tokens and their mutual relations detcrmine wJnat object;
is designated by a cornpiex expression. (2) ]'here exist
expressions that designate every process of which t}'~e
machine is capable. (3) There exist processes for creating
any expression and for modifying any expression its
arbitrary ways. (4) Expressions are stable; once created
they will continue to exist until explicitly modified or
deleted. (5) The number of expressions that fine system
can hold is essentially unbounded.
The "type of system we have just defined is not u~>
familiar to computer scientists. It bears a strong family
resemblance to sit general purpose computers. If u.
symbol manipulation language, such as I.lSP, is taken
as defining a machine, then the kinship becomes truly
brotherly. Our intent in laying out such a system is no~
to propose something new. Just the opposite: it is to
show what is now known and hypothesized about
systems that satisf) such a characterization.
We can now state a general scientific hypothesis --a
law of qualitative structure for symbol systems:
The Physical Symbol System Hypothesis. A phys-.
ical symbol system has the necessary and sufl%
cient means for general intelligent action.
By "necessary" we mean that any system that
exhibits general intelligence will prove upon analysis
to be a physical symbol system. By "sufficient" we mear~
that any physical symbol system of sufficient size can
be organized further to exhibit general intelligence. By
"general intelligent action" we wish to indicate the
sarne scope of intelligence as we see in humian a.ctio~a:
that in any real situation behavior approprate to the
ends of the system and adaptive to the demands of the
environment can occur, within som.e limits of speed
and complexity.
The Physical Symbol System Hypothesis clearly is
a law of qualitative structure. It specifies a general class
of systems within which one will find those capable of
intelligent action.
This is an empirical hypothesis. We have defined a
class of systems; we wish to ask whether that class
accounts for a set of phenomena we find in the real
world. Intelligent action is everywhere around us in
the biological world, mostly in human behavior. It is :a
form of behavior we can recognize by its effects whether
it is performed by humans or not. The hypothesis
could indeed be false. Intelligent behavior is not so
easy to produce that any system will exhibit it willynilly,
Indeed, there are people whose analyses lead them
to conclude either on philosophical or on scientific
grounds that the hypothesis is false. Scientifically, one """, [])






encryption = textToDictionnary("""The security of our encryption scheme is based on complexity theory. Thus, when
we say that it is "impossible" for an adversary to compute any information about the
cleartext from the cyphertext we mean that it is not computationally feasible.
The relatively young field of complexity theory has not yet been able to prove a
nonlinear lower bound for even one natural NP-complete problem. At the same time,
despite the enormous mathematical effort, some problems in number theory have for
centuries refused any "domestication." Thus, for concretely implementing our
scheme, we assume the intractability of some problems in number theory such as
factoring or deciding quadratic residuosity with respect to composite moduli. In this
context, proving that a problem is hard means to prove it equivalent to one of the
above mentioned problems. In other words, any threat to the security of the concrete
implementation of our encryption scheme will result in an efficient algorithm for
deciding quadratic residuosity modulo composite integers.
* This research was done when both authors were students at the University of California at Berkeley
and supported in part by NSF Grant MCS 82-04506. The preparation of this manuscript was done when
the first author was at the Laboratory of Computer Science at MIT and supported by a Bantrell
fellowship and an IBM faculty development award, and the second author was at the Computer Science
Department at the University of Toronto.
270
0022-0000/84 $3.00
Copyright 0 1984 by Academic Press, Inc.
All rights of reproduction in any form reserved. 
PROBABILISTIC ENCRYPTION 271
1.1. Deterministic Encryption: The Trapdoor Function Model
Our encryption scheme benefits from the ideas of DifIie and Hellman [9], Rivest,
Shamir, and Adleman [21], and Rabin [20].
Diffie and Hellman [9] introduced the idea of a public key cryptosystem, which is
based on the intractability of some underlying computational problem. Intuitively, the
idea is to find an encryption function E which is easy to compute but difficult to
invert unless some secret information, the trapdoor, is known. Such a function is
called a trapdoor function. To encrypt a message m, anyone simply evaluates E(m),
but only those who know the trapdoor information can compute m from E(m).
The two implementations of a trapdoor function most relevant and inspiring for
this paper are the RSA function [21], due to Rivest, Shamir, and Adleman, and its
particularization suggested by Rabin [ 201.
1.2. Basic Objections to the Trapdoor Function Model
We point out two basic weaknesses of this approach:
(I) The fact that f is a trapdoor function does not rule out the possibility of
computing x from f (x) when x is of a special form. Usually messages do not consist
of numbers chosen at random but possess more structure. Such structural information
may help in decoding. For example, a function f, which is hard to invert on a generic
input, could conceivably be easy to invert on the ASCII representations of English
sentences.
(2) The fact that f is a trapdoor function does not rule out the possibility of
easily computing some partial information about x (even every other bit of x) from
f(x). Encrypting messages in a way that ensures the secrecy of all partial information
is an important goal in cryptography. Assume we want to use encryption to
play card games over the telephone. If the suit or color of a card could be
compromised the whole game should be invalid. Indeed Lipton [ 171 has pointed out
that one bit of information about cards to remain hidden can be easily computed in
the SRA implementation of Mental Poker [22].
Though no one knows how to break the RSA or the Rabin scheme, in none of
these schemes is it proved that decoding is hard without any assumptions made on
the message space. Rabin shows that, in this scheme, decoding is hard for an
adversary if the set of possible messages has some density property. We discuss this
further in Section 2.
1.3. Probabilistic Encryption: The New Model
In this paper we switch from a deterministic framework to a probabilistic
framework. This enables us to deal with the problems that arose with the trapdoor
function model, without imposing any probability structure on the messages we
would like to send. 
272 GOLDWASSER AND MICALI
We replace the notion of a trapdoor function with the notion of an unapproximable
trapdoor predicate. Briefly, the predicate B is trapdoor and unapproximable if anyone
can select an x such that B(x) = 0 or y such that B(y) = 1, but only those who know
the trapdoor information can, given z, compute the value of B(z). When the trapdoor
information is unknown, an adversary with polynomially bounded computational
resources can not decide the value of B(z) better than guessing at random (see
Section 3 for formal definition).
We replace deterministic block encryption by probabilistic encryption of single
bits, where there are many different encodings of a "1" and many different encodings
of a "0." To encrypt each message we make use of a fair coin. Thus the encoding of
each message will depend on the message plus the result of a sequence of coin tosses.
More specifically, a binary message will be encrypted bit-by-bit as follows: a "0" is
encoded by randomly selecting an x such that B(x) = 0 and a "1" is encoded by
randomly selecting an x such that B(x) = 1. Consequently, there are many possible
encodings for each message. However, messages are always uniquely decodable.
Two properties of the new model are:
(1) Decoding is easy for the legal receiver of a message, who knows the
trapdoor information, but provably hard for an adversary. Therefore the spirit of a
trapdoor function is maintained. In addition, in our scheme, we do not impose any
restrictions on the message space. The security of the scheme is proved for messages
belonging to any message space with any probability distribution.
(2) No information about an encrypted message can be obtained by an
adversary.
Let g: M+ V be a nonconstant function m. Assume that the message space M has
some probability distribution. Accordingly, let pv = prob(g(m) = v 1 m E M) for each
v E V, and let fi E V be such that pG = rnaxUEr, pv. Then, without any special ability,
an adversary given the cyphertext, can always guess the value of g over the cleartext
and be correct with probability pE. We prove that for a probabilistic encryption
scheme, an adversary, given the cyphertext, cannot guess the value of g over the
cleartext with probability better than pa. Note that g needs not be polynomially
computable, or even recursive. Thus, our encryption model passes a polynomially
bounded version of Shannon's perfect secrecy definition; see Subsection 7.3.
This property enabled Goldwasser and Micali to device a scheme for Mental
Poker for which, under the Quadratic Residuosity Assumption, no partial information
about cards that should remain hidden can be easily computed.
1.4. Concrete Implementation of the New Model
We introduce Quadratic Residuosity modulo composite integers whose
factorization is unknown (see Section 6 for precise definition), as the first example of
an unapproximable trapdoor predicate. Thus we introduce a new probabilistic public
key cryptosystem that is secure in a very strong probabilistic sense if and only if 
PROBABILISTIC ENCRYPTION 213
deciding quadratic residuosity with composite moduli is hard (see Section 4). The
security offered by this Public Key Cryptosystems extends to all partial information
about encrypted messages, to ail possible message spaces and to all possible
probability distributions for the message space (see Section 5 for formal definition of
security).
Another example of such predicates, has appeared in a Goldwasser, Micah, and
Tong [ 121 and in Goldwasser [ 131. The predicate they propose is unapproximable if
and only if factoring composite numbers is hard. Using the construction of Section 4,
we can build a public key cryptosystem based on the predicate they propose. Again,
any threat to the security of this last cryptosystem, will result in an efficient factoring
algorithm.
In [26], Yao shows that unapproximable trapdoor predicates exist if one-to-one
trapdoor functions exist.
1.5. Related Work
Blum and Micali in [5] showed the first example of an unapproximable predicate
which is not trapdoor. Their predicate is unapproximable if and only if the discrete
logarithm problem is hard.
The quadratic residuosity predicate is not only an example of an unapproximable
trapdoor predicate, but possesses other properties which make it particularly
attractive for protocol design. It has been widely used since we first proposed it in
[lo]. The first protocol that uses this predicate was suggested by Goldwasser and
Micali in [ 111. They design a protocol for two players to play mental poker over the
telephone, so that no player can obtain any partial information about cards not in his
hand. Other works in which this predicate has proved useful are: Blum, Blum, and
Shub's implementation [4] of a cryptographically strong pseudo random bit generator
[5], Brassard's [7] implementation of authentication tags, Luby, Micali, and
Rackoff s [ 191 method for simultaneously exchanging a secret bit, and Vazirani and
Vazirani's [25] implementation of one bit disclosures.
2. SURVEY OF PUBLIC KEY CRYPTOSYSTEMS BASED ON TRAPDOOR FUNCTIONS
All the number theoretic notation used in this section will be defined in Section 3.
2.1. What Is a Public Key Cryptosystem?
The concept of a Public Key Cryptosystem was introduced by Diffie and Hellman
in their ingenious paper [9]. Let M be a finite message space, let {A, B,...} be users,
and let m E M denote a message. Let E,: M + M be A's encryption function, which is
ideally bijective, and D, be A's decryption function such that D,(E,(m)) = m for all
m E M. In a Public Key Cryptosystem E, is placed in a public file, and user A keeps
D, private. D, should be difficult to compute knowing only E,. To send message m 
274 GOLDWASSERAND MICALI
to A, B takes EA from the public file, computes EA(m) and sends this message to A. A
easily computes DA(EA(m)) to obtain m.
2.2. The RSA Scheme and the Rabin Scheme
Two implementations of such encryption functions E, are the RSA function 1211
of Rivest et al. and the Rabin function [20].
The key idea in both the RSA scheme and the Rabin scheme' consists in the
selection of an appropriate number theoretic trapdoor function. In the RSA scheme,
user A selects n, the product of two large distinct primes p, and pz and a number s
such that s and q(n) are relatively prime, where o is the Euler totient function. A puts
rr and s in a public file and keeps the factorization of n private. Let Zz = (x E N:
1 <x < n - 1 and x and n are relatively prime}. For every message m E Zz,
EA(m) = mS mod n. Clearly, the ability to take sth roots mod n implies the ability to
decode. A, who knows the factorization of n, can easily take sth roots mod n. No
efficient way to take sth roots mod n is known when the factorization of n is
unknown.
Rabin suggested to modify the RSA scheme by choosing s = 2. Thus, for all users
A, EA(x) = x2 mod n. Notice that E, is a 4-l function because our n is the product of
two primes. In fact, every quadratic residue mod n, i.e., every q such that
q=x'modn for some XE Z,*, has four square roots mod n: ix mod n and
fy mod n. As A knows the factorization of n, upon receiving the encrypted message
m* mod n, she could easily compute its four square roots and get the message m. (A
may compute square roots mod n by first computing square roots modp, and pz and
then by combining them via the Chinese Remainder Theorem.) The following
heuristics may be suggested for eliminating ambiguity in decoding: for sending a
message m, send m* mod n together with the last 20 bits of m. Such extra information
cannot effectively help in decoding: one could always guess the last 20 digits of m.
(To avoid publicizing the last 20 digits of m, just select a 20-bit random integer r and
send (m2*' + r)' mod n together with r.)
The following theorem shows how hard it is to invert Rabin's funct""", [])










graham = textToDictionnary("""DESCRIPTION

From The Publisher. 
This book introduces the mathematics that supports advanced computer programming and the analysis of algorithms. The primary aim of its well-known authors is to provide a solid and relevant base of mathematical skills - the skills needed to solve complex problems, to evaluate horrendous sums, and to discover subtle patterns in data. It is an indispensable text and reference not only for computer scientists - the authors themselves rely heavily on it! - but for serious users of mathematics in virtually every discipline.

 Concrete mathematics is a blending of CONtinuous and disCRETE mathematics. "More concretely," the authors explains, "it is the controlled manipulation of mathematical formulas, using a collection of techniques for solving problems." The subject matter is primarily an expansion of the Mathematical Preliminaries section in Knuth's classic Art of Computer Programming, but the style of presentation is more leisurely, and individual topics are covered more deeply. Several new topics have been added, and the most significant ideas have been traced to their historical roots. The book includes more than 500 exercises, divided into six categories. Complete  answers are provided for all exercises, except research problems, making the book particularly valuable for self-study.

[ Top ]
PREFACE
This book is based on a course of the same name that has been taught annually at Stanford  University since 1970. About fifty students have taken it each year juniors and seniors, but  mostly graduate students - and alumni of these classes have begun to spawn similar courses  elsewhere. Thus the time seems ripe to present the material to a wider audience (including  sophomores).

It was dark and stormy decade when Concrete Mathematics was born. Long-held values were  constantly being questioned during those turbulent years; college campuses were hotbeds of  controversy. The college curriculum itself was challenged, and mathematics did not escape  scrutiny. John Hammersley had just written a thought-provoking article "On the enfeeblement of  mathematical skills by 'Modern Mathematics' and by similar soft intellectual trash in schools and  universities" [176] ; other worried mathematicians [332] even asked, "Can mathematics be  saved?" One of the present authors had embarked on a series of books called The Art of  Computer Programming, and in writing the first volume he (DEK) had found that there were  mathematical tools missing from his repertoire; the mathematics he needed for a thorough,  well-grounded understanding of computer programs was quite different from what he'd learned  as a mathematics major in college. So he introduced a new course, teaching what he wished  somebody had taught him.

The course title "Concrete Mathematics" was originally intended as an antidote to "Abstract  Mathematics," since concrete classical results were rapidly being swept out of the modern  mathematical curriculum by a new wave of abstract ideas popularly called the "New Math."  Abstract mathematics is a wonderful subject, and there's nothing wrong with it: It's beautiful,  general, and useful. But its adherents had become deluded that the rest of mathematics was  inferior and no longer worthy of attention. The goal of generalization had become so fashionable  that a generation of mathematicians had become unable to relish beauty in the particular, to  enjoy the challenge of solving quantitative problems, or to appreciate the value of technique.  Abstract mathematics was becoming inbred and losing touch with reality; mathematical  education needed a concrete counterweight in order to restore a healthy balance.

When DEK taught Concrete Mathematics at Stanford for the first time he explained the  somewhat strange title by saying that it was his attempt to teach a math course that was hard  instead of soft. He announced that, contrary to the expectations of some of his colleagues, he  was not going to teach the Theory of Aggregates, not Stone's Embedding Theorem, nor even the  Stone-Cech compactification. (Several students from the civil engineering department got up and  quietly left the room.)

 Although Concrete Mathematics began as a reaction against other trends, the main reasons for 
 its existence were positive instead of negative. And as the course continued its popular place in 
 the curriculum, its subject matter "solidified" and proved to be valuable in a variety of new 
 applications. Meanwhile, independent confirmation for the appropriateness of the name came 
 from another direction, when Z.A. Melzak published two volumes entitled Companion to 
 Concrete Mathematics [267].

The material of concrete mathematics may seem at first to be a disparate bag of tricks, but  practice makes it into a disciplined set of tools. Indeed, the techniques have an underlying unity  and a strong appeal for many people. When another one of the authors (RLG) first taught the  course in 1979, the students had such fun that they decided to hold a class reunion a year later.

But what exactly is Concrete Mathematics? It is a blend of continuous and discrete  mathematics. More concretely, it is the controlled manipulation of mathematical formulas, using  a collection of techniques for solving problems. Once you, the reader, have learned the material  in this book, all you will need is a cool head, a large sheet of paper, and fairly decent handwriting  in order to evaluate horrendous-looking sums, to solve complex recurrence relations, and to  discover subtle patterns in data. You will be so fluent in algebraic techniques that you will often  find it easier to obtain exact results than to settle for approximate answers that are valid only in  a limiting sense.

The major topics treated in this book include sums, recurrences, elementary number theory,  binomial coefficients, generating functions, discrete probability, and asymptotic methods. The  emphasis is on manipulative techniques rather than on existence theorems or combinatorial  reasoning; the goal is for each reader to become as familiar with discrete operation (like the  greatest integer function and finite summation) as a student of calculus is familiar with  continuous operations (like the absolute-value function and infinite integration)

Notice that this list of topics is quite different from what is usually taught nowadays in  undergraduate course entitled "Discrete Mathematics." Therefore the subject needs a distinctive  name, and "Concrete Mathematics" has proved to be as suitable as another

The original textbook for Stanford's course on concrete mathematics was the "Mathematical  Preliminaries" section in The Art of Computer Programming [207]. But the presentation in those  110 pages is quite terse, so another author (OP) was inspired to draft a lengthy set of  supplementary notes. The present book is an outgrowth of those notes; it is an expansion of, and  a more leisurely introduction to, the material if Mathematical Preliminaries. Some of the more  advanced parts have been omitted; on the other hand, several topics not found there have been  included here so that the story will be complete

The authors have enjoyed putting this book together because the subject began to jell and to take  on a life of its own before our eyes; this book almost seemed to write itself. Moreover, the  somewhat unconventional approaches we have adopted in several places have seemed to fit  together so well, after these years of experience, that we can't help feeling that this book is a  kind of manifesto about our favorite way to do mathematics. So we think the book has turned  out to be a tale of mathematical beauty and surprise, and we hope that our readers will share at  least of the pleasure we had while writing it.

Since this book was born in a university setting, we have tried to capture the spirit of a  contemporary classroom by adopting an informal style. Some people think that mathematics is a  serious business that must always be cold and dry; but we think mathematics is fun, and we  aren't ashamed to admit the fact. Why should a strict boundary line be drawn between work and  play? Concrete mathematics is full of appealing patterns; the manipulations are not always easy,  but the answers can be astonishingly attractive. The joy and sorrows of mathematical work are  reflected explicitly in this book because they are part of our lives.

Students always know better than their teachers, so we have asked the first students of this  material to contribute their frank opinions, as "graffiti" in the margins. Some of these marginal  markings are merely corny, some are profound; some of them warn about ambiguities or  obscurities, others are typical comments made by wise guys in the back row; some are positive,  some are negative, some are zero. But they all are real indications of feelings that should make  the text material easier to assimilate. (the inspiration for such marginal notes comes from a  student handbook entitled Approaching Stanford, where the official university line is  counterbalanced by the remarks of outgoing students. For example, Stanford says, "There are a  few things you cannot miss in this amorphous .. what the h*** does that mean? Typical of the  pseudo-intellectualism around her." Stanford: There is no end to the potential of a group of  students living together." Graffito: "Stanford dorms are like zoos without a keeper."

The margins also include direct quotations from famous mathematicians of past generations,  giving the actual words in which they announced some of their fundamental discoveries.  Somehow it seems appropriate to mix the words of Leibniz, Euler, Gauss, and others with those  of the people who will be continuing the work. Mathematics is an ongoing endeavor for people  everywhere; many strands are being woven into one rich fabric.

 This book contains more than 500 exercises, divided into six categories:

 1.Warmups are exercises that every reader should try to do when first reading the material. 
 2.Basics are exercises to develop facts that are best learned by trying one's own derivation  rather than by reading     somebody else's. 
 3.Homework exercises are problems intended to deepen an understanding of material in the  current chapter. 
 4.Exam problems typically involve ideas from two or more chapters simultaneously; they  are generally intended for use in take-home exams (not for in-class exams under time  pressure). 
 5.Bonus problems go beyond what an average student of concrete mathematics is expected  to handle while taking a course based on this book; they extend the text in interesting  ways. Bonus problems go beyond what an average student of concrete mathematics is  expected to handle while taking a course based on this book; they extend the text in  interesting ways. 
 6.Research problems may or may not be humanly solvable, but the ones presented here  seen to be worth a try (without time pressure).

Answers to all the exercises appear in Appendix A, often with additional information about  related results. (Of course the "answers" to research problems are incomplete; but even in these  cases, partial results or hints are given that might prove to be helpful.) Readers are encouraged  to look at the answers especially the answers to the warmup problems, but only after making a  serious attempt to solve the problems without peeking.

We have tried in Appendix C to give proper credit to the sources of each exercise, since a great  deal of creativity and/or luck often goes into the design of an instructive problem.  Mathematicians have unfortunately developed a tradition of borrowing exercises without an  acknowledgment; we believe that the opposite tradition, practiced for example books and  magazines about chess (where names, dates, and location of original chess problems are  routinely specified) is far superior. However, we have not been able to pin down the sources of  many problems that have become part of the folklore. If any reader knows the origin of an  exercise for which our citation is missing or inaccurate, we would be glad to learn the details so  that we can correct the omission in subsequent editions of this book.

The typeface used for mathematics throughout this book is a new design by Hermann Zapf  [227], commissioned by the American Mathematical Society and developed with the help of a  committee that included B. Beeton, R.P. Boas. L.K. Durst, D. E. Knuth, P. Murdock, R.S.  Palais, P Renz, E. Swanson, S.B. Whidden and W.B. Woolf. The underlying philosophy of  Zapf's design is to capture the flavor of mathematics as it might be written by a mathematician  with excellent handwriting. A handwritten rather than mechanical style is appropriate because  people generally create mathematics with pen, pencil, or chalk. (For example, one of the  trademarks of the new design is the symbol for zero, 'O', which is slightly pointed at the top  because a handwritten zero rarely closes together smoothly when the curve returns to its  starting point.) The letters are upright, not italic, so the subscripts, superscripts, and accents are  more easily fitted with ordinary symbols. This new type of family has been named AMS Euler,  after the great Swiss mathematician Leonhard Euler (1707-1783) who discovered so much of  mathematics as we know it today. The alphabets include Euler Text, Euler Fraktur, and Euler  Script Capitals, as well as Euler Greek and special symbols such as <p> and <N>. We are  especially pleased to be able to inaugurate the Euler Family of typefaces in this book, because  Leonhard Euler's spirit truly lives on every pare: Concrete mathematics is Eulerian mathematics.

The authors are extremely grateful to Andrei Broder, Ernst Mayr, Andrew Yao, and Frances  Yao, who contributed greatly to this book during the years that they taught Concrete  Mathematics at Stanford. Furthermore we offer 1024 thanks to the teaching assistants who  creatively transcribed what took place in class each year and who helped to design the  examination questions; their names are listed in Appendix C. This book, which is essentially a  compendium of sixteen years' worth of lecture notes, would have been impossible without their  first-rate work.""", [])







list_dic_freq = [weiser, newell, encryption, graham] 
list_titles= ["weiser", "newell", "encryption", "graham"]
dic = linkWordDocFreq(list_dic_freq, list_titles)

u = create_matrix(dic, list_titles)
m=u[0]
n = create_matrix2(dic, list_titles)

l = []
t0 = time.clock()
for i in range(len(m)):
    for j in range(len(m[0])) :
        l.append(accessMatrix(m,i,j))
print("La premiere methode met en secondes :")
print time.clock() - t0

p=[]
t0 = time.clock()
for i in range(len(m)):
    for j in range(len(m[0])) :
        p.append(accessMatrix2(n,i,j))
print("La deuxieme methode met en secondes :")
print time.clock() - t0




        
        
