### Notes for Documentation 

1. Dataset Selection
    - About the data.
    - Explain the thought process behind selection of the data. 
    - Thought Process: 
        - We wanted large dataset with good number of records. 
        - Since its a classification, we wanted 
        - The select text should require a lot of preprocessing. we wanted data that require extensive text 
            cleaning. 

    - Characteristics about data: 



2. Data Scrubbing 
    - Follow the notebook. 

3. EDA
    - Follow the notebook.

4. Text Processing 
    - Text processing is divided into 2 steps. 
    1. Text Cleaning
    2. Text Normalization 

    **Text Cleaning**

    a. Tokenization

    For text cleaning we first define the tokenizer class: 

        ```code
        class Tokenizer:
            def __init__(self) -> None:
                self.tokenizer = RegexpTokenizer("[\w']+")
        ```
    The Tokenizer class uses `RegexpTokenizer` which uses the `[\w']+` pattern to look for alphanumeric characters and apostrophes. Here we are preserving the contractions. 
    
    For example: 
    Input text ```"It's so hot in Toronto, isn't it?"``` will be broken as ```["It's", 'so', 'hot', 'in', 'Toronto', "isn't", 'it']```. 

    b. Text Cleaning 
    
    Text cleaning is done via text cleaner class that inherits tokenization from Tokenizer class and works applies following cleaning to text: 

    ```
    lowercase -> remove white space -> remove punctuation -> remove html -> remove emoji -> convert acronyms -> convert contractions
     
    ```
    Convert this to flowchart. And explain each of the steps. 

    i. Lowercase conversion 

    Write why do we do lowercase? Take reference from : [LINK](https://www.kaggle.com/code/sugataghosh/e-commerce-text-classification-tf-idf-word2vec?scriptVersionId=107548253&cellId=39)





    ... 


    iiii. Convert Contractions

    Same, take reference from this link. [LINK](https://www.kaggle.com/code/sugataghosh/e-commerce-text-classification-tf-idf-word2vec?scriptVersionId=107548253&cellId=59)



    **Note:⚠️⚠️**  Take reference of everything from this link. [LINK](https://www.kaggle.com/code/sugataghosh/e-commerce-text-classification-tf-idf-word2vec?scriptVersionId=107548253&cellId=59)


    c. Text Normalization 

    Text Normalization is done via TextPreProcess class that inherits tokenization from Tokenizer class and works applies following normalization to text:
    
            word_list = self.remove_stopwords(word_list)
            word_list = self.pyspellchecker(word_list)
            word_list = self.porter_stemmer(word_list)
            word_list = self.lemmatizer(word_list)
            word_list = self.remove_additional_stopwords(word_list)

    Make flowchart for this and same thing as textcleanser. Everything is at this [LINK](https://www.kaggle.com/code/sugataghosh/e-commerce-text-classification-tf-idf-word2vec?scriptVersionId=107548253&cellId=59). 





5. Text Vectorization  

    a. Bag of WORDS 

        Explain BOW. ADD MATH ALSO + there's wordmap for BAG of words. 
        - Prajwal, your task will be to add mathematical breakdown of these. 

    b. TF-IDF 

        SAME. ADD MATH, ADD EQUATIONS AS MUCH AS YOU CAN!!!!. 
        - Prajwal, your task will be to add mathematical breakdown of these. 


6. Modelling 

    We are using following combinations: 
    
    - Bag of Words + MultinomialNB

    - Bag of Words + RandomForestClassifier

    - TF-IDF + MultinomialNB

    - TFIDF + RandomForestClassifier
    
    Add classification report, confusion matrix for all of the stuffs. You know these i don't need to explain. 


    A bit difficult will be BERT ill explain here use this: 

    
