import io_data_module as iodata
import tkinter

clusteringType = input("Enter a cluster type (K-Mean --> type k // Fuzzy-C-Mean --> type c): ")

if clusteringType == 'k' or clusteringType == 'K':

    clusterNum = int(input("Enter the number of clusters (between 1 to 8): "))
    input_data_list = int(input("Enter a data file (ellipse1 --> type 1 // ellipse2 --> type 2): "))
    if input_data_list== 1:
        data_list = iodata.read_data_file('ellipse1.txt')
    else:
        data_list = iodata.read_data_file('ellipse2.txt')


    centre_list = [[3,4], [2,2], [3,2], [3,6], [2,4], [4,3], [3,3], [2,3]]
    cluster_centre_list = iodata.find_cluster_centre(centre_list, clusterNum)
    print(cluster_centre_list)


    littleError = 0.1
    error= 10000000
    x = True
    while x == True:
        memberships = iodata.calculate_memberships(cluster_centre_list, data_list)
        newError = iodata.calculate_error(memberships, cluster_centre_list, data_list, clusterNum)
        cluster_centre_list = iodata.recalcCluster(memberships, data_list, clusterNum)
        if abs(newError-error) > littleError:
            error = newError
        else:
            x = False
        print(error)


    top = tkinter.Tk()
    C = tkinter.Canvas(top, bg="white", height=700, width=700)


    #Display data
    [scaled_data_list, scaled_cluster_centre_list] = iodata.scale_all_data_to_canvas_size(data_list, cluster_centre_list)
    for x, y in scaled_data_list:
        C.create_oval(x-3, y-3, x+3, y+3, outline = "grey", fill="grey")


    #Display line between data point and cluster point
    data_len = len(data_list)
    cc_len = len(cluster_centre_list)

    for t in range(data_len):
        for i in range(cc_len):
            if memberships[t][i] == 1:
                x1 = scaled_data_list[t][0]
                y1 = scaled_data_list[t][1]
                x2 = scaled_cluster_centre_list[i][0]
                y2 = scaled_cluster_centre_list[i][1]
                C.create_line(x1, y1, x2, y2, fill='teal')

    #Display cluster centre
    for x, y in scaled_cluster_centre_list:
        C.create_oval(x-3, y-3, x+3, y+3, outline = "red", fill="red")

    C.pack()
    top.mainloop()
else:
    exit(0)