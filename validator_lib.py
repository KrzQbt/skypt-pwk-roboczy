
import xml.etree.ElementTree as ET
import re
from html.parser import HTMLParser
from collections import defaultdict
from functools import reduce
import json
import sys
from typing import List



# https://stackoverflow.com/questions/44542853/how-to-collect-the-data-of-the-htmlparser-in-python-3
class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.d = []
        super().__init__()
     

    def handle_data(self, data):
        #some hispanic white space https://stackoverflow.com/questions/10993612/how-to-remove-xa0-from-string-in-python
        data = data.replace('&amp;', '&')
        data = data.replace(u'\xa0', u' ')
        
        self.d.append(data)
        # self.d.append(data.replace(u'\xa0', u' '))
        return (data)

    def return_data(self):
        result = self.d

        self.d =[]

        return result

def loadFromJson(filename):

    file = open(filename)
    data = json.load(file)
    return data

class Vertex:
    def __init__(self, id, content, prodType, color, xPosition, yPosition):
        self.id = id
        self.content = content
        self.prodType = prodType
        self.color = color
        self.x = xPosition
        self.y = yPosition

    def show(self):
        print("Vertex:","\n\tid:", self.id,"\tid:", self.id,"\n\tcontent:", self.content,"\n\ttype:", self.prodType, "\n\tcolor",self.color,"\n\txPos:",self.x,"\n\tyPos:",self.y)

class Edge:
    def __init__(self, fromId, toId, edgeId):
        self.source = fromId
        self.target = toId
        self.edgeId = edgeId

    def show(self):
        print("Edge from ",self.source," to ",self.target)

class MainStoryProps:
    def __init__(self, mainStoryX, mainStoryY, mainStoryWidth,mainStoryHeight,mainStoryEndX,mainStoryEndY):
        self.x = mainStoryX
        self.y = mainStoryY
        self.width = mainStoryWidth
        self.height = mainStoryHeight
        self.endX = mainStoryEndX
        self.endY = mainStoryEndY 





def isVertexColorCorrect(vertex:Vertex, vertexTypesList, vertexColorDict):
    """
    checks if Vertex class instance color attribute is adequate to its type
    :param vertex:Vertex Vertex class instance
    :return: Boolean, True if color is correct, false if
    """

    for type in vertexTypesList:
        if(vertex.prodType == type):
            return vertex.color.lower() in vertexColorDict[type]
    
    return False


def mayBeGeneric(production):

    """
    checks if production (content from vertex) suffices regular expressions for generic type
    :param mask: pattern of file names taken into consideration
    :return: Boolean
    """
    slashIndex = production.find("/")
    if(slashIndex == -1):
        return False
    
    beforeSlashRegex ="\s?([A-z\-’`',]+\s)+\s?"
    if(not bool(re.search(beforeSlashRegex,production[0:slashIndex]))):
        return False
    

    semicolonIndex  = production.find(";")

    if(semicolonIndex == -1):
        return False

    slashToSemicolon = production[slashIndex:semicolonIndex+1] 
    slashToSemicolonRegex = "/\s([A-ząćĆęłŁńóÓśŚżŻźŹ\-’`',]+\s?)+\;"

    if(not bool(re.search(slashToSemicolonRegex,slashToSemicolon))):
        return False


    bracketsPart = production[semicolonIndex+1:]
    bracketsRegex ="\s?\((\s?([A-z_/’`'])+\s?,)*\s?([A-z_/’`'])+\s?\)"
    if(not bool(re.search(bracketsRegex,bracketsPart))):
        return False

    return True



def separateArgsFromBrackets(argsInBrackets):
    argsList = []

    argsInBrackets = argsInBrackets.strip()
    argsInBrackets = argsInBrackets.replace("(","")

    while "," in argsInBrackets:
        argsInBrackets = argsInBrackets.strip()
        commaAt = argsInBrackets.find(",")
        argsList.append(
            argsInBrackets[0:commaAt].strip()
        )
        argsInBrackets = argsInBrackets[commaAt+1:]

    argsInBrackets = argsInBrackets.replace(")","").strip()

    argsList.append(argsInBrackets)
    return argsList




def isGenericProductionAllowed(production,genericProductionList, charactersList,itemsList,locationsList, testResultList):
    begIndex = 0
    if production[0] == " ":
        begIndex = 1
    
    semicolonIndex = production.find(";")

    if production[semicolonIndex] ==" ":
        semicolonIndex -=1 #whittespace before ;
    
    titlePart = production[begIndex:semicolonIndex]
    isOnList = False
    
    for p in genericProductionList:
        if p["Title"] == titlePart:
           
            isOnList = True

    if not isOnList:
        
        if "`" in production or "'" in production:
            testResultList.append("ERROR\n\t" +production + "\n\tGeneric production was not found on allowed generic productions list, check for accidental ' apostrophes, (maybe ’)")
        else:
            testResultList.append("ERROR\n\t" +production + "\n\tGeneric production was not found on allowed generic productions list, check for spelling mistakes" )
        
        return False


    bracketPart = production[semicolonIndex+1:]
    bracketPart = bracketPart.strip()

    argsInBrackets = separateArgsFromBrackets(bracketPart)

    for arg in argsInBrackets:
        if (arg not in charactersList) and (arg not in itemsList) and (arg not in locationsList) : 
            if "/" in arg:
                testResultList.append("WARNING\n\t" +production+"\n\t(triggered by '/') for " +arg+" make sure all arguments are of same kind and allowed on list , if they are, ignore warning")
                # 
            else:
                testResultList.append("ERROR\n\t" +production + "\n\t"+arg+" is not on allowed Characters/Items/Locations list, check for spelling mistakes")

    # count args
    commaCount = bracketPart.count(',')
    if (commaCount != 0):
        argsCount = commaCount + 1
    else:
        argsCount = 1

    charactersCount = 0
    itemsCount = 0
    connectionsCount =0


    for p in genericProductionList: 
        if p["Title"] in titlePart:
            loc = p["LSide"]
            characsloc = loc["Locations"]
            
            for i in characsloc[0]["Characters"]:
                charactersCount += 1
                if("Items" in  i ):
                    itemsCount += len(i["Items"])

            if "Items" in characsloc[0]:
                for i in characsloc[0]["Items"]:
                    charactersCount += 1
                    if("Items" in  i ):
                        itemsCount += len(i["Items"])
                        


            if "Location change" in production:
                if(argsCount == 2):
                    return True
            if "Picking item" in production or "Dropping item" in production:
                if(argsCount == 1):
                    return True

            if charactersCount + itemsCount + connectionsCount != argsCount:
                if argsCount == 1:
                    testResultList.append("WARNING\n\t" +production+"\n\tCheck amount of args in production " )

                elif "Location change" in production:
                    testResultList.append("WARNING\n\t" +production+"\n\tCheck amount of args in production " )
                else:
                    testResultList.append("WARNING\n\t" +production+"\n\tCheck amount of args in production, expected " + str(charactersCount + itemsCount + connectionsCount) + ", but got " + str(argsCount) )



    return True


def parseColor(style):
    """
    find color bycolor string from style cropped from drawing xml
    :param style: attrib["style"] from drawing
    :return: string color
    """
    fillColorTag ="fillColor"
    hexColorLen = 7 # with #xxxxxx
    if style.find(fillColorTag) == -1:
        return "none" 


    begColorIndex = style.index(fillColorTag) + len(fillColorTag) +1 
    endColorIndex = begColorIndex + hexColorLen
    

    return style[begColorIndex:endColorIndex]


def getNeighboursIds(vertexId, edgeDict):
    # print("checkup ", vertexId)
    neigboursList = edgeDict.get(vertexId)
    neigboursIdList = []
    # print(neigboursList)

    if bool(neigboursList):
        for e in neigboursList:
            neigboursIdList.append(e.target)
    else:
        neigboursIdList = []

    return neigboursIdList


def dfsToEnding(vertexDict, edgeDict, visitedList, foundEnding, currentVertex):
    
    visitedList.append(currentVertex) 

    neighboursIds = getNeighboursIds(currentVertex,edgeDict)

    endingProductionType = "ending"


    if( vertexDict.get(currentVertex).prodType == endingProductionType):
        foundEnding[0] = True

    if foundEnding[0]:
        return True # found an ending from vertex

    for vId in neighboursIds:
        if foundEnding[0]:
            return True 

        if vId not in visitedList:
            return dfsToEnding(vertexDict,edgeDict,visitedList,foundEnding,vId)

    if foundEnding[0]:
        return True # found an ending from vertex


    return False





def readEdgesAndVertexFromXml(drawingFileLocation, vertexListToFill, edgeListToFill, edgeDictToFill, mainStoryPropsToFill, testResultList, notAllowedShapesList):
    tree = ET.parse(drawingFileLocation)
    root = tree.getroot()
    parser = MyHTMLParser() 
    mainStoryWidth= 0


    endingProductionType = "ending"

    for elem in root.iter('mxCell'):
        if "edge" in elem.attrib:

            if(("source" not in elem.attrib ) or ("target" not in elem.attrib)):
                testResultList.append(
                    'ERROR\n\tedge with id ' + str(elem.attrib["id"]) +"\n\tis not connected to source or target properly"
                )
                # foundAtLeastBadEdge = True
                continue

            if("source" in elem.attrib ) and ("target" in elem.attrib):
                edgeListToFill.append(Edge(
                    elem.attrib["source"],
                    elem.attrib["target"],
                    elem.attrib["id"]
                ))
               
                
    
    
            if not bool(edgeDictToFill.get(elem.attrib["source"])):
                edgeDictToFill[elem.attrib["source"]] = []
                edgeDictToFill[elem.attrib["source"]].append(
                    Edge(
                    elem.attrib["source"],
                    elem.attrib["target"],
                    elem.attrib["id"]
                ))
                continue
            
            edgeDictToFill[elem.attrib["source"]].append(
                Edge(
                elem.attrib["source"],
                elem.attrib["target"],
                elem.attrib["id"]
            ))
            continue




        if "vertex" in elem.attrib:

            allowedShape = True
            for s in notAllowedShapesList:
                if s in elem.attrib["style"]:
                    testResultList.append("ERROR\n\t"+str(s)+" vertex shape is not allowed, skipping this vertex in checkups")
                    foundAtLeastBadOneVertex = True
                    continue





            if "ellipse" in elem.attrib["style"]:

                if "value" in elem.attrib and not elem.attrib["id"] == "":
                    if( bool(re.search("\s?[1-9][0-9]?\s?",elem.attrib["value"]))):
                        vertexListToFill.append(
                        Vertex(elem.attrib["id"],
                        elem.attrib["value"].replace("<br>","\n"),
                        endingProductionType,
                        parseColor(elem.attrib["style"]),
                        0,
                        0
                    )) 
                else:
                    testResultList.append('ERROR\n\t'+'check id: '+ str( elem.attrib["id"])+'\n\tUnexpected value in ending production (not a mission number)')



                vertexListToFill.append(
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
                    mainStoryPropsToFill.x = float(geometry.attrib['x'])
                    mainStoryPropsToFill.y = float(geometry.attrib['y'])
                    mainStoryPropsToFill.width = float(geometry.attrib['width'])
                    mainStoryPropsToFill.height = float(geometry.attrib['height'])
                    mainStoryPropsToFill.endX = float(mainStoryPropsToFill.x + mainStoryPropsToFill.width )
                    mainStoryPropsToFill.endY = float(mainStoryPropsToFill.y + mainStoryPropsToFill.height)
                continue



            hasX = False
            hasY= False


            parser.feed(elem.attrib["value"].replace("<br>","\n"))
            for geometry in elem.iter('mxGeometry'):

                if 'x' in geometry.attrib:
                    xPos = geometry.attrib['x']
                    hasX = True
                if 'y' in geometry.attrib:
                    yPos = geometry.attrib['y']
                    hasY = True

            if not (hasX and hasY):
                hasX=False
                hasY=False
                foundAtLeastBadOneVertex = True
                testResultList.append('ERROR\n\t'+str(elem.attrib["value"]) + '\n\tis not proper vertex, has no x or y position, skipping this vertex in later checkups')
                continue

            # print(elem.attrib)

            vertexListToFill.append(
                Vertex(elem.attrib["id"],
                reduce(lambda a,b: a+b,parser.return_data()),
                "type",
                parseColor(elem.attrib["style"]),
                float(xPos),
                float(yPos)
                )
            )

            continue

def checkVertexAlignmentInMainStory(vertexList:List[Vertex],mainStoryProps:MainStoryProps,testResultList):
    # fix this method
    mainStoryFirstXValue = []
    for x in vertexList:
        if ( x.x > mainStoryProps.x) and ( x.y > mainStoryProps.y) and ( x.x < mainStoryProps.endX) and (x.y < mainStoryProps.endY):
            if len(mainStoryFirstXValue) >0:
                if x.x != mainStoryFirstXValue[0]:
                    testResultList.append("WARNING\n\t" + str(x.content) +"\n\tCheck if vertexes are alliged in main story")



def checkProductionTypesByRegex(vertexList:List[Vertex],testResultList:List):
    missionProductionType= "mission"
    genericProductionType = "generic"
    detailedProductionType = "detailed"
    endingProductionType = "ending"
    missionProductionRegex = "^\(\s?(\w\s*)+[?|!]?\s?,\s?Q[0-9]+\s?(\)\s?)$"
    detailedProductionRegex = "s?([A-z-’`',]+\s)+\s?/\s?([A-ząćĆęłŁńóÓśŚżŻźŹ\-’`',]+\s?)+"

    for x in vertexList:
        

        if(mayBeGeneric(x.content)):
            x.prodType = genericProductionType
            continue
    
        if(bool(re.search(missionProductionRegex,x.content))):
            x.prodType = missionProductionType
            continue
    
        if(bool(re.match(detailedProductionRegex,x.content)) and "(" not in x.content and ";" not in x.content):

            x.prodType = detailedProductionType
            continue
   
        if( x.prodType != endingProductionType and "!" in x.content):
            testResultList.append("ERROR\n\t"+str(x.content)+"\n\tProduction name does not seem to fit any proper format of production, check '!'")

        elif( x.prodType != endingProductionType):
            testResultList.append("ERROR\n\t"+str(x.content)+"\n\tProduction name does not seem to fit any proper format of production")


def copyVertexListToDict(vertexList:List[Vertex],vertexDict):
    
    for v in vertexList:
        vertexDict[v.id] = v

def checkVertexListColors(vertexList, testResultList,allowedColorDictionary):

    
    missionProductionType= "mission"
    detailedProductionType = "detailed"
    endingProductionType = "ending"
    genericProductionType = "generic"

    vertexTypesList = [missionProductionType,detailedProductionType,endingProductionType,genericProductionType]
    
    for x in vertexList:
        if x.prodType == "type":
            testResultList.append("WARNING\n\t"+ x.content + "\n\tSkipped color check as production type was not recognized")
        elif not isVertexColorCorrect(x,vertexTypesList,allowedColorDictionary) and (x.color.lower() in allowedColorDictionary[genericProductionType] ):
            testResultList.append("WARNING\n\t" +x.content+"\n\tfound color in production: " + x.color+", make sure its generic production(generic colors are none or #ffffff). If it is, ignore warning")

        elif not isVertexColorCorrect(x,vertexTypesList,allowedColorDictionary):
            testResultList.append("ERROR\n\t" +x.content+"\n\tcolor " + x.color+" in production of type "+x.prodType +" is not on allowed list: " + str(allowedColorDictionary[x.prodType]))


def checkIfGenericVertexesAreAllowed(vertexList, allowedGenericProductionList, charactersList, itemsList, locationsList, testResultList):
    genericProductionType = "generic"

    for x in vertexList:
        if(x.prodType == genericProductionType):
            isGenericProductionAllowed(x.content,allowedGenericProductionList,charactersList, itemsList, locationsList, testResultList)


def checkOutgoingEdgesCorrectness(vertexDict,edgeDict,testResultList):
    endingProductionType = "ending"
    for v in vertexDict.values():

        if not bool(edgeDict.get(v.id)):
            if v.prodType != endingProductionType:
                testResultList.append("ERROR\n\t"+str(v.content)+"\n\tNo outgoing edges from non-ending vertex")

        if bool(edgeDict.get(v.id)) and v.prodType == endingProductionType:
            testResultList.append("ERROR\n\t"+"ending id"+str(v.id)+"\n\tending should not have outgoing edges")

def startingChecks(vertexList, vertexDict,edgeList, edgeDict,testResultList):
    suspectedStartingVertex = [] 

    suspectedStartingVertex = list(edgeDict.keys())

    # checking vertex with no incoming edge
    for edgeList in edgeDict.values():

        for edge in edgeList:
        
            for suspect in suspectedStartingVertex:
                if suspect == edge.target:
                    suspectedStartingVertex.remove(suspect)




    # second part, ones with incoming vertexes
    for v in vertexList:
        isStarting = False
        for e in edgeList:
            if e.target == v.id:
                if vertexDict[e.target].y < v.y:
                    isStarting = True
                else:
                    isStarting = False 
                    break # breaking loop as one incoming edge is higher

    
        if isStarting:
            suspectedStartingVertex.append(suspectedStartingVertex)

    # end of starting finding validation


    if (len(suspectedStartingVertex )== 0 ):
        testResultList.append("ERROR\n\t","Could not find staring point, make sure that it is higher than any vertex pointing to it or has no incoming edges")


    if(len(suspectedStartingVertex) > 1):
        testResultList.append("WARNING\n\t"+"more than one vertex is a starting point (no incoming edges or its higher than all incoming edges), please check if there should be more than one starting points")


def getNeighboursIds(vertexId, edgeDict):

    neigboursList = edgeDict.get(vertexId)
    neigboursIdList = []

    if bool(neigboursList):
        for e in neigboursList:
            neigboursIdList.append(e.target)
    else:
        neigboursIdList = []

    return neigboursIdList

# foundEnding = [False] # to keep reference
def dfsToEnding(vertexDict, edgeDict, visitedIdList, foundEnding, currentVertexId):
    endingProductionType = "ending"

    
    visitedIdList.append(currentVertexId) 

    neighboursIds = getNeighboursIds(currentVertexId,edgeDict)


    if( vertexDict.get(currentVertexId).prodType == endingProductionType):
        foundEnding[0] = True

    if foundEnding[0]:
        return True # found an ending from vertex

    for vId in neighboursIds:
        if foundEnding[0]:
            return True 

        if vId not in visitedIdList:
            return dfsToEnding(vertexDict,edgeDict,visitedIdList,foundEnding,vId)

    if foundEnding[0]:
        return True # found an ending from vertex


    return False

def checkIfAnyEndingFoundFromEveryVertex(vertexList,vertexDict,edgeDict, testResultList, foundAtLeastOneBadVertex):
    endingProductionType = "ending"

    foundEnding = [False] # to keep reference
    visitedList = []
    foundEnding = [False]
    if not foundAtLeastOneBadVertex:

        for v in vertexList:
            visitedList = []
            foundEnding = [False]

            if v.prodType != endingProductionType:
                foundEnding = [False]
                if not dfsToEnding(vertexDict,edgeDict,visitedList,foundEnding,v.id):
                    testResultList.append(
                    "ERROR\n\t"+
                    v.content +
                    '\n\tCould not reach any ending from vertex, check connections' 
                )
    else:
        testResultList.append(
                    "WARNING\n\t"+
                    'Skipped ending search from each vertex' 
                )