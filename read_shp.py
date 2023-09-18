import os
import matplotlib.pyplot as plt
import geopandas
import webbrowser
# from geodatasets import get_path

def main():
    # get shapefile path
    shp_path = input("Enter path to shapefile: ")

    while (not os.path.isdir(shp_path)):
        print("No such path exists")
        shp_path = input("Enter path to shapefile: ")

    # read in shapefile
    shp_gdf = geopandas.read_file(shp_path)
    shp_gdf["area"] = shp_gdf.area

    # plot map
    shp_gdf.plot("area", legend=True)         # plain background
    plt.show()

    # plot web map
    webmap = shp_gdf.explore("area", legend=True)        # interactive map
    filename = input("Enter filename: ")
    webmap_file = os.getcwd() + r"\{filename}.html".format(filename=filename)
    webmap.save(webmap_file)
    webbrowser.open(webmap_file)

    print("Map Plotted!")

if __name__ == "__main__":
    main()