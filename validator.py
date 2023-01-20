import xml.etree.ElementTree as ET
import re
from html.parser import HTMLParser
from collections import defaultdict
from functools import reduce
import json

# https://www.geeksforgeeks.org/defaultdict-in-python/

# https://stackoverflow.com/questions/44542853/how-to-collect-the-data-of-the-htmlparser-in-python-3
class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.d = []
        super().__init__()
     

    def handle_data(self, data):
        #some hispanic white space https://stackoverflow.com/questions/10993612/how-to-remove-xa0-from-string-in-python
        self.d.append(data.replace(u'\xa0', u' ')) 
        return (data)

    def return_data(self):
        # maybe zero it, check if

        result = self.d
        self.d =[]
        return result



class Vertex:
    def __init__(self, id, content, prodType, color, xPosition, yPosition):
        self.id = id
        self.content = content
        self.prodType = prodType
        self.color = color
        self.x = xPosition
        self.y = yPosition

    def show(self):
        print("Vertex:","\n\tid:", self.id,"\tid:", self.id,"\n\tcontent:", self.content,"\n\ttype:", self.prodType, "\n\tcolor",self.color)

# types constant
missionProductionType= "mission"
genericProductionType = "generic"
detailedProductionType = "detailed"
endingProductionType = "ending"

class Edge:
    def __init__(self, fromId, toId, edgeId):
        self.source = fromId
        self.target = toId
        self.edgeId = edgeId

    def show(self):
        print("Edge from ",self.source," to ",self.target)






def parseEdge():



    return







# https://regex101.com/
missionProductionRegex = "^\(\s?(\w\s*)+[?|!]?\s?,\s?Q[0-9]+\s?(\)\s?)$"
genericProductionRegex ="\s?([A-z-’`']+\s)+\s?/\s([A-ząćĆęłŁńóÓśŚżŻźŹ-’`']+\s?)+\;\s?\((\s?([A-z_/’`'])+\s?,)*\s?([A-z_/’`'])+\s?\)"
detailedProductionRegex = "s?([A-z-’`']+\s)+\s?/\s?([A-ząćĆęłŁńóÓśŚżŻźŹ\-’`']+\s?)+"

# [\l\u] potestować - wsyztskie literki

allowedColorDictionary = defaultdict()
allowedColorDictionary[missionProductionType] ="#e1d5e7"
allowedColorDictionary[genericProductionType] = {"#ffffff","none"}
allowedColorDictionary[detailedProductionType] ="#d5e8d4"
allowedColorDictionary[endingProductionType] = {"#fff2cc","#000000","#ffffff","#e1d5e7","none","none;"}


allowedDetailProductionSet = {}
allowedMissionProductionSet={}


def loadFromJson(filename):

    file = open(filename)
    data = json.load(file)
    return data

def isVertexColorCorrect(vertex:Vertex):
    """
    checks if Vertex class instance color attribute is adequate to its type
    :param vertex:Vertex Vertex class instance
    :return: Boolean, True if color is correct, false if
    """
    if(vertex.prodType == missionProductionType):
        return vertex.color == allowedColorDictionary[missionProductionType]

    if(vertex.prodType == genericProductionType):
        return vertex.color in allowedColorDictionary[genericProductionType]

    if(vertex.prodType == detailedProductionType):
        return vertex.color == allowedColorDictionary[detailedProductionType]

    if(vertex.prodType == endingProductionType):
        return vertex.color in allowedColorDictionary[endingProductionType]

'''
parsing color
'''
def parseColor(style):
    """
    Scans path recursively and looks for files with .json extensions.
    :param mask: pattern of file names taken into consideration
    :param path: folder path name
    :return: list of the files in folder according to the pattern
    """
    # print(style)
    fillColorTag ="fillColor"
    hexColorLen = 7 # with #xxxxxx
    if style.find(fillColorTag) == -1:
        return "none" # throw later iif its problem


    begColorIndex = style.index(fillColorTag) + len(fillColorTag) +1 
    endColorIndex = begColorIndex + hexColorLen
    

    return style[begColorIndex:endColorIndex]

'''

'''
def mayBeGeneric(production):
    slashIndex = production.find("/")
    if(slashIndex == -1):
        # print("not generic (no slash /)")
        return False
    
    beforeSlashRegex ="\s?([A-z\-’`']+\s)+\s?"
    if(not bool(re.search(beforeSlashRegex,production[0:slashIndex]))):
        # print("content before slash not compliant to ", beforeSlashRegex)
        return False
    
    # print("before slash:__", production[0:slashIndex])

    semicolonIndex  = production.find(";")

    if(semicolonIndex == -1):
        # print("not generic (no ;)")
        return False

    slashToSemicolon = production[slashIndex:semicolonIndex+1] 
    slashToSemicolonRegex = "/\s([A-ząćĆęłŁńóÓśŚżŻźŹ\-’`']+\s?)+\;"

    if(not bool(re.search(slashToSemicolonRegex,slashToSemicolon))):
        # print(slashToSemicolon," content from / to ; not compliant to ", slashToSemicolonRegex)
        return False
    # print("slash to semi:__", slashToSemicolon)


    bracketsPart = production[semicolonIndex+1:]
    bracketsRegex ="\s?\((\s?([A-z_/’`'])+\s?,)*\s?([A-z_/’`'])+\s?\)"
    if(not bool(re.search(bracketsRegex,bracketsPart))):
        # print(bracketsPart," content from ;+1 to end not compliant to ", bracketsRegex)
        return False
    # print("brackets part:__", bracketsPart)

    # print(" is generic")
    return True





allowedGenericProductionList = loadFromJson("./produkcje_generyczne.json")
allowedCharactersList= loadFromJson("./allowedCharacters.json")
allowedItemsList = loadFromJson("./allowedItems.json")
allowedLocationsList= loadFromJson("./allowedCharacters.json")







# START

tree = ET.parse('./q00_DragonStory_diagram projektowy.drawio.xml')
# tree = ET.parse('./not _reaching _end_diargam.xml')

root = tree.getroot()



parser = MyHTMLParser() 


vertexStore = [] # later to be substituted by vertexmap when connection verification
edgeMap = defaultdict() # key is sourceid, value are all Edge entities with this source and some target
edgeStore = [] # good for looking for starig vertex

# READING XML

mainStoryX= 0
mainStoryY= 0
mainStoryEndX =0
mainStoryEndY =0

mainStoryWidth= 0
mainStoryHeight= 0


for elem in root.iter('mxCell'):


    if "edge" in elem.attrib:
        # print("\n\nelemą ", elem.attrib,"\n\n")
        edgeStore.append(Edge(
                elem.attrib["source"],
                elem.attrib["target"],
                elem.attrib["id"]
            ))


        print(elem.attrib["source"])
        print(edgeMap.get(elem.attrib["source"]))
        if not bool(edgeMap.get(elem.attrib["source"])):
            edgeMap[elem.attrib["source"]] = []
            edgeMap[elem.attrib["source"]].append(
                Edge(
                elem.attrib["source"],
                elem.attrib["target"],
                elem.attrib["id"]
            ))
            continue

        edgeMap[elem.attrib["source"]].append(
            Edge(
            elem.attrib["source"],
            elem.attrib["target"],
            elem.attrib["id"]
        ))
        continue




    if "vertex" in elem.attrib:

        if "ellipse" in elem.attrib["style"]:

            #if value then it should hav mission no
            if "value" in elem.attrib and not elem.attrib["id"] == "":
                if( bool(re.search("\s?[1-9][0-9]?\s?",elem.attrib["value"]))):
                    vertexStore.append(
                    Vertex(elem.attrib["id"],
                    elem.attrib["value"],
                    endingProductionType,
                    parseColor(elem.attrib["style"]),
                    0,
                    0
                )) 
            else:
                raise Exception('Unexpected value in ending production (not a mission number), check id: {}'.format(elem.attrib["id"]))


            vertexStore.append(
                Vertex(elem.attrib["id"],
                "",
                endingProductionType,
                parseColor(elem.attrib["style"]),
                0,
                0
            )
            )




            continue # to not vertex it again

        if "#fff2cc" in elem.attrib["style"] and mainStoryWidth==0 and ("ellipse" not in elem.attrib["style"]):
            for geometry in elem.iter('mxGeometry'):
                mainStoryX = geometry.attrib['x']
                mainStoryY = geometry.attrib['y']
                mainStoryWidth = geometry.attrib['width']
                mainStoryHeight = geometry.attrib['height']
                
            # masz juz width, stad dodaj walidacje
            # print("probably main story, skip") # TODO SPRAWDZIC CZY JEST 1 - szerokość, wysokość, czy ma polacenie, nie powinine
            continue



        parser.feed(elem.attrib["value"])
        for geometry in elem.iter('mxGeometry'):
            xPos = geometry.attrib['x']
            yPos = geometry.attrib['y']

            

        
        vertexStore.append(
            Vertex(elem.attrib["id"],
            reduce(lambda a,b: a+b,parser.return_data()),
            "type",
            parseColor(elem.attrib["style"]),
            xPos,
            yPos
            )
        )
        continue


# exit(0)




# is alligned in main story check:
# mainStoryFirstXValue = [] # none until found first, then
# for x in vertexStore:
    
#     mainStoryX
#     if ( x.x > mainStoryX) and ( x.y > mainStoryY) and ( x.x < mainStoryEndX) and (x.y <mainStoryEndY):
#         if len(mainStoryFirstXValue >0):
#             if x.x !=

#continue from HERE 18:14




for x in vertexStore:
   
    # final already assigned

    if(mayBeGeneric(x.content)):
        x.prodType = genericProductionType
        # x.show()
        print(" is generic")
        continue
    
    if(bool(re.search(missionProductionRegex,x.content))):
        x.prodType = missionProductionType
        # x.show()
        print("is mission")
        continue
    
    if(bool(re.search(detailedProductionRegex,x.content))):
        x.prodType = detailedProductionType
        # x.show()
        print("is detailed")
        continue
   
    print("is ",x.prodType)
    # x.show()
    # print("\n")
print("\n\nend\n\n\n")

# print że nie ma typu


def separateArgsFromBrackets(argsInBrackets):
    argsList = []

    argsInBrackets = argsInBrackets.strip()
    argsInBrackets = argsInBrackets.replace("(","")
    # print("S",argsInBrackets)
    # argsInBrackets = argsInBrackets.strip()
    while "," in argsInBrackets:
        argsInBrackets = argsInBrackets.strip()
        commaAt = argsInBrackets.find(",")
        argsList.append(
            argsInBrackets[0:commaAt].strip()
        )
        argsInBrackets = argsInBrackets[commaAt+1:]

    #end of commas - 
    argsInBrackets = argsInBrackets.replace(")","").strip()

    argsList.append(argsInBrackets)
    return argsList




# verify color, generic (content), production list vs actual
def isGenericProductionAllowed(production,allowedList):
    #use on already regex verified prods
    # check if has type, is on list, with generic extra check of arguments vs allowed items places etc
    begIndex = 0
    if production[0] == " ":
        begIndex = 1
    
    semicolonIndex = production.find(";")

    if production[semicolonIndex] ==" ":
        semicolonIndex -=1 #whittespace before ;
    
    titlePart = production[begIndex:semicolonIndex]
    isOnList = False

    for p in allowedList:
        if p["Title"] == titlePart:
            isOnList = True
            print("on list",production)
    # print(titlePart)
    #czas na odczyt argumentów i edge, continue here

    if not isOnList:

        print("not on list", titlePart)
        raise Exception('Generic production: {} not on list'.format(titlePart))
        
        return False

    # TODO BRACKET PART - tyle samo argumentów,przedmitoów, postać, tyle postaci ile postaci, czy lokacja w zakresie nazw, niekoniecznie kolejność, dowolna kolejnosc dziala



    # found record on list
    # now isolate bracket part
    bracketPart = production[semicolonIndex+1:]
    bracketPart = bracketPart.strip()
    print(bracketPart)
    print(separateArgsFromBrackets(bracketPart))

    argsInBrackets = separateArgsFromBrackets(bracketPart)

    for arg in argsInBrackets:
        if (arg not in allowedCharactersList) and (arg not in allowedItemsList) and (arg not in allowedLocationsList) : 
            if "/" in arg:
                print(arg,"make sure all arguments are of same kind and allowed in ", production)
            else:
                print(arg,"is not on allowed list")

    # count args
    commaCount = bracketPart.count(',')
    if (commaCount != 0):
        argsCount = commaCount + 1
    else:
        argsCount = 1

    print(argsCount, " args")



    # TODO continue validation
    # 1 arg case - hard to recognise, for manual check
    



    charactersCount = 0
    itemsCount = 0
    connectionsCount =0
    for p in allowedList: 
        if p["Title"] in titlePart:
            loc = p["LSide"]
            # print(p["Title"],"\n","\npe",loc,"\n")
            # print("\n",loc["Locations"],"\nep\n")
            characsloc = loc["Locations"]
            print("characters ", len(characsloc[0]["Characters"]))
            for i in characsloc[0]["Characters"]:
                charactersCount += 1
                if("Items" in  i ):
                    itemsCount += len(i["Items"])
                    print(i["Id"]," ",i["Items"])
                    for item in i["Items"]:
                        print("itek",item)

            # print("cons",) 
            if "Connections" in characsloc[0]:
                print("cons",characsloc[0]["Connections"])
                if len(characsloc[0]["Connections"]) > 0:
                    # connectionsCount += 1
                    connectionsCount += len(characsloc[0]["Connections"]) 

            if "Items" in characsloc[0]:
                if len(characsloc[0]["Items"]) > 0:
                    itemsCount += len(characsloc[0]["Items"])

            if charactersCount + itemsCount + connectionsCount != argsCount:
                if argsCount == 1:
                    print("not checking, 1 item") # with one item its hard to count args, check on user side

                elif "Fight" in production:
                    print("fight ars, not checking,") # with fitght its hard to count args, as player flees to location outside not in args check on user side


                # print("TUTAJ")
            # print("args ",argsCount," ",charactersCount+itemsCount+connectionsCount)
            # print("args ",argsCount," ",charactersCount+itemsCount)




    return True




# color and generic prod validation
print("\n\n\n\n\n")


for x in vertexStore:
    # x.show()
    # print(x.prodType)
    print(isVertexColorCorrect(x))
    if(x.prodType == genericProductionType):
        # print(x.content)

        # isGenericProductionAllowed(x.content,allowedGenericProductionList)
        print("allowed ",isGenericProductionAllowed(x.content,allowedGenericProductionList)) # later delete)



print("\n\n\n\n\n")


# exit(0)


# check edge fitting
vertexMap = defaultdict()
#to map
for v in vertexStore:
    vertexMap[v.id] = v
    vertexMap[v.id].show()

print("\n\nnow\n\n\n")

for v in vertexMap.values():
    print(v.id)
    if not bool(edgeMap.get(v.id)):
        if v.prodType != endingProductionType:
            print(" production ",v.id," ",v.content, "is not a source throw EXCEPTION")
        #     v.show()
        print("ending is not a source")
        v.show()

    if bool(edgeMap.get(v.id)) and v.prodType == endingProductionType:
        print("ending ",v.id, " is a source, validate is it should be")
    # for e in edgeMap.get(v.id):
    #     e.show()

print("\n\n\n\n\n")


suspectedStartingVertex = [] #if there are two, find out, only ids
# go trough all and update at ocurrence

suspectedStartingVertex = list(edgeMap.keys())

for edgeList in edgeMap.values():

    for edge in edgeList:
        
        for suspect in suspectedStartingVertex:
            if suspect == edge.target:
                suspectedStartingVertex.remove(suspect)



print(suspectedStartingVertex)

if(len(suspectedStartingVertex) == 0):
    print("no starting Vertex found")
    #raise exception - ostrzec czy musi byc wejsciowa

if(len(suspectedStartingVertex) > 1):
    print("more than one vertex is entrypoint (more than one edge id is not edge target)", suspectedStartingVertex)
    #raise exception/ tutaj tylko ostrzec ze > 1


def findStartingVertexBy(edgeMap):
    return








# check if from every edge is some sort of way to ending, maybe dfs
# foundEnding is false at beg

foundEnding = [False] # to keep reference


# visted list and current vertex are



def getNeighboursIds(vertexId, edgeMap):
    # print("checkup ", vertexId)
    neigboursList = edgeMap.get(vertexId)
    neigboursIdList = []
    # print(neigboursList)

    if bool(neigboursList):
        for e in neigboursList:
            neigboursIdList.append(e.target)
    else:
        neigboursIdList = []

    return neigboursIdList



# returns true if reached any ending from starting edge
# found ending is array with one boolean to keep track of reference
def dfsToEnding(vertexMap, edgeMap, visitedList, foundEnding, currentVertex):

    
    
    visitedList.append(currentVertex) # jst string vertex key

    neighboursIds = getNeighboursIds(currentVertex,edgeMap)

    # print(currentVertex)

    if( vertexMap.get(currentVertex).prodType == endingProductionType):
        print("found some ending: ")
        vertexMap.get(currentVertex).show()
        foundEnding[0] = True

    if foundEnding[0]:
        return True # found an ending from vertex

    for vId in neighboursIds:
        if foundEnding[0]:
            return True 

        if vId not in visitedList:
            return dfsToEnding(vertexMap,edgeMap,visitedList,foundEnding,vId)

    if foundEnding[0]:
        return True # found an ending from vertex

    # if( vertexMap.get(currentVertex).prodType == endingProductionType):
    #     foundEnding = True

    # if foundEnding:
    #     return True # found an ending from vertex
    


    return "\nDID NOT REACHxd\n"


print("\n\n\n")
# print(getNeighboursIds("0h0rLAMfrDWNozQSX6OC-1",edgeMap))

# edgeMap.get("8mZ_FmGga-K4OqEKXEgO-4").show() # its a list


print("\n\n\n")

visitedList = []
foundEnding = [False]


print("\n\n\n")
print("\n\n\n")
print("RESULT DFS\n\n\n")

print(dfsToEnding(vertexMap,edgeMap,visitedList,foundEnding,"0h0rLAMfrDWNozQSX6OC-1"))

print("\n\n\n")
print("\n\n\n")


for v in vertexStore:
    visitedList = []
    foundEnding = [False]

    if v.prodType != endingProductionType:
        # dfsToEnding(vertexMap,edgeMap,visitedList,foundEnding,v.id)
        print(v.content, "can reach some ending: ",dfsToEnding(vertexMap,edgeMap,visitedList,foundEnding,v.id))
    



