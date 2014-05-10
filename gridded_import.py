### asdf

def makeSquare():
    ST_Extend(features)

def featureCount():
    pass

def splitBbox():
    pass

def addToDB():
    pass

bbox = makeSquare(features)

gridCells = [['1', bbox]]

while len(gridCells):
    cell = gridCells[0]
    fCount = featureCount(cell[1])

    if fCount > threshold:
        bbox1, bbox2, bbox3, bbox4 = splitBbox(bbox)

        parentId = gridCells.pop(0)
        gridCells= [[parentId + '.1',bbox1],
                    [parentId + '.2', bbox2],
                    [parentId + '.3', bbox3],
                    [parentId + '.4', bbox4]
                    ] + gridCells

    else:
        addToDB(cell[0], cell[1], fCount)
        gridCells.pop(0)













def splitCell (features, cellId='1', threshold):
    newId = 1
    cellcount = sum(ST_NPoints(features))

    bbox = getBbox(features)

    if (cellcount > threshold):
        for i in range(1,5):
            bbox /= 4
            newCellId = cellId + '.' + i
            splitCell(result, cellId = newCellId, threshold = threshold)
    else:
        # insert into table: select *, bboxId FROM feature

        newId += 1






while cellCount > threshold:


dx = ['1','2','3','4']

first = dx.pop(0)

dx = [first + '.1', first + '.2', first + '.3', first + '.4'] + dx
