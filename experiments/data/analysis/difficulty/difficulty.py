import numpy as np
from scipy import stats
from sklearn.preprocessing import normalize
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, cohen_kappa_score
import matplotlib.pyplot as plt
import seaborn as sns

norm = True
# norm = False

age = [1,4,1,0,2,4,3,0,3,1,1,1]

types = ['goal_amazon', 'fuzzy_amazon', 'exploring_amazon', 'goal_medium', 'fuzzy_medium', 'exploring_medium', 'goal_dribbble', 'fuzzy_dribbble', 'exploring_dribbble']
markers = ['^', 'o', '*', 'x', '+', 'D', '1', 'H', 's']
task_color = np.array([
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'burlywood', 'chartreuse'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'burlywood', 'chartreuse'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'burlywood', 'chartreuse'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'burlywood', 'chartreuse'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'burlywood', 'chartreuse'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'burlywood', 'chartreuse'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'burlywood', 'chartreuse'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'burlywood', 'chartreuse'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'burlywood', 'chartreuse'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'burlywood', 'chartreuse'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'burlywood', 'chartreuse'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'burlywood', 'chartreuse'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'burlywood', 'chartreuse'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'burlywood', 'chartreuse'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'burlywood', 'chartreuse'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'burlywood', 'chartreuse'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'burlywood', 'chartreuse'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'burlywood', 'chartreuse'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'burlywood', 'chartreuse'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'burlywood', 'chartreuse'],
    ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'burlywood', 'chartreuse'],
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
    difficulty = normalize(difficulty)

visit_length = np.array([
    [29, 24, 57, 44, 30, 16, 21, 66, 79],
    [29, 28, 60, 15, 41, 26, 10, 23, 20],
    [36, 68, 30, 23, 26, 26, 24, 37, 30],
    [19, 43, 29, 26, 12, 10, 39, 44, 29],
    [27, 18, 53, 14, 18, 13, 32, 23, 32],
    [28, 28, 29, 30, 19, 27, 19, 31, 28],
    [50, 35, 92, 59, 89, 30, 21, 36, 44],
    [18, 21, 48, 15, 31, 10,  8,  8, 46],
    [27, 60, 27, 18, 24, 32,  9,  9, 40],
    [15, 24, 33,  9, 23, 24, 22, 41, 22],
    [28, 17, 47, 12, 38, 19, 20, 15, 10],
    [42, 13, 33, 13, 30, 14, 16, 10, 30],
    [53, 24, 37, 34, 22, 16,  6, 15, 19],
    [30, 27, 33, 16, 28, 29, 42, 27, 48],
    [56, 30, 36, 28, 41, 21, 22, 17, 34],
    [21, 25, 69, 53, 36,  9, 16, 42, 18],
    [42, 37, 41, 12, 61, 12, 10, 22, 31],
    [18, 27, 42, 23, 11, 19, 17, 18, 16],
    [34, 66, 40, 12, 27, 19, 31, 25, 58],
    [27, 47, 37, 16, 16, 16, 20, 20, 33],
    [38, 26, 38, 16, 32, 26, 14, 12, 31]
])
if norm:
    visit_length = normalize(visit_length)

visit_duration = np.array([
    [284.489, 170.064, 593.648, 458.147, 480.341, 588.302, 173.641, 299.552, 537.534],
    [354.068, 218.199, 565.857, 701.575, 697.462, 682.596, 310.684, 3600.86, 398.393],
    [454.254, 631.883, 445.107, 581.808, 625.618, 636.066, 358.972, 821.563,  521.22],
    [404.005, 626.483, 567.608, 829.991, 763.548, 489.894, 543.559, 347.081, 820.861],
    [564.074, 402.324, 625.725, 629.153, 801.834, 648.349, 346.461, 203.639, 503.031],
    [548.836, 356.985, 573.074, 849.71 , 618.023, 716.338, 353.227, 1056.38, 442.141],
    [454.312, 369.617, 587.367, 626.244, 573.051, 472.01 , 274.565, 246.945, 284.613],
    [269.752, 219.182, 861.698, 1014.25, 804.404, 444.074, 136.649, 195.155,  887.16],
    [349.591, 591.7  , 252.099, 831.168, 557.796, 870.622, 291.146, 136.001, 697.842],
    [291.552, 279.853, 510.074, 409.767, 679.267, 640.41 , 314.937, 547.181, 731.976],
    [476.097, 239.142, 498.354, 421.814, 603.703, 659.428, 163.98 , 191.954,  184.77],
    [673.587, 338.936, 787.144, 819.702, 772.819, 912.73 , 261.135, 141.491, 413.541],
    [647.783, 393.003, 822.535, 842.88 , 472.229, 791.121, 224.39 , 211.569, 745.484],
    [344.449, 348.182, 461.715, 645.493, 685.178, 648.312, 576.851, 481.027, 660.149],
    [493.449, 461.792, 596.231, 516.381, 532.722, 860.43 , 205.371, 152.81 , 300.547],
    [362.928, 431.421, 661.301, 1097.99, 631.376, 100.085, 244.219, 265.547,  798.45],
    [787.984, 604.285, 590.454, 886.052, 885.347, 458.989, 210.805, 452.489, 496.706],
    [361.452, 370.513, 951.63 , 691.388, 721.875, 846.208, 302.704, 309.352, 264.074],
    [552.041, 633.778, 601.036, 376.018, 473.715, 618.305, 194.733, 247.922, 1272.85],
    [466.602, 808.905, 655.656, 648.39 , 616.177, 540.246, 256.277, 1277.92, 359.609],
    [650.564, 483.616, 791.709, 610.443, 600.113, 618.347, 231.242, 292.754,  565.56]
])
if norm:
    visit_duration = normalize(visit_duration)

task_goal = difficulty.T[[0, 3, 6]].T
task_fuzzy = difficulty.T[[1, 4, 7]].T
task_exploring = difficulty.T[[2, 5, 8]].T

length_goal = visit_length.T[[0, 3, 6]].T
length_fuzzy = visit_length.T[[1, 4, 7]].T
length_exploring = visit_length.T[[2, 5, 8]].T

duration_goal = visit_duration.T[[0, 3, 6]].T
duration_fuzzy = visit_duration.T[[1, 4, 7]].T
duration_exploring = visit_duration.T[[2, 5, 8]].T

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


# -------------------------------------------------------------------------------------

# idx = [0,1,2]
# idx = [1,2,3]
# idx = [2,3,4]
# idx = [3,4,5]
# idx = [4,5,6]
# idx = [5,6,7]
# idx = [6,7,8]
# idx = [0,  2]



def get_data(idx):
    x = difficulty[:,idx].flatten()
    y = visit_length[:,idx].flatten()
    z = visit_duration[:,idx].flatten()
    w = np.multiply(y, 1/z)
    data = np.concatenate((x[np.newaxis].T,y[np.newaxis].T,z[np.newaxis].T), axis=1)
    data_avg = np.concatenate((x[np.newaxis].T,w[np.newaxis].T), axis=1)

    colors = task_color[:,idx].flatten()
    labels = task_type[:,idx].flatten()
    colorlabel = np.concatenate((colors[np.newaxis].T, labels[np.newaxis].T), axis=1)
    return data, colorlabel

def plot_3d(x, y, z, colors, lables):
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i, l in enumerate(types):
        xx = [value for index, value in enumerate(x) if labels[index] == l]
        yy = [value for index, value in enumerate(y) if labels[index] == l]
        zz = [value for index, value in enumerate(z) if labels[index] == l]
        cc = [value for index, value in enumerate(colors) if labels[index] == l]
        if len(xx) > 0:
            ax.scatter(xx, yy, zz, c=cc, marker=markers[i], label=l)
        ax.legend()
    plt.show()


def plot_tsne(data, labels, path):
    from sklearn.manifold import TSNE
    from sklearn.decomposition import PCA
    X_tsne = TSNE(n_components=2).fit_transform(data)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i, l in enumerate(types):
        xx = [value for index, value in enumerate(X_tsne[:,0]) if labels[:,1][index] == l]
        yy = [value for index, value in enumerate(X_tsne[:,1]) if labels[:,1][index] == l]
        cc = [value for index, value in enumerate(labels[:,0]) if labels[:,1][index] == l]
        if len(xx) > 0:
            ax.scatter(xx, yy, c=cc, marker=markers[i], label=l)
    ax.legend()
    plt.savefig(path)


# xtrain, xtest, ytrain, ytest = train_test_split(data, colorlabel, test_size=0.0, random_state=42)
# for i in range(0, 10):
#     plot_tsne(xtrain, ytrain, f'tsne-{i}.png')


def learn_svm_f1(data, labels):
    from sklearn import svm
    while True:
        xtrain, xtest, ytrain, ytest = train_test_split(data, labels, test_size=0.5, random_state=42)
        if len(list(set(ytrain[:, 1]))) < 3 or len(list(set(ytest[:, 1]))) < 3:
            continue
        clf = svm.SVC(kernel='rbf', gamma='scale')
        clf.fit(xtrain, ytrain[:, 1])
        ypred = clf.predict(xtest)
        v = cohen_kappa_score(ytest[:, 1], ypred)
        return v

x, y = get_data([0,1,2])
print(learn_svm_f1(x, y))

x, y = get_data([3,4,5])
print(learn_svm_f1(x, y))

x, y = get_data([6,7,8])
print(learn_svm_f1(x, y))


x, y = get_data([0,3,6])
print(learn_svm_f1(x, y))

x, y = get_data([1,4,7])
print(learn_svm_f1(x, y))

x, y = get_data([2,5,8])
print(learn_svm_f1(x, y))