from wordcloud import WordCloud
import matplotlib
# matplotlib.use("gtk")
import matplotlib.pyplot as plt
import pickle


def word_cloud_run(path):
    with open(path+'/word_cloud.pickle', 'rb') as handle:
        d2 = pickle.load(handle)

    # reader = csv.reader(open('namesDFtoCSV', 'r',newline='\n'))
    # for k,v in reader:
    #     d[k] = int(v)
    # d = {"A":10,"B":2,"C":43}
    # d2 = {}
    # cnt = 0
    # for key in d:
    #     d2[str(key)] = d[key]
    #     cnt +=1
    #     if cnt == 1000:
    #         break

    # d2 = { str(key):int(d[key]) for key in d}
    # d2 = {'(183, 96, 89)': 1, '(207, 110, 67)': 1, '(139, 7, 2)': 1, '(176, 56, 58)': 1, '(240, 225, 132)': 3, '(245, 177, 30)': 4, '(156, 5, 14)': 8}
    # print d2
    # print len(d2)
    # Generating wordcloud. Relative scaling value is to adjust the importance of a frequency word.
    # See documentation: https://github.com/amueller/word_cloud/blob/master/wordcloud/wordcloud.py
    wordcloud = WordCloud(width=900, height=500, max_words=len(d2), relative_scaling=1,
                          normalize_plurals=False).generate_from_frequencies(d2)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    # plt.show()
    # plt.ion()
    plt.savefig(path+"/word_cloud.png")
    # plt.show()