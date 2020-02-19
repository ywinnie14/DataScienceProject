#Function to read data from file and save data to a dataset (python list)
def read_data_file(filename):
    dataset = [] #dataset is a python list
    f = None
    try:
        f = open(filename, 'r')
        while True:
            line = f.readline()
            if len(line) == 0:
                break
            line = line.replace('\n', '') #remove end of line \n character
            xystring = line.split(' ') #x y coordinates in string format
            #convert x & y strings to x & y numbers and
            #add them as an array [x, y] to dataset

            dataset.append([float(xystring[0]), float(xystring[1])])
    except Exception as ex:
        print(ex.args)
    finally:
        if f:
            f.close()
    return dataset
#end of function


def scale_data_to_canvas_size(dataset, width=700, height=700):
    #dataset is a list of samples as [[x1, y1], [x2, y2],. . , [xn, yn]]
    margin = 100
    width = width - 100
    height = height - 100
    scaled_data = []
    maxW = -1000000.0
    minW = 1000000.0
    maxH = -1000000.0
    minH = 1000000.0
    for sample in dataset: #sample: [x, y], dataset: [[x1, y1], . . , [xn, yn]]
        if maxW < sample[0]:
            maxW = sample[0]
        if minW > sample[0]:
            minW = sample[0]
        if maxH < sample[1]:
            maxH = sample[1]
        if minH > sample[1]:
            minH = sample[1]
    for sample in dataset:
        x = int (width * (sample[0] - minW) / (maxW - minW)) + margin / 2
        y = int(height * (sample[1] - minH) / (maxH - minH)) + margin / 2
        scaled_data.append([x, y])
    return scaled_data
# end of function


#Function that calculates distance between 2 points [x1,y1] and [x2,y2]
def calculate_distance(point1, point2):
    x = point1[0] - point2[0]
    y = point1[1] - point2[1]
    distance = (x*x + y*y) ** 0.5 #power ** 0.5 is equivalent to square root
    return distance


#Function to find shortest distance from all distances
#between a reference point to all points in point_list
def find_shortest_distance(ref_point, point_list):
    min_dist = 1000000.0
    min_index = -1
    index = 0
    for point in point_list:
        dist = calculate_distance(ref_point, point)
        if min_dist > dist:
            min_dist = dist
            min_index = index
        index += 1
    return [min_index, min_dist]
#end of function


def calculate_memberships(cluster_centre_list, data_list):
    data_len = len(data_list)
    cc_len = len(cluster_centre_list)
    memberships = []
    for xt_index in range(data_len):
        t_memberships = []
        for i in range(cc_len):
            t_memberships.append(0)
        memberships.append(t_memberships)
    for data_point in data_list:
        xt_index = data_list.index(data_point)
        [ncc_index, shortest_dist] = find_shortest_distance(data_point, cluster_centre_list)
        memberships[xt_index][ncc_index] = 1
    return memberships
#end of program


#Function to scale data samples and cluster centres to fit canvas size
def scale_all_data_to_canvas_size(dataset, clusterset, width=700, height=700):
    margin = 100
    width = width - 100
    height = height - 100
    scaled_data = []
    scaled_clusters = []
    maxW = -1000000.0
    minW = 1000000.0
    maxH = -1000000.0
    minH = 1000000.0
    for sample in dataset:
        if maxW < sample[0]:
            maxW = sample[0]
        if minW > sample[0]:
            minW = sample[0]
        if maxH < sample[1]:
            maxH = sample[1]
        if minH > sample[1]:
            minH = sample[1]
    for sample in dataset:
        x = int (width * (sample[0] - minW) / (maxW - minW)) + margin / 2
        y = int(height * (sample[1] - minH) / (maxH - minH)) + margin / 2
        scaled_data.append([x, y])
    for sample in clusterset:
        x = int (width * (sample[0] - minW) / (maxW - minW)) + margin / 2
        y = int(height * (sample[1] - minH) / (maxH - minH)) + margin / 2
        scaled_clusters.append([x, y])
    return [scaled_data, scaled_clusters]
# end of function


def calculate_sum_2(memberships, distances):
    sum2=0
    for n in range(len(memberships)):
        for q in range(len(memberships[n])):
            sum2 += memberships[n][q] * distances[n][q]* distances[n][q]
    return sum2


def recalcCluster(memberships, data_list, clusterNum):
    i = 0
    newCluster = []
    while i < clusterNum:
        cSumX = 0
        cSumY = 0
        clusterCount = 0
        for p in range(len(memberships)):
            P1 = data_list[p]
            P2 = memberships[p]
            if P2[i] == 1:
                cSumX += P1[0]
                cSumY += P1[1]
                clusterCount += 1
        newCluster.append([cSumX / (clusterCount+0.001), cSumY / (clusterCount+0.001)])
        i += 1
    return newCluster


def find_cluster_centre(centre_list, clusterNum):
    cluster_centre_list = []
    i = 0
    while i < clusterNum:
        cluster_centre_list.append(centre_list[i])
        i+=1
    return cluster_centre_list


def calculate_error(newMembership, newCluster, data_list, clusterNum):
    # clusterNum = 2
    i = 0
    error = 0
    while i < clusterNum:
        clusterError = 0
        for p in range(len(newMembership)):
            temp = newMembership[p]
            if temp[i] == 1:
                P1 = data_list[p]
                P2 = newCluster[i]
                calculate_distance(P1, P2)
                clusterError = clusterError + calculate_distance(P1, P2)**2
            p+=1
        i+=1
    error = error + clusterError
    return error
