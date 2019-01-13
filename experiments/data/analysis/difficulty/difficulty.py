import numpy as np
from scipy import stats
from sklearn import svm
from sklearn.preprocessing import normalize
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, cohen_kappa_score
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.ensemble import ExtraTreesClassifier
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from mlxtend.plotting import plot_decision_regions
import seaborn as sns
sns.set(style='ticks')

norm = True
# norm = False

age = [1,4,1,0,2,4,3,0,3,1,1,1]

types = ['goal_amazon', 'fuzzy_amazon', 'exploring_amazon', 'goal_medium', 'fuzzy_medium', 'exploring_medium', 'goal_dribbble', 'fuzzy_dribbble', 'exploring_dribbble']
markers = ['^', 'o', '*', 'x', '+', 'D', '1', 'H', 's']
task_color = np.array([
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'steelblue', '#82a67d'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'steelblue', '#82a67d'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'steelblue', '#82a67d'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'steelblue', '#82a67d'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'steelblue', '#82a67d'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'steelblue', '#82a67d'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'steelblue', '#82a67d'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'steelblue', '#82a67d'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'steelblue', '#82a67d'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'steelblue', '#82a67d'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'steelblue', '#82a67d'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'steelblue', '#82a67d'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'steelblue', '#82a67d'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'steelblue', '#82a67d'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'steelblue', '#82a67d'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'steelblue', '#82a67d'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'steelblue', '#82a67d'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'steelblue', '#82a67d'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'steelblue', '#82a67d'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'steelblue', '#82a67d'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'steelblue', '#82a67d'],
])
task_type = np.array([
    ['goal_amazon', 'fuzzy_amazon', 'exploring_amazon', 'goal_medium', 'fuzzy_medium', 'exploring_medium', 'goal_dribbble', 'fuzzy_dribbble', 'exploring_dribbble'],
    ['goal_amazon', 'fuzzy_amazon', 'exploring_amazon', 'goal_medium', 'fuzzy_medium', 'exploring_medium', 'goal_dribbble', 'fuzzy_dribbble', 'exploring_dribbble'],
    ['goal_amazon', 'fuzzy_amazon', 'exploring_amazon', 'goal_medium', 'fuzzy_medium', 'exploring_medium', 'goal_dribbble', 'fuzzy_dribbble', 'exploring_dribbble'],
    ['goal_amazon', 'fuzzy_amazon', 'exploring_amazon', 'goal_medium', 'fuzzy_medium', 'exploring_medium', 'goal_dribbble', 'fuzzy_dribbble', 'exploring_dribbble'],
    ['goal_amazon', 'fuzzy_amazon', 'exploring_amazon', 'goal_medium', 'fuzzy_medium', 'exploring_medium', 'goal_dribbble', 'fuzzy_dribbble', 'exploring_dribbble'],
    ['goal_amazon', 'fuzzy_amazon', 'exploring_amazon', 'goal_medium', 'fuzzy_medium', 'exploring_medium', 'goal_dribbble', 'fuzzy_dribbble', 'exploring_dribbble'],
    ['goal_amazon', 'fuzzy_amazon', 'exploring_amazon', 'goal_medium', 'fuzzy_medium', 'exploring_medium', 'goal_dribbble', 'fuzzy_dribbble', 'exploring_dribbble'],
    ['goal_amazon', 'fuzzy_amazon', 'exploring_amazon', 'goal_medium', 'fuzzy_medium', 'exploring_medium', 'goal_dribbble', 'fuzzy_dribbble', 'exploring_dribbble'],
    ['goal_amazon', 'fuzzy_amazon', 'exploring_amazon', 'goal_medium', 'fuzzy_medium', 'exploring_medium', 'goal_dribbble', 'fuzzy_dribbble', 'exploring_dribbble'],
    ['goal_amazon', 'fuzzy_amazon', 'exploring_amazon', 'goal_medium', 'fuzzy_medium', 'exploring_medium', 'goal_dribbble', 'fuzzy_dribbble', 'exploring_dribbble'],
    ['goal_amazon', 'fuzzy_amazon', 'exploring_amazon', 'goal_medium', 'fuzzy_medium', 'exploring_medium', 'goal_dribbble', 'fuzzy_dribbble', 'exploring_dribbble'],
    ['goal_amazon', 'fuzzy_amazon', 'exploring_amazon', 'goal_medium', 'fuzzy_medium', 'exploring_medium', 'goal_dribbble', 'fuzzy_dribbble', 'exploring_dribbble'],
    ['goal_amazon', 'fuzzy_amazon', 'exploring_amazon', 'goal_medium', 'fuzzy_medium', 'exploring_medium', 'goal_dribbble', 'fuzzy_dribbble', 'exploring_dribbble'],
    ['goal_amazon', 'fuzzy_amazon', 'exploring_amazon', 'goal_medium', 'fuzzy_medium', 'exploring_medium', 'goal_dribbble', 'fuzzy_dribbble', 'exploring_dribbble'],
    ['goal_amazon', 'fuzzy_amazon', 'exploring_amazon', 'goal_medium', 'fuzzy_medium', 'exploring_medium', 'goal_dribbble', 'fuzzy_dribbble', 'exploring_dribbble'],
    ['goal_amazon', 'fuzzy_amazon', 'exploring_amazon', 'goal_medium', 'fuzzy_medium', 'exploring_medium', 'goal_dribbble', 'fuzzy_dribbble', 'exploring_dribbble'],
    ['goal_amazon', 'fuzzy_amazon', 'exploring_amazon', 'goal_medium', 'fuzzy_medium', 'exploring_medium', 'goal_dribbble', 'fuzzy_dribbble', 'exploring_dribbble'],
    ['goal_amazon', 'fuzzy_amazon', 'exploring_amazon', 'goal_medium', 'fuzzy_medium', 'exploring_medium', 'goal_dribbble', 'fuzzy_dribbble', 'exploring_dribbble'],
    ['goal_amazon', 'fuzzy_amazon', 'exploring_amazon', 'goal_medium', 'fuzzy_medium', 'exploring_medium', 'goal_dribbble', 'fuzzy_dribbble', 'exploring_dribbble'],
    ['goal_amazon', 'fuzzy_amazon', 'exploring_amazon', 'goal_medium', 'fuzzy_medium', 'exploring_medium', 'goal_dribbble', 'fuzzy_dribbble', 'exploring_dribbble'],
    ['goal_amazon', 'fuzzy_amazon', 'exploring_amazon', 'goal_medium', 'fuzzy_medium', 'exploring_medium', 'goal_dribbble', 'fuzzy_dribbble', 'exploring_dribbble'],
])
difficulty = np.array([
    [2, 1, 2, 2, 4, 1, 2, 3, 2],
    [2, 2, 1, 2, 3, 1, 1, 5, 1],
    [3, 2, 2, 2, 5, 3, 3, 1, 3],
    [3, 4, 2, 2, 5, 2, 3, 3, 2],
    [2, 1, 3, 3, 5, 3, 2, 1, 3],
    [2, 2, 1, 3, 4, 1, 1, 3, 2],
    [3, 4, 2, 3, 5, 3, 4, 3, 2],
    [1, 1, 1, 3, 5, 2, 2, 1, 1],
    [2, 3, 2, 2, 5, 2, 3, 1, 1],
    [1, 3, 2, 2, 3, 2, 2, 3, 3],
    [2, 2, 3, 1, 4, 5, 1, 2, 3],
    [3, 2, 1, 3, 4, 1, 3, 2, 2],
    [4, 1, 3, 5, 4, 2, 2, 2, 1],
    [2, 2, 2, 2, 3, 1, 2, 2, 1],
    [5, 1, 3, 2, 4, 1, 4, 2, 3],
    [1, 2, 1, 1, 3, 1, 1, 1, 1],
    [3, 1, 1, 3, 4, 3, 2, 2, 3],
    [2, 2, 1, 2, 3, 1, 3, 2, 2],
    [3, 2, 2, 2, 2, 1, 1, 1, 2],
    [1, 3, 2, 3, 5, 1, 2, 3, 2],
    [3, 3, 2, 3, 5, 4, 2, 3, 5]
])
if norm:
    # minimum = np.min(difficulty)
    # maximim = np.max(difficulty)
    # difficulty -= minimum
    # difficulty = difficulty / (maximim - minimum)
    difficulty = normalize(difficulty)

visit_length = np.array([
    # [29, 24, 57, 44, 30, 16, 21, 66, 79],
    # [29, 28, 60, 15, 41, 26, 10, 23, 20],
    # [36, 68, 30, 23, 26, 26, 24, 37, 30],
    # [19, 43, 29, 26, 12, 10, 39, 44, 29],
    # [27, 18, 53, 14, 18, 13, 32, 23, 32],
    # [28, 28, 29, 30, 19, 27, 19, 31, 28],
    # [50, 35, 92, 59, 89, 30, 21, 36, 44],
    # [18, 21, 48, 15, 31, 10,  8,  8, 46],
    # [27, 60, 27, 18, 24, 32,  9,  9, 40],
    # [15, 24, 33,  9, 23, 24, 22, 41, 22],
    # [28, 17, 47, 12, 38, 19, 20, 15, 10],
    # [42, 13, 33, 13, 30, 14, 16, 10, 30],
    # [53, 24, 37, 34, 22, 16,  6, 15, 19],
    # [30, 27, 33, 16, 28, 29, 42, 27, 48],
    # [56, 30, 36, 28, 41, 21, 22, 17, 34],
    # [21, 25, 69, 53, 36,  9, 16, 42, 18],
    # [42, 37, 41, 12, 61, 12, 10, 22, 31],
    # [18, 27, 42, 23, 11, 19, 17, 18, 16],
    # [34, 66, 40, 12, 27, 19, 31, 25, 58],
    # [27, 47, 37, 16, 16, 16, 20, 20, 33],
    # [38, 26, 38, 16, 32, 26, 14, 12, 31]
    [29, 24, 57, 43, 30, 16, 21, 66, 78] ,
    [28, 27, 59, 14, 40, 25,  9, 22, 19] ,
    [35, 67, 29, 22, 25, 25, 23, 36, 30] ,
    [18, 43, 29, 25, 11,  9, 38, 43, 28] ,
    [26, 17, 52, 13, 17, 12, 31, 23, 31] ,
    [27, 27, 28, 29, 18, 26, 18, 30, 27] ,
    [49, 34, 91, 58, 88, 29, 20, 36, 44] ,
    [16, 20, 47, 14, 30,  9,  7,  7, 44] ,
    [26, 60, 26, 17, 23, 31,  7,  9, 39] ,
    [14, 23, 32,  8, 22, 23, 21, 40, 21] ,
    [27, 16, 47, 11, 37, 18, 19, 15,  9] ,
    [41, 12, 32, 12, 29, 13, 15, 10, 29] ,
    [52, 24, 36, 30, 21, 15,  5, 14, 18] ,
    [28, 26, 32, 15, 27, 28, 41, 27, 47] ,
    [55, 29, 35, 27, 40, 20, 21, 17, 33] ,
    [20, 24, 68, 52, 35,  8, 15, 41, 18] ,
    [41, 36, 40, 11, 60, 11,  9, 22, 30] ,
    [17, 26, 41, 22, 10, 18, 16, 18, 15] ,
    [33, 62, 39, 11, 26, 18, 30, 24, 58] ,
    [26, 46, 36, 15, 15, 15, 19, 19, 32] ,
    [37, 25, 36, 15, 31, 25, 14, 12, 30]
])
if norm:
    # minimum = np.min(visit_length)
    # maximim = np.max(visit_length)
    # visit_length -= minimum
    # visit_length = visit_length / (maximim - minimum)
    visit_length = normalize(visit_length)

visit_duration = np.array([
    # [284.489, 170.064, 593.648, 458.147, 480.341, 588.302, 173.641, 299.552, 537.534],
    # [354.068, 218.199, 565.857, 701.575, 697.462, 682.596, 310.684, 3600.86, 398.393],
    # [454.254, 631.883, 445.107, 581.808, 625.618, 636.066, 358.972, 821.563,  521.22],
    # [404.005, 626.483, 567.608, 829.991, 763.548, 489.894, 543.559, 347.081, 820.861],
    # [564.074, 402.324, 625.725, 629.153, 801.834, 648.349, 346.461, 203.639, 503.031],
    # [548.836, 356.985, 573.074, 849.71 , 618.023, 716.338, 353.227, 1056.38, 442.141],
    # [454.312, 369.617, 587.367, 626.244, 573.051, 472.01 , 274.565, 246.945, 284.613],
    # [269.752, 219.182, 861.698, 1014.25, 804.404, 444.074, 136.649, 195.155,  887.16],
    # [349.591, 591.7  , 252.099, 831.168, 557.796, 870.622, 291.146, 136.001, 697.842],
    # [291.552, 279.853, 510.074, 409.767, 679.267, 640.41 , 314.937, 547.181, 731.976],
    # [476.097, 239.142, 498.354, 421.814, 603.703, 659.428, 163.98 , 191.954,  184.77],
    # [673.587, 338.936, 787.144, 819.702, 772.819, 912.73 , 261.135, 141.491, 413.541],
    # [647.783, 393.003, 822.535, 842.88 , 472.229, 791.121, 224.39 , 211.569, 745.484],
    # [344.449, 348.182, 461.715, 645.493, 685.178, 648.312, 576.851, 481.027, 660.149],
    # [493.449, 461.792, 596.231, 516.381, 532.722, 860.43 , 205.371, 152.81 , 300.547],
    # [362.928, 431.421, 661.301, 1097.99, 631.376, 100.085, 244.219, 265.547,  798.45],
    # [787.984, 604.285, 590.454, 886.052, 885.347, 458.989, 210.805, 452.489, 496.706],
    # [361.452, 370.513, 951.63 , 691.388, 721.875, 846.208, 302.704, 309.352, 264.074],
    # [552.041, 633.778, 601.036, 376.018, 473.715, 618.305, 194.733, 247.922, 1272.85],
    # [466.602, 808.905, 655.656, 648.39 , 616.177, 540.246, 256.277, 1277.92, 359.609],
    # [650.564, 483.616, 791.709, 610.443, 600.113, 618.347, 231.242, 292.754,  565.56]
    [284.489, 170.064, 593.648, 400.565, 480.341, 588.302, 173.641, 299.552, 528.253] ,
    [260.689, 174.644, 545.783, 475.378, 659.406, 559.945, 204.612, 377.401, 396.163] ,
    [405.196, 580.993, 400.751, 453.114, 506.934, 527.872, 264.981, 338.408, 521.22] ,
    [269.564, 626.483, 567.608, 710.458, 750.348, 442.037, 505.368, 324.833, 292.869] ,
    [422.683, 299.258, 584.943, 459.499, 684.107, 416.249, 301.092, 203.639, 454.596] ,
    [ 485.36, 301.025, 520.727, 773.686,  481.29, 589.447, 310.104, 383.629, 367.654] ,
    [ 338.35, 357.992, 576.084, 586.089, 531.219, 382.657, 259.577, 246.945, 284.613] ,
    [195.524, 181.573,  604.86, 915.937, 798.188, 234.594,  109.98, 149.182, 579.835] ,
    [296.519,   591.7, 234.608, 805.175, 461.006, 852.182, 262.068, 136.001, 690.937] ,
    [267.045, 265.499, 377.551, 281.499, 614.877,   571.8, 290.819,  525.65, 286.364] ,
    [467.376, 208.554, 498.354, 288.225, 570.177, 415.202, 144.518, 191.954, 151.321] ,
    [628.459, 283.833, 722.479, 717.971,  664.38, 665.968, 229.879, 141.491, 377.768] ,
    [634.986, 393.003, 750.537, 609.589, 449.871, 580.035, 214.614, 204.803, 118.736] ,
    [323.689,  275.48, 439.113, 541.271,  640.66, 624.248, 558.425, 481.027, 635.973] ,
    [ 469.21, 380.921, 489.074, 470.392, 464.872, 738.842, 189.753,  152.81, 269.852] ,
    [304.013, 389.461, 635.043, 1058.45, 542.114,  81.668,  196.49, 241.894, 798.45] ,
    [713.009, 568.123, 564.287, 756.953, 851.461, 455.168, 180.848, 452.489, 464.794] ,
    [329.085, 333.546, 918.145, 662.648, 451.174, 841.737,  267.93, 309.352, 249.687] ,
    [462.965, 446.609, 545.524, 274.662, 384.682, 453.619, 170.615, 221.912, 1272.85] ,
    [ 279.44, 754.755, 551.952, 472.542,  535.99, 505.866, 247.567, 272.73 , 329.263] ,
    [602.858, 408.209, 569.714, 516.607, 591.927, 506.952, 231.242, 292.754, 527.989]
])
if norm:
    # minimum = np.min(visit_duration)
    # maximim = np.max(visit_duration)
    # visit_duration -= minimum
    # visit_duration = visit_duration / (maximim - minimum)
    visit_duration = normalize(visit_duration)

task_efficiency = np.array([
    [0.3914, 0.8349, 0.1734, 0.2953, 0.3652, 0.7073, 0.3013, 0.1555, 0.0236],
    [0.3493, 0.2230, 0.1203, 0.5413, 0.3363, 0.1909, 0.2000, 0.2789, 0.1092],
    [0.3773, 0.3828, 0.2194, 0.9510, 0.3523, 0.1459, 0.5178, 0.3354, 0.1486],
    [0.8519, 0.0132, 0.9356, 0.2619, 0.2424, 0.6350, 0.1307, 0.2108, 0.4437],
    [0.6763, 1.0000, 0.1768, 0.2941, 0.4139, 0.1838, 0.1653, 0.2085, 0.3438],
    [0.4058, 0.6904, 0.8488, 0.3307, 0.6835, 0.3035, 0.4376, 0.2549, 0.1480],
    [0.1710, 0.3889, 0.1416, 0.3463, 0.3185, 0.3787, 0.2169, 0.3026, 0.1248],
    [0.9092, 0.4515, 0.3546, 0.9096, 0.1097, 0.6171, 0.3828, 0.2620, 0.0227],
    [0.2801, 0.0622, 0.5126, 0.1507, 0.4041, 0.1580, 0.2030, 0.3736, 0.2147],
    [0.9185, 0.9085, 0.5782, 0.7907, 0.5268, 0.7795, 0.4011, 0.3871, 0.3176],
    [0.6170, 0.4798, 0.4606, 0.9997, 0.3488, 0.2315, 0.3725, 0.3466, 0.9038],
    [0.2540, 0.4503, 0.2221, 0.3174, 0.2557, 0.2100, 0.3249, 0.4583, 0.2513],
    [0.2862, 0.3142, 0.4412, 0.5925, 0.3559, 0.5147, 0.3730, 0.3280, 0.1573],
    [0.4749, 0.3633, 0.4239, 0.5136, 0.6098, 0.3792, 0.1011, 0.6635, 0.3289],
    [0.2866, 0.5425, 0.3245, 0.2327, 0.1987, 0.1608, 0.1386, 0.2576, 0.2490],
    [0.3820, 0.6696, 0.2078, 0.2347, 0.2221, 0.2549, 0.2753, 0.4002, 0.9433],
    [0.7425, 0.3004, 0.4946, 0.5096, 0.2195, 0.7292, 0.6073, 0.4422, 0.2136],
    [0.7876, 0.6121, 0.9163, 0.2514, 1.0000, 0.1442, 0.3904, 0.3788, 0.2986],
    [0.4303, 0.1888, 0.5342, 1.0000, 0.6691, 0.3953, 0.4746, 0.3520, 0.5817],
    [0.3187, 0.6652, 0.2073, 0.2853, 0.6462, 0.1147, 0.3896, 0.2477, 0.0901],
    [0.3369, 0.7462, 0.6191, 0.7516, 0.5547, 0.3175, 0.0625, 0.4585, 0.3451],
])
if norm:
    # minimum = np.min(task_efficiency)
    # maximim = np.max(task_efficiency)
    # task_efficiency -= minimum
    # task_efficiency = task_efficiency / (maximim - minimum)
    task_efficiency = normalize(task_efficiency)

# task_goal = difficulty.T[[0, 3, 6]].T
# task_fuzzy = difficulty.T[[1, 4, 7]].T
# task_exploring = difficulty.T[[2, 5, 8]].T

task_goal = task_efficiency.T[[0, 3, 6]].T
task_fuzzy = task_efficiency.T[[1, 4, 7]].T
task_exploring = task_efficiency.T[[2, 5, 8]].T

print('mean efficiency_goal: ', np.mean(task_goal))
print('mean efficiency_fuzzy: ', np.mean(task_fuzzy))
print('mean efficiency_exploring: ', np.mean(task_exploring))

length_goal = visit_length.T[[0, 3, 6]].T
length_fuzzy = visit_length.T[[1, 4, 7]].T
length_exploring = visit_length.T[[2, 5, 8]].T

print('mean length_goal: ', np.mean(length_goal))
print('mean length_fuzzy: ', np.mean(length_fuzzy))
print('mean length_exploring: ', np.mean(length_exploring))

duration_goal = visit_duration.T[[0, 3, 6]].T
duration_fuzzy = visit_duration.T[[1, 4, 7]].T
duration_exploring = visit_duration.T[[2, 5, 8]].T

print('mean duration_goal: ', np.mean(duration_goal))
print('mean duration_fuzzy: ', np.mean(duration_fuzzy))
print('mean duration_exploring: ', np.mean(duration_exploring))

# From same distribution

def ks2sample_test(name1, name2, data1, data2, p = 0.05):
    p = stats.ks_2samp(data1.flatten(), data2.flatten()).pvalue
    if p < 0.05:
        print(f'{name1} \tv.s. {name2}: \treject H0, p: ', p)
    else:
        print(f'{name1} \tv.s. {name2}: \taccept H0, p: ', p)



def mannwhitneyu_test(name1, name2, data1, data2, p = 0.05):
    p = stats.mannwhitneyu(data1.flatten(), data2.flatten()).pvalue
    if p < 0.05:
        print(f'{name1} \tv.s. {name2}: \treject H0, p: ', p)
    else:
        print(f'{name1} \tv.s. {name2}: \taccept H0, p: ', p)


def significant_tests():
    tests = [
        {
            'name1': 'task_fuzzy',
            'name2': 'task_exploring',
            'data1': task_fuzzy,
            'data2': task_exploring,
            'p': 0.05
        },
        {
            'name1': 'task_goal',
            'name2': 'task_exploring',
            'data1': task_goal,
            'data2': task_exploring,
            'p': 0.05
        },
        {
            'name1': 'task_fuzzy',
            'name2': 'task_goal',
            'data1': task_fuzzy,
            'data2': task_goal,
            'p': 0.05
        },

        {
            'name1': 'length_fuzzy',
            'name2': 'length_exploring',
            'data1': length_fuzzy,
            'data2': length_exploring,
            'p': 0.05
        },
        {
            'name1': 'length_goal',
            'name2': 'length_exploring',
            'data1': length_goal,
            'data2': length_exploring,
            'p': 0.05
        },
        {
            'name1': 'length_fuzzy',
            'name2': 'length_goal',
            'data1': length_fuzzy,
            'data2': length_goal,
            'p': 0.05
        },

        {
            'name1': 'duration_fuzzy',
            'name2': 'duration_exploring',
            'data1': duration_fuzzy,
            'data2': duration_exploring,
            'p': 0.05
        },
        {
            'name1': 'duration_goal',
            'name2': 'duration_exploring',
            'data1': duration_goal,
            'data2': duration_exploring,
            'p': 0.05
        },
        {
            'name1': 'duration_fuzzy',
            'name2': 'duration_goal',
            'data1': duration_fuzzy,
            'data2': duration_goal,
            'p': 0.05
        }
    ]

    print('H0: data from same distribution')
    print('H1: data not from same distribution')
    for t in tests:
        ks2sample_test(t['name1'], t['name2'], t['data1'], t['data2'])

    print('H0: samples not show significant difference')
    print('H1: samples show significant difference')
    for t in tests:
        mannwhitneyu_test(t['name1'], t['name2'], t['data1'], t['data2'])



# H0: data from same distribution
# H1: data not from same distribution

# task_fuzzy      v.s. task_exploring:    reject H0, p:  2.548471762285516e-05
# task_goal       v.s. task_exploring:    reject H0, p:  0.046973677697447175
# task_fuzzy      v.s. task_goal:         reject H0, p:  0.004865388750615347

# length_fuzzy    v.s. length_exploring:  accept H0, p:  0.2653845643858763
# length_goal     v.s. length_exploring:  reject H0, p:  0.02801532091008028
# length_fuzzy    v.s. length_goal:       accept H0, p:  0.18114976435522995

# duration_fuzzy  v.s. duration_exploring:reject H0, p:  0.01616038345029024
# duration_goal   v.s. duration_exploring:reject H0, p:  0.00486538875061536
# duration_fuzzy  v.s. duration_goal:     accept H0, p:  0.808651341574673

# H0: samples not show significant difference
# H1: samples show significant difference

# task_fuzzy      v.s. task_exploring:    reject H0, p:  4.971082568554275e-05
# task_goal       v.s. task_exploring:    reject H0, p:  0.005342226014935479
# task_fuzzy      v.s. task_goal:         reject H0, p:  0.014573552905790875

# length_fuzzy    v.s. length_exploring:  accept H0, p:  0.11691680667664384
# length_goal     v.s. length_exploring:  reject H0, p:  0.0018327479412754979
# length_fuzzy    v.s. length_goal:       reject H0, p:  0.025777669047580186

# duration_fuzzy  v.s. duration_exploring:reject H0, p:  0.0032867528951321993
# duration_goal   v.s. duration_exploring:reject H0, p:  0.000461548309969623
# duration_fuzzy  v.s. duration_goal:     accept H0, p:  0.3145335442741327

# mean length_goal:  0.2585755837403175
# mean length_fuzzy:  0.3098150772361861
# mean length_exploring:  0.33711495680528586
# mean duration_goal:  0.28224403385520425
# mean duration_fuzzy:  0.28587927211314296
# mean duration_exploring:  0.35275456730571414

# (difficulty, length of clickstream, time duration of clickstream)
# difficulty: explore < goal < fuzzy
# length:     goal < {exploring, fuzzy}
# duration:   {goal, fuzzy} < {exploring}

# -------------------------------------------------------------------------------------

# idx = [0,1,2]
# idx = [1,2,3]
# idx = [2,3,4]
# idx = [3,4,5]
# idx = [4,5,6]
# idx = [5,6,7]
# idx = [6,7,8]
# idx = [0,  2]

def get_data_by_task_id(idx):
    # x = difficulty[:,idx].flatten()
    x = task_efficiency[:,idx].flatten()
    y = visit_length[:,idx].flatten()
    z = visit_duration[:,idx].flatten()
    w = np.multiply(y, 1/z)
    data = np.concatenate((
        x[np.newaxis].T,y[np.newaxis].T,z[np.newaxis].T,
    ), axis=1)
    data_avg = np.concatenate((x[np.newaxis].T,w[np.newaxis].T), axis=1)

    colors = task_color[:,idx].flatten()
    labels = task_type[:,idx].flatten()
    colorlabel = np.concatenate((colors[np.newaxis].T, labels[np.newaxis].T), axis=1)
    return data, colorlabel

def plot_2d(x, y, labels, path, xlabel, ylabel, xlim, ylim, title, region=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    if region:
        xx = np.expand_dims(np.array(x), axis=1)
        yy = np.expand_dims(np.array(y), axis=1)
        X = np.concatenate((xx, yy), axis=1)
        yy = []
        colors = []
        for idx, _ in enumerate(labels[:,1]):
            if 'goal' in labels[:,1][idx]:
                yy.append(0)
                colors.append(labels[:,0][idx])
            elif 'fuzzy' in labels[:,1][idx]:
                yy.append(1)
                colors.append(labels[:,0][idx])
            elif 'exploring' in labels[:,1][idx]:
                yy.append(2)
                colors.append(labels[:,0][idx])

        try:
            yy = np.array(yy)
            clf = svm.SVC(kernel='rbf', gamma='scale')
            clf.fit(X, yy)

            x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
            y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
            xx, yyy = np.meshgrid(np.arange(x_min, x_max, 0.01),
                                np.arange(y_min, y_max, 0.01))
            Z = clf.predict(np.c_[xx.ravel(), yyy.ravel()])
            Z = Z.reshape(xx.shape)
            plt.contourf(xx, yyy, Z, colors=list(set(colors)))
        except:
            pass

    for i, l in enumerate(types):
        xx = [value for index, value in enumerate(x) if labels[:,1][index] == l]
        yy = [value for index, value in enumerate(y) if labels[:,1][index] == l]
        cc = [value for index, value in enumerate(labels[:,0]) if labels[:,1][index] == l]
        if len(xx) > 0:
            ax.scatter(xx, yy, c=cc, marker=markers[i], label=l)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    ax.set_title(title, y=1.0)
    ax.legend()
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.savefig(path, bbox_inches='tight', format='eps')
    plt.close(fig)

def plot_2dtsne(data, labels, path):
    X_tsne = TSNE(n_components=2).fit_transform(data)
    amin = np.amin(X_tsne)
    amax = np.amax(X_tsne)
    plot_2d(X_tsne[:,0],X_tsne[:,1], labels, path, '', '', (amin, amax), (amin, amax),
    "t-SNE visualization", region=False)

def plot_2d_len_dur(idx, category):
    data, colorlabel = get_data_by_task_id(idx)
    xtrain, xtest, ytrain, ytest = train_test_split(data, colorlabel, test_size=0.0, random_state=42)
    plot_2d(xtrain[:,1],xtrain[:,2], ytrain, 
    f'2d-len-dur-{category}.eps', 'number of actions in a session', 
    'total time duration of a session', (0, 1), (0, 1),
    "", region=False)

def plot_2d_eff_len(idx, category):
    data, colorlabel = get_data_by_task_id(idx)
    xtrain, xtest, ytrain, ytest = train_test_split(data, colorlabel, test_size=0.0, random_state=42)
    plot_2d(xtrain[:,0],xtrain[:,1], ytrain, 
    f'2d-eff-len-{category}.eps', 'task completion efficiency', 
    'number of actions in a session', (0, 1), (0, 1),
    "", region=False)

def plot_2d_dif_dur(idx, category):
    data, colorlabel = get_data_by_task_id(idx)
    xtrain, xtest, ytrain, ytest = train_test_split(data, colorlabel, test_size=0.0, random_state=42)
    plot_2d(xtrain[:,0],xtrain[:,2], ytrain, 
    f'2d-eff-dur-{category}.eps', 'task completion efficiency', 
    'total time duration of a session', (0, 1), (0, 1),
    "", region=False)

def plot_tsne(idx, category):
    data, colorlabel = get_data_by_task_id(idx)
    xtrain, xtest, ytrain, ytest = train_test_split(data, colorlabel, test_size=0.0, random_state=42)
    plot_2dtsne(xtrain, ytrain, f'tsne-{category}.eps')

def plot_3d(data, labels, path, xlabel, ylabel, zlabel):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i, l in enumerate(types):
        xx = [value for index, value in enumerate(data[:,0]) if labels[:,1][index] == l]
        yy = [value for index, value in enumerate(data[:,1]) if labels[:,1][index] == l]
        zz = [value for index, value in enumerate(data[:,2]) if labels[:,1][index] == l]
        cc = [value for index, value in enumerate(labels[:,0]) if labels[:,1][index] == l]
        if len(xx) > 0:
            ax.scatter(xx, yy, zz, c=cc, marker=markers[i], label=l)
        ax.legend()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    ax.set_xlim((0,1))
    ax.set_ylim((0,1))
    ax.set_zlim((0,1))
    # plt.show()
    # plt.close()
    plt.savefig(path, bbox_inches='tight')
    plt.close(fig)

def plot_3draw(idx, category):
    data, colorlabel = get_data_by_task_id(idx)
    xtrain, xtest, ytrain, ytest = train_test_split(data, colorlabel, test_size=0.0, random_state=42)
    plot_3d(xtrain, ytrain, f'3d-len-dur-{category}.png', 
        'task completion efficiency', 
        'number of actions in a session', 
        'total time duration of a session'
    )

def plot_features():
    idxs_by_type = {
        'amazon':   [0,1,2],
        'medium':   [3,4,5],
        'dribbble': [6,7,8]
    }
    idxs_by_website = {
        'goal':   [0,3,6],
        'fuzzy':   [1,4,7],
        'exploring': [2,5,8]
    }

    for category, idx in idxs_by_type.items():
        plot_2d_len_dur(idx, category)
        plot_2d_eff_len(idx, category)
        plot_2d_dif_dur(idx, category)
        plot_tsne(idx, category)
        plot_3draw(idx, category)

    for category, idx in idxs_by_website.items():
        plot_2d_len_dur(idx, category)
        plot_2d_eff_len(idx, category)
        plot_2d_dif_dur(idx, category)
        plot_tsne(idx, category)
        plot_3draw(idx, category)

def learn_svm_f1(data, labels):
    while True:
        xtrain, xtest, ytrain, ytest = train_test_split(data, labels, test_size=0.2)
        if len(list(set(ytrain[:, 1]))) < 3 or len(list(set(ytest[:, 1]))) < 3:
            continue
        clf = svm.SVC(kernel='rbf', gamma='scale')
        clf.fit(xtrain, ytrain[:, 1])
        ypred = clf.predict(xtest)
        v = cohen_kappa_score(ytest[:, 1], ypred)
        return v

def clf_report(data, labels):
    while True:
        xtrain, xtest, ytrain, ytest = train_test_split(data, labels, test_size=0.5)
        if len(list(set(ytrain[:, 1]))) < 3 or len(list(set(ytest[:, 1]))) < 3:
            continue
        clf = svm.SVC(kernel='rbf', gamma='scale')
        clf.fit(xtrain, ytrain[:, 1])
        ypred = clf.predict(xtest)
        v = classification_report(ytest[:, 1], ypred)

        #importance
        model = ExtraTreesClassifier()
        model.fit(xtrain, ytrain)
        print('task_efficiency/visited_length/visited_duration importance: ', list(set(ytrain[:, 1])), model.feature_importances_)
        return v


def clf():
    idxs_by_type = [
        [0,1,2],
        [3,4,5],
        [6,7,8]
    ]
    idxs_by_website = [
        [0,3,6],
        [1,4,7],
        [2,5,8]
    ]
    for idx in idxs_by_type:
        x, y = get_data_by_task_id(idx)
        print(clf_report(x, y))
    for idx in idxs_by_website:
        x, y = get_data_by_task_id(idx)
        print(clf_report(x, y))

    # classify goal/fuzzy/explore
    # 0.027624309392265234
    # 0.276595744680851
    # 0.0
    # 
    # classify amazon/dribble/medium
    # 0.30434782608695654
    # 0.26881720430107525
    # 0.0

def main():
    # significant_tests()
    plot_features()
    # clf()


# 结论：

# - difficulty: fuzzy > goal > exploring

#                 tp / (tp + fp)
#                              tp / (tp + fn)       The number of occurrences of each label in y_true.

# feature importance

# task_efficiency/visited_length/visited_duration importance:  ['goal_amazon', 'fuzzy_amazon', 'exploring_amazon'] 
# [0.26795169 0.36754544 0.36450287] length
# task_efficiency/visited_length/visited_duration importance:  ['fuzzy_medium', 'goal_medium', 'exploring_medium'] 
# [0.29025323 0.39860784 0.31113893] length
# task_efficiency/visited_length/visited_duration importance:  ['fuzzy_dribbble', 'exploring_dribbble', 'goal_dribbble'] 
# [0.24160315 0.39226943 0.36612743] length
# task_efficiency/visited_length/visited_duration importance:  ['goal_amazon', 'goal_medium', 'goal_dribbble'] 
# [0.30868672 0.32416932 0.36714397] duration
# task_efficiency/visited_length/visited_duration importance:  ['fuzzy_medium', 'fuzzy_dribbble', 'fuzzy_amazon'] 
# [0.3426562  0.30083865 0.35650515] duration
# task_efficiency/visited_length/visited_duration importance:  ['exploring_medium', 'exploring_amazon', 'exploring_dribbble'] 
# [0.31325273 0.38611585 0.30063142] length

#                   precision    recall  f1-score   support

# exploring_amazon       0.39      0.88      0.54         8
#     fuzzy_amazon       0.00      0.00      0.00        12
#      goal_amazon       0.36      0.42      0.38        12

#        micro avg       0.38      0.38      0.38        32
#        macro avg       0.25      0.43      0.31        32
#     weighted avg       0.23      0.38      0.28        32

#                   precision    recall  f1-score   support

# exploring_medium       0.35      0.70      0.47        10
#     fuzzy_medium       0.00      0.00      0.00        12
#      goal_medium       0.42      0.50      0.45        10

#        micro avg       0.38      0.38      0.38        32
#        macro avg       0.26      0.40      0.31        32
#     weighted avg       0.24      0.38      0.29        32

#                     precision    recall  f1-score   support

# exploring_dribbble       0.50      0.10      0.17        10
#     fuzzy_dribbble       0.30      1.00      0.46         9
#      goal_dribbble       0.00      0.00      0.00        13

#          micro avg       0.31      0.31      0.31        32
#          macro avg       0.27      0.37      0.21        32
#       weighted avg       0.24      0.31      0.18        32

#                precision    recall  f1-score   support

#   goal_amazon       1.00      0.15      0.27        13
# goal_dribbble       0.53      1.00      0.69        10
#   goal_medium       0.73      0.89      0.80         9

#     micro avg       0.62      0.62      0.62        32
#     macro avg       0.75      0.68      0.59        32
#  weighted avg       0.78      0.62      0.55        32

#                 precision    recall  f1-score   support

#   fuzzy_amazon       0.38      0.60      0.46        10
# fuzzy_dribbble       0.58      0.78      0.67         9
#   fuzzy_medium       0.75      0.23      0.35        13

#      micro avg       0.50      0.50      0.50        32
#      macro avg       0.57      0.54      0.49        32
#   weighted avg       0.59      0.50      0.48        32

#                     precision    recall  f1-score   support

#   exploring_amazon       0.82      0.82      0.82        11
# exploring_dribbble       1.00      0.42      0.59        12
#   exploring_medium       0.56      1.00      0.72         9

#          micro avg       0.72      0.72      0.72        32
#          macro avg       0.79      0.74      0.71        32
#       weighted avg       0.81      0.72      0.70        32
if __name__ == "__main__":
    main()