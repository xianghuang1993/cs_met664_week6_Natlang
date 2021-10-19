import textrazor
from textblob import TextBlob

# The API key for textrazor.
textrazor.api_key = "4cd41a6aa25a05b3c63e1f2d31a38c85aa3e855628feb4ecc4663193"
# Word list and entities extraction from a sentence.
client = textrazor.TextRazor(extractors=["entities", "words"])
# Word list.
wordList = ['CORRECT','YES','CANCEL']
# Words to end conversation.
endConversation = ['OKAY','I SEE','THANKS','BYE','GOT IT']
# The random order number for illustration purpose in this example.
orderNumber = '17356306608'
# The order information.
orderInformation = {'Name':'Julia Hawkins', 'Product':'Sweater', 'Amount':'$99'}

# Method to prompt for user input.
def userInput():
    userInput = input()
    return userInput

# Method to start the conversation.
def startConversation():
    sentence = userInput()
    sentiment = sentimentAnalysis(sentence)
    # Default greeting reply.
    reply = 'Hi, this is Nat robot. '
    print(reply)
    # Depending on the sentiment analysis result, reply different sentences to client.
    if sentiment == 'positive':
        print('It is my pleasure to help you. ')
    elif sentiment == 'neutral':
        print('What can I do for you? ')
    elif sentiment == 'negative':
        print('Sorry to hear that, I will try my best to help you solve any problems you have. ')
    print('Can I know the order number to verification purpose?')

# Method for sentiment analysis.
def sentimentAnalysis(sentence):
    # Call for TexBlob to query the sentiment polarity.
    analysisPol = TextBlob(sentence).polarity
    # Categorize the score into positive, neutral and negative, it ban be adjusted in the future.
    if analysisPol > 0.2:
        return 'positive'
    elif analysisPol >= -0.2 and analysisPol <= 0.2:
        return 'neutral'
    elif analysisPol < -0.2:
        return 'negative'

# Method to extract the words and entities from reply.
def entitiesWordsExtraction(sentence):
    information = {'entities':[],'words':[]}
    entities = list(sentence.entities())
    for entity in entities:
        if entity.id not in information['entities']:
            information['entities'].append(entity.id)
    words = list(sentence.words())
    for word in words:
        if word not in information['words']:
            information['words'].append(word)
    return information

# Method to generate the response  based on the text processing result.
def generateResponse():
    while True:
        sentence = userInput()
        # Get response result.
        response = client.analyze(sentence)
        # Determine entities, and reply different sentences.
        entitiesAndWords = entitiesWordsExtraction(response)
        for entity in entitiesAndWords['entities']:
            if entity == orderNumber:
                print('Is below order information correct?')
                print('Name: {}, Product: {}, Amount: {}.'.format(orderInformation['Name'],orderInformation['Product'],orderInformation['Amount']))

        # Determine words, and reply different sentences.
        for word in entitiesAndWords['words']:
            if word.lemma.upper() == wordList[0] or word.lemma.upper() == wordList[1]:
                print('Okay, what can I do for you?')
            elif word.lemma.upper() == wordList[2]:
                print('Please complete the order cancellation form and your refund will be deposited into your account in next 5 working days.')
            elif word.lemma.upper() in endConversation:
                print('Hope this is helpful, have a good day, bye!')
                break

# Method to start the conversation.
def start():
    startConversation()
    generateResponse()

# Start the application.
if __name__ == '__main__':
    start()

