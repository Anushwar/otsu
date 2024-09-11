import math
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image


def calculate_histogram(image):
    row, col = image.shape
    histogram = np.zeros(256)
    for i in range(0, row):
        for j in range(0, col):
            histogram[image[i, j]] += 1
    x = np.arange(0, 256)
    plt.bar(x, histogram, color="b", width=5, align="center", alpha=0.25)
    plt.show()
    return histogram


def regenerate_image(image, threshold):
    row, col = image.shape
    result = np.zeros((row, col))
    for i in range(0, row):
        for j in range(0, col):
            if image[i, j] >= threshold:
                result[i, j] = 255
            else:
                result[i, j] = 0
    return result


def count_pixels(histogram):
    count = 0
    for i in range(0, len(histogram)):
        if histogram[i] > 0:
            count += histogram[i]
    return count


def calculate_weight(start, end, histogram):
    weight = 0
    for i in range(start, end):
        weight += histogram[i]
    return weight


def calculate_mean(start, end, histogram):
    mean = 0
    weight = calculate_weight(start, end, histogram)
    for i in range(start, end):
        mean += histogram[i] * i
    return mean / float(weight)


def calculate_variance(start, end, histogram):
    variance = 0
    mean = calculate_mean(start, end, histogram)
    weight = calculate_weight(start, end, histogram)
    for i in range(start, end):
        variance += ((i - mean) ** 2) * histogram[i]
    variance /= weight
    return variance


def calculate_threshold(histogram):
    count = count_pixels(histogram)
    threshold_values = {}
    for i in range(1, len(histogram)):
        vb = calculate_variance(0, i, histogram)
        wb = calculate_weight(0, i, histogram) / float(count)
        mb = calculate_mean(0, i, histogram)

        vf = calculate_variance(i, len(histogram), histogram)
        wf = calculate_weight(i, len(histogram), histogram) / float(count)
        mf = calculate_mean(i, len(histogram), histogram)

        V2w = wb * (vb) + wf * (vf)
        V2b = wb * wf * (mb - mf) ** 2

        fw = open("trace.txt", "a")
        fw.write("T=" + str(i) + "\n")

        fw.write("Wb=" + str(wb) + "\n")
        fw.write("Mb=" + str(mb) + "\n")
        fw.write("Vb=" + str(vb) + "\n")

        fw.write("Wf=" + str(wf) + "\n")
        fw.write("Mf=" + str(mf) + "\n")
        fw.write("Vf=" + str(vf) + "\n")

        fw.write("within class variance=" + str(V2w) + "\n")
        fw.write("between class variance=" + str(V2b) + "\n")
        fw.write("\n")

        if not math.isnan(V2w):
            threshold_values[i] = V2w

    return threshold_values


def get_optimal_threshold(threshold_values):
    min_V2w = min(threshold_values.values())
    optimal_threshold = [k for k, v in threshold_values.items() if v == min_V2w]
    print("optimal threshold", optimal_threshold[0])
    return optimal_threshold[0]


image = Image.open("data/img.jpg").convert("L")
image_array = np.asarray(image)

histogram = calculate_histogram(image_array)
threshold_values = calculate_threshold(histogram)
optimal_threshold = get_optimal_threshold(threshold_values)

result = regenerate_image(image_array, optimal_threshold)
plt.imshow(result)
plt.savefig("data/otsu.jpg")
