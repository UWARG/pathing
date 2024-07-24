import numpy as np
import math


#inflate_polygon: Given a list of LLA coordinates representing vertices for a polygon geometry,
#offset the vertices such that the perpendicular distance between the original and offset edges is 
#always equal to the scale factor.

#Parameters: 
#vertices: a numpy array of LLA coordinates representing the vertices. Each vertex in the list forms an edge with the next.
#The last vertex in the list forms an edge with the first. 
#scale_factor: How far (in meters) to offset the vertices by (postitive for inflation, negative for deflation).

def inflate_polygon(vertices: np.ndarray, scale_factor: int) -> np.ndarray:

    #Ensure that the input vertices contains all three feilds for LLA:
    assert vertices.shape[1] == 3, f"Expected 3 fields (latidue, longitude, altitude). Got" + str(vertices.shape[1]) + "columns."

    #Referance radius for altitude (Radius of earth = 6371 km):
    R_ref = 6371 * (10**3)

    #Convert LLA coordinates from degrees to radians:
    for i in range(len(vertices)):
        (lat, lon, alt) = vertices[i]
        (lat_deg, lon_deg) = math.radians(lat), math.radians(lon)
        vertices[i] = (lat_deg, lon_deg, alt)

    #Convert to LLA to cartesian:
    for i in range(len(vertices)):
        (lat, lon, alt) = vertices[i]

        x = (R_ref + alt) * math.cos(lat) * math.cos(lon)
        y = (R_ref + alt) * math.cos(lat) * math.sin(lon)
        z = (R_ref + alt) * math.sin(lat)
        vertices[i] = (x, y, z)

    #Generate a list of edges joining the vertices:
    edges = np.zeros((len(vertices), 3))
    for i in range(len(edges) - 1):
        (x1, y1, z1) = vertices[i]
        (x2, y2, z2) = vertices[i + 1]
        (dx, dy, dz) = (x2 - x1, y2 - y1, z2 - z1)
        edges[i] = (dx, dy, dz)

    #Generate the last edge (connecting last vertex in list to the first).
    (x1, y1, z1) = vertices[len(vertices) - 1]
    (x2, y2, z2) = vertices[0]
    (dx, dy, dz) = (x2 - x1, y2 - y1, z2 - z1)
    edges[len(edges) - 1] = (dx, dy, dz)

    #Calculate the direction vector of the angle bisectors:
    bisectors = np.zeros((len(edges), 3))
    for i in range(len(bisectors) - 1):
        edge1 = np.array(edges[i])
        edge2 = np.array(edges[i + 1])
        edge1 = edge1 / np.linalg.norm(edge1)
        edge2 = edge2 / np.linalg.norm(edge2)
        bisector = edge1 + edge2
        bisector /=  np.linalg.norm(bisector)

        #Calculate the required norm of the bisector vector given the scaling factor
        l = scale_factor / math.sqrt((1 + np.dot(edge1, edge2))/2)
        bisector *= l
        bisectors[i] = bisector
        
    #Calculate final bisector (final edge with first)
    edge1 = np.array(edges[len(edges) - 1])
    edge2 = np.array(edges[0])
    edge1 = edge1 / np.linalg.norm(edge1)
    edge2 = edge2 / np.linalg.norm(edge2)
    bisector = edge1 + edge2
    bisector /=  np.linalg.norm(bisector) 

    #Calculate the required norm of the bisector vector given the scaling factor
    l = scale_factor / math.sqrt((1 + np.dot(edge1, edge2))/2)
    bisector *= l
    bisectors[len(bisectors) - 1] = bisector 

    #Offset the vertices by the bisector vectors
    offset_verts = np.zeros((len(edges), 3))
    for i in range(len(offset_verts)):
        (x1, y1, z1) = vertices[i]
        (x2, y2, z2) = bisectors[i]
        offset_verts[i] = (x1 - x2, y1 - y2, z1 - z2)

    #Convert cartesian to LLA
    for i in range(len(offset_verts)):
        (x, y, z) = offset_verts[i]
        lon = math.atan2(y, x)
        lat = math.atan2(z, x)
        alt = math.sqrt(x**2 + y**2 + z**2) - R_ref

        #Convert lat and long from radians to degrees
        lon = math.degrees(lon)
        lat = math.degrees(lat)

        offset_verts[i] = lat, lon, alt


    #Return the offset vertices
    return offset_verts

triangle = np.array([[48.8567,  2.3508,  0], [61.4140105652, 23.7281341313, 0], [51.760597, -1.261247, 0]])
print(inflate_polygon(triangle, 10))

