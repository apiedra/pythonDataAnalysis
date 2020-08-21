import tweepy
import csv
import re
import pandas as pd
import numpy as np
from PIL import Image
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS,ImageColorGenerator

#definicion de una clase
class SentimentAnalysis:
#definicion de un método
    def __init__(self):
        self.tweets = []
        self.tweetText = []
        self.searchTerm=''
        self.NoOfTerms=''

    def Adquirir(self):
        # authenticating
        consumerKey = ''
        consumerSecret = ''
        accessToken = ''
        accessTokenSecret = ''
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        # input for term to be searched and how many tweets to search
        searchTerm = input("Tema a buscar: ")
        NoOfTerms = int(input("Número de tweets a buscar: "))

        # searching for tweets
        self.tweets = tweepy.Cursor(
            api.search, q=searchTerm, lang="es").items(NoOfTerms)

        # Open/create a file to append data to
        txtFile = open('tweets.txt', 'w')

        # creating some variables to store info
        polarity = 0
        positive = 0
        negative = 0
        neutral = 0

        # iterating through tweets fetched
        for tweet in self.tweets:
            # Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetText.append(self.limpieza(tweet.text).encode('utf-8'))
            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            analysis = TextBlob(tweet.text)
            # print(analysis.sentiment)  # print tweet's polarity
            # adding up polarities to find the average later
            polarity += analysis.sentiment.polarity

            # adding reaction of how people are reacting to find average later
            if (analysis.sentiment.polarity == 0):
                neutral += 1
            elif (analysis.sentiment.polarity > 0):
                positive += 1
            elif (analysis.sentiment.polarity < 0):
                negative += 1
                # Write to csv and close csv file
            txtFile.write(self.limpieza(tweet.text))

        # finding average of how people are reacting
        positive = self.percentage(positive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)

        # finding average reaction
        polarity = polarity / NoOfTerms

        # printing out data
        print("Reporte de sentimiento sobre " + searchTerm +
              " analizando " + str(NoOfTerms) + " tweets.")
        self.visualizacionChart(positive,negative,neutral, searchTerm, NoOfTerms)

    def limpieza(self, tweet):
        #Remove http
        tweet=tweet.replace("http", "")
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())
    
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def visualizacionChart(self, positive,negative,neutral,searchTerm,noOfSearchTerms):
        labels = ['Positivo [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]','Negativo [' + str(negative) + '%]']
        sizes = [positive,neutral, negative]
        colors = ['lightsalmon', 'grey', 'darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('Reporte de sentimiento sobre ' + searchTerm +
                  ' analizando ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    def visualizacionWordcloud1(self):
        plt.rcParams['font.size'] = 12  # 10
        plt.rcParams['savefig.dpi'] = 100  # 72
        plt.rcParams['figure.subplot.bottom'] = .1
        stopwords = set(STOPWORDS)
        file_content = open("tweets.txt").read()
        wordcloud = WordCloud(
            background_color='white',
            stopwords=stopwords,
            max_words=200,
            max_font_size=40,
            random_state=42
        ).generate(file_content)

        fig = plt.figure(1)
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.show()
        fig.savefig("visualizacionWordcloud1.png", dpi=900)

    def visualizacionWordcloud2(self):
        file_content = open("tweets.txt").read()
        stopwords = set(STOPWORDS)
                # Generate a word cloud image
        mask = np.array(Image.open("r.png"))
        wordcloud_usa = WordCloud(stopwords=stopwords, background_color="white", mode="RGBA", max_words=1000, mask=mask).generate(file_content)

        # create coloring from image
        image_colors = ImageColorGenerator(mask)
        plt.figure(figsize=[7,7])
        plt.imshow(wordcloud_usa.recolor(color_func=image_colors), interpolation="bilinear")
        plt.axis("off")

        # store to file
        plt.savefig("visualizacionWordcloud2.png", format="png")

        plt.show()
    
    
#llamado de las funciones
sa = SentimentAnalysis()
sa.Adquirir()
sa.visualizacionWordcloud1()
sa.visualizacionWordcloud2()
