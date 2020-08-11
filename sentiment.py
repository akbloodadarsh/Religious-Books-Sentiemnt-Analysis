import re 
from textblob import TextBlob 
import PyPDF2 
import textract
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
def clean(word): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", word).split())

def get_sentiment(word): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(clean(word)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0: 
            return 0
        else: return -1
def check_sentiment(filename):
    #open allows you to read the file.
    pdfFileObj = open(filename,'rb')
    #The pdfReader variable is a readable object that will be parsed.
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    #Discerning the number of pages will allow us to parse through all the pages.
    num_pages = pdfReader.numPages
    count = 0
    text = ""
    #The while loop will read each page.
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        text += pageObj.extractText()
    #This if statement exists to check if the above library returned words. It's done because PyPDF2 cannot read scanned files.
    if text != "":
       text = text
    #If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text.
    else:
       text = textract.process(fileurl, method='tesseract', language='eng')
    #Now we have a text variable that contains all the text derived from our PDF file. Type print(text) to see what it contains. It likely contains a lot of spaces, possibly junk such as '\n,' etc.
    #Now, we will clean our text variable and return it as a list of keywords.
    #The word_tokenize() function will break our text phrases into individual words.
    tokens = word_tokenize(text)
    #We'll create a new list that contains punctuation we wish to clean.
    punctuations = ['(',')',';',':','[',']',',']
    #We initialize the stopwords variable, which is a list of words like "The," "I," "and," etc. that don't hold much value as keywords.
    stop_words = stopwords.words('english')
    #We create a list comprehension that only returns a list of words that are NOT IN stop_words and NOT IN punctuations.
    keywords = [word for word in tokens if not word in stop_words and not word in punctuations]

    neg_sum = 0
    pos_sum = 0
    neu_sum = 0
    for word in keywords:
        res = get_sentiment(word)
        if res==1:
            pos_sum += 1
        elif res==-1:
            neg_sum -= 1
        elif res == 0: neu_sum += 1
    print('Negative words: ' + str(neg_sum))
    print('Positive words: ' + str(pos_sum))
    print('Neutral words: ' + str(neu_sum))


print('Bible')
check_sentiment('Bible.pdf')
print('Quran')
check_sentiment('Quran.pdf')
print('Geeta')
check_sentiment('Geeta.pdf')
