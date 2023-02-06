from validator_lib import *


missionProductionType= "mission"
genericProductionType = "generic"
detailedProductionType = "detailed"
endingProductionType = "ending"
allowedColorDictionary = defaultdict()
allowedColorDictionary[missionProductionType] ="#e1d5e7"
allowedColorDictionary[genericProductionType] = {"#ffffff","none"}
allowedColorDictionary[detailedProductionType] ="#d5e8d4"
allowedColorDictionary[endingProductionType] = {"#fff2cc","#000000","#ffffff","#e1d5e7","none","none;"}


vertexList =[]
vertexDict = defaultdict()
edgeList =[]
edgeDict = defaultdict()
testResultList =[]
notAllowedShapesList =["rhombus", "process","parallelogram", "hexagon","cloud"]
allowedGenericProductionList = loadFromJson("./produkcje_generyczne.json")
allowedCharactersList= loadFromJson("./allowedCharacters.json")
allowedItemsList = loadFromJson("./allowedItems.json")
allowedLocationsList= loadFromJson("./allowedLocations.json")

mainStoryProps = MainStoryProps(0,0,0,0,0,0)

if len(sys.argv) == 1:
    print("please pass name of xml file to verify in cli argument, ex:\n\t",
        "python3 validator_new.py example.drawio.xml"
    )
    exit(-1)
pathToXml = "./" + sys.argv[1]

readEdgesAndVertexFromXml(pathToXml,vertexList,edgeList,edgeDict, mainStoryProps,testResultList,notAllowedShapesList)

copyVertexListToDict(vertexList,vertexDict)

checkVertexAlignmentInMainStory(vertexList,mainStoryProps,testResultList)

checkProductionTypesByRegex(vertexList,testResultList)

checkVertexListColors(vertexList,testResultList,allowedColorDictionary)

checkIfGenericVertexesAreAllowed(vertexList,allowedGenericProductionList,allowedCharactersList,allowedItemsList,allowedLocationsList,testResultList)

checkOutgoingEdgesCorrectness(vertexDict,edgeDict,testResultList)

startingChecks(vertexList,vertexDict,edgeList,edgeDict,testResultList)

checkIfAnyEndingFoundFromEveryVertex(vertexList,vertexDict,edgeDict,testResultList,False)


print("RESULTS\n\n")


for t in testResultList:
    print(t,"\n")

