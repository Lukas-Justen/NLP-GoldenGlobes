# NLP on Golden Globes
_by Vamsi Banda, Eric Yang, Souvik Bagchi and Lukas Justen_ 

**Repository** https://github.com/Lukas-Justen/NLP-on-GoldenGlobes

This project aims to use NLP methods to identify the presenters, nominees, awards, winners and hosts for a given award ceremony. Overall goal of our project was generalizing the strategies so that they will be applicable to any other award ceremony besides the Golden Globes. Although this model is only trained or build on tweets for the Golden Globes we are sure that it will also perform good on other award ceremonies.

Since we knew that the awards will be an integral part of our approach we started out by identifying the award categories. Here we used a chunking approach that allowed us to identify categories based on the underlying syntactic and semantic structure. We created patterns to extract the categories based on this structure. In order to make sure that this approach will also apply to other award ceremonies we included categories from other ceremonies like the Oscars or Grammys. We found out that the resulting patterns are applicable to any other ceremony since the patterns of adjectives and nouns that the categories contain are always the same. 

For the subsequent tasks like identifying the winners, nominees or presenters we categorized the tweets into different groups. A major difficulty was matching the right presenters, winners or nominees to the right awards. Especially the presenters and nominees were hard to identify. For one reason we think that there are less tweets about presenters and nominees compared to winners. That makes it harder to extract the right people. Furthermore, we found that tweets that mention presenters or nominees have a high dependency on time. Therefore we also had to identify the right point in time where is might makes sense to search for the presenters or nominees.  

### Goals
Standard Goals:
- Hosts
- Awards
- Winners
- Presenters
- Nominees  

Additional Goals:
- Dresses (best/worst)
- Moments (fun/sad/surprise/victory/awkward)

### Dependencies

Before you can run the code you will need to install some additional python libraries:

1. ```conda install nltk / pip install nltk```  
  NLTK api comes with supporting packages, please proceed with option - ' y '

2. ```conda install pandas / pip install pandas```  
  Pandas api comes with supporting packages, please proceed with option - ' y '

3. ```pip install google_images_download```  
  Google_images_download API is only supported by pip. Use the above command to install the package.

4. ```conda install spacy / pip install spacy```  
  Spacy comes with supporting packages, please proceed with option - ' y '

5. ```conda install unidecode / pip install unidecode```  
  Unidecode comes with supporting packages, please proceed with option - ' y '
  
6. ```pip install google_images_download```  
  Required for downloading the images of actors and their dresses
  
You will need to download the following additional nltk packages ```punkt```, ```words```, ```stopwords``` and ```averaged_perceptron_tagger```. In order to install the ```punkt``` packages you will need to run this command on the command line:

```python3 -m nltk.downloader punkt```

We found that there is a bug in the nltk library we are using. If you don't fix that bug the code won't find any awards. In order to fix this you have to follow this https://github.com/nltk/nltk/issues/2184 issue. Although the issue has already been fixed with this pull request https://github.com/nltk/nltk/pull/2186 the bug is still in the current version of the library. Open the nltk source library on your local machine and navigate to ```nltk/tag/__init__.py```. Now change the last line of this file from:

```return [_pos_tag(sent, tagset, tagger) for sent in sentences]```

to 

```return [_pos_tag(sent, tagset, tagger, lang) for sent in sentences]```

### Running the Code
In order to run the code and get the results in a .json and a human readable .md format you need to run the main function of the ```gg_api.py``` file. Simply place the ```gg<year>.json.zip``` files in the same folder. If you only want to run the pre_ceremony which will download information from the wikidata knowldge base you have to comment the ```main()``` function call in the ```__main__``` definition. Just like this:

```python
if __name__ == '__main__':
    pre_ceremony()
```

If you want to run both the downloading of the knwoledge base and the actual NLP model, then you have to run the following ```__main__``` function definition:

```python
if __name__ == '__main__':
    pre_ceremony()
    main()
```


### Results
The code will produce two result files. First, it creates a ```results.json``` which contains the results for the autograder. The ```gg_api.py``` will automatically read the content of that file and feed it into the autograder. Secondly, we are creating a ```results.md``` file which is human readable and contains the same results. Furthermore, we added some visualizations to that file which show the results for the additional goals we had.

###### Best Dressed
 0. Kate Hudson (0.11363636363636363) 
 1. Julia Roberts (0.10606060606060606) 
 2. Lucy Liu (0.08333333333333333) 

<img src='https://static.gofugyourself.com/uploads/2013/01/159422573.jpg' height=300px alt='Kate Hudson 2013 Golden Globes Dress'>  <img src='https://media1.popsugar-assets.com/files/thumbor/FH31FkzGw5pcpkJhotijvsmou1I/fit-in/1024x1024/filters:format_auto-!!-:strip_icc-!!-/2013/01/03/1/192/1922398/3d2882dc391eefa7_159445965_10/i/Julia-Roberts-presented-Golden-Globes-black-dress.jpg' height=300px alt='Julia Roberts 2013 Golden Globes Dress'>  <img src='http://applesandonions.com/wp-content/uploads/2013/01/lucy-liu-2013-golden-globes-red-carpet.jpg' height=300px alt='Lucy Liu 2013 Golden Globes Dress'>  

“@PerezHilton: Kate Hudson was also one of my best dressed at the #GoldenGlobes!!! http://t.co/5826njRa” beautiful  

Julia Roberts! Always beautiful #goldenglobes  

RT @bookoisseur: I want to make out with Lucy Liu's dress. It is that pretty. I would go lesbian for that dress. #goldenglobes  

### Autograder
During our development time we achieved the following autograder scores on completeness and spelling:

##### 2013
|   |Hosts   |Awards   |Winners   |Presenters   |Nominees   |
|---|---|---|---|---|---|
|Spelling   |1.0   |0.8845678970073358   |0.7692307692307693   |0.5   |0.5066666666666667   |
|Completeness   |1.0   |0.25972222222222224   |   |0.19807692307692307   |0.07291111111111111   |

##### 2015
|   |Hosts   |Awards   |Winners   |Presenters   |Nominees   |
|---|---|---|---|---|---|
|Spelling   |1.0   |0.8845678970073358   |0.7307692307692307   |0.4790933467404056   |0.47566176470588234   |
|Completeness   |1.0   |0.22261904761904763   |   |0.18269230769230768   |0.09758809523809524   |