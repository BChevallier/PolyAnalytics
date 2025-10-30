import math

color2identifier = {
    (204, 0, 0):     'Tr1',
    (0, 0, 255):     'Tr2',
    (53, 37, 20):    'Tr3',
    (255, 255, 0):   'Tr4',
    (0, 255, 0):     'Tr5',
    (153, 102, 0):   'Tr6',
    (171, 59, 214):  'Tr7',
    (255, 255, 255): 'Tr8',
    (255, 153, 0):   'Tr9',
    (54, 226, 170):  'Tr10',
    (39, 92, 74):    'Tr11',
    (125, 35, 28):   'Tr12',
    (243, 131, 129): 'Tr13',
    (255, 0, 153):   'Tr14',
    (182, 161, 133): 'Tr15',
    (194, 253, 0):   'Tr16',
    (103, 140, 48):  'Tr13',#Skin of aquarion.
}


def color_distance_rgb(rgb1, rgb2):
    r1, g1, b1,= rgb1[:3]
    r2, g2, b2 = rgb2[:3]
    distance = math.sqrt((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2)
    max_distance = math.sqrt(255**2 + 255**2 + 255**2)  # ~441.67
    normalized_distance = distance / max_distance
    #print(f"normalized distance is: {normalized_distance}")
    return normalized_distance  # 0 means identical, 1 means maximally different

def colors_are_similar(rgb1, rgb2):
    r1, g1, b1 = rgb1[:3]
    r2, g2, b2 = rgb2[:3]
    if color_distance_rgb(rgb1,rgb2)<0.2:
        return True
    else:
        return False


def identify_tribe(color):
    min_distance = float('inf')
    closest_tribe = None
    for known_color, tribe in color2identifier.items():
        dist = color_distance_rgb(color, known_color)
        if dist < min_distance:
            min_distance = dist
            closest_tribe = tribe

    if colors_are_similar(color, list(color2identifier.keys())[list(color2identifier.values()).index(closest_tribe)]):
        return closest_tribe
    else:
        return None


# returns True if color is more green than blue and has a lot of green
def check_if_complete(color):
    return True if color[1]>color[2] and color[1]>100 else False



if __name__ == "__main__":
    #print(identify_tribe((0,0,220)))
    print(color_distance_rgb((0,0,0),(0,0,0)))