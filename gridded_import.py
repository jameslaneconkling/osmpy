### asdf

import psycopg2



def makeSquare(conn, table, geom):

    c = conn.cursor()
    c.execute("SELECT ST_Extend(?) FROM ?", (geom, table)) 
    row = c.fetchone()

    bbox = row[1]

    #PostGIS spits out something like this
    #"BOX(968651.781199999 -434363.015500002,1667026.9567 257522.6459)"

    minx = bbox[4:-1].split(',')[0].split(' ')[0]
    miny = bbox[4:-1].split(',')[0].split(' ')[1]
    maxx = bbox[4:-1].split(',')[1].split(' ')[0]
    maxy = bbox[4:-1].split(',')[1].split(' ')[1]

    width = maxx-minx
    height = maxy-miny

    dx = 0
    dy = 0

    #fat
    if width > height:
        dy = (width - height)/2
    
    #tall
    elif width < height:
        dx = (height - width)/2
    #square
    else:
        pass

    minx = minx - dx
    miny = miny - dy
    maxx = minx + dx
    maxy = maxy + dy

    
    bbox = [minx,miny,maxx,maxy]

    return bbox

    

def featureCount():
    pass

def splitBbox():
    pass

def addToDB():
    pass

#connetion to PostgreSQL
conn = psycopg2.connect(database="testdb", user="postgres", password="pass123", host="127.0.0.1", port="5432")
#Road table
table = 'roads'
#Geometry column of road table
geom = 'geom'

bbox = makeSquare(conn, table, geom)

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
