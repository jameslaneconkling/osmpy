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

    
    bbox = "BOX(? ?,? ?)",(minx,miny,maxx,maxy)

    return bbox

    

def featureCount(conn, table, geom, bbox):
    c = conn.cursor()
    c.execute("SELECT SUM(st_npoints(st_intersection(?, ST_GeomFromText(?))) FROM ? WHERE ST_Intersects(?, ST_GeomFromText(?))", (geom, bbox,table)
    row = c.fetchone()
    count = row[1]
    return count


def splitBbox(bbox):

    minx = bbox[4:-1].split(',')[0].split(' ')[0]
    miny = bbox[4:-1].split(',')[0].split(' ')[1]
    maxx = bbox[4:-1].split(',')[1].split(' ')[0]
    maxy = bbox[4:-1].split(',')[1].split(' ')[1]

    midx = minx + (maxx-minx)/2
    midy = miny + (maxy-miny)/2

    bbox1 = "BOX(? ?,? ?)", (minx,midy,midx,maxy)
    bbox2 = "BOX(? ?,? ?)", (midx,midy,maxx,maxy)
    bbox3 = "BOX(? ?,? ?)", (minx,miny,midx,midy)
    bbox4 = "BOX(? ?,? ?)", (midx,miny,maxx,midy)

    bbox = [bbox1,bbox2,bbox3,bbox4]

    return bbox
              

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
    fCount = featureCount(conn,table, geom, cell[1])

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


conn.close()






