# Artworks images classification using neural networks

Modern museum specialists successfully work in the digital cultural space: today, laboratories for digitizing funds are being created everywhere in museums.

Here is just a small list of institutions and platforms that allow you to study and download your funds in high quality for personal or commercial use:

- **Solomon Guggenheim Museum**. The digitized collection consists of about 1,700 works — slightly less than a quarter of the museum's collection.
- **London National Gallery**. More than 2,300 works have been digitized and are publicly available on the museum's website.
- **Metropolitan Museum of Art**. The digital collection of the fourth most visited museum in the world contains about 430 thousand works.
- The **Prado Museum** has posted more than 2,700 exhibits on its website.
- **Getty Center**. More than 100 thousand exhibits of the Los Angeles Museum have become public domain.
- **Google Arts & Culture**. A cultural platform with which more than a thousand museums around the world have shared digitized exhibits.
- **Artsy**. The project contains works from leading galleries, museums and foundations, in addition, objects from art fairs and auctions are placed on the site.

Digital resources provide many advantages, such as the creation of an insurance fund and high-quality copies to assist in the restoration of exhibits, the publication of reprints, the organization of projects. The issue of evaluation and attribution of works of art is also relevant.

In turn, the innovative capabilities of Data Science, namely the rapid development of neural networks, even allow you to create works of art without an artist, thus affecting the issues of art theory.

The **Thread Genius** program, acquired by the world's largest auction house Sotheby's, expands the possibilities of visual search, including the detection of works of art based on their visual similarity.

The **Artnome** team is trying to make a revolution in the field of artistic analytics. Its mission is to use technology and data to improve the world history of art and attract attention to artists working at the intersection of art and technology.

The **Art Recognition** AI System evaluates the authenticity of a work of art by comparing the submitted photograph with a set of photographs of the original paintings of the attributed artist, thereby increasing the transparency and integrity of the art market.

**Artsy** is developing The Art Genome Project, a classification system that displays the characteristics that link artists, works of art, architecture and design objects throughout history. The project has more than 1000 characteristics, including historical art trends, themes and formal qualities.

***In this project, based on the Artsy database, we will develop a neural network that solves the problem of classifying artworks images and identify problems of such attribution.***

The target will be the technique (medium) of fine art.

**Stages**
1. Data collection and cleaning 
2. Study of images visual features
3. Model development 
4. Model testing and results analysis

**Libraries**
- Pasing: requests, json, pprint, time
- Tabular data: pandas, numpy, re, collections, nltk
- Images: PIL (Image), cv2, os (reading files)
- Models: tensorflow, including efficientnet for transfer learning, sklearn

## Data collection and cleaning
**Artsy.net database**
- 16,901 images of artworks in high quality
- 5 techniques of fine art:
  - painting
  - engraving
  - drawing
  - gouache and watercolor
  - photography

- It was decided to take the database from the website Artsy - one of the leading platforms for the study, sale and purchase of artworks - using a public API (application programming interface).
- API resources are linked databases (json files), such as: works of art, artists, exhibitions, fairs, partners, “genes”, images, etc. First, the structure of json files was studied. Since there were cases of non-standard structure within one database, parsing of parameters occurred in parts.
- It was decided to limit ourselves to works having 2 dimensions; exclude architecture, sculpture, objects, etc.; leave paintings, drawings, photographs, etc.
- Initially, “genes” were chosen as the target - characteristics, including historical art trends, themes and formal qualities. But it turned out that “genes” were defined only for half of the selected database of works. It would be incorrect to fill in the gaps in 50% of the target yourself. Therefore, the medium technique was chosen as the target: painting, drawing, engraving, gouache and watercolor, photography.

## Study of images visual features
- The data on the size of the images showed that mostly the images we have are quite heavy: the average size is ~ 3000x2000 pixels. Models will not be able to work with such a volume of information. 
- But since we are going to define techniques, details are very important to us, and images collected in such quality allow us to see in detail brush strokes, a fuzzy pencil line and, conversely, a very clear one - a dry needle.
- There is also a (not always unambiguous) pattern in the composition of works performed in different techniques. Drawings, for example, are characterized by a small number of objects and a lot of empty space around it. For paintings - the presence of a large number of colors, and they tend to the dark part of the spectrum because of the density of the paint.
- All this led to the idea of creating a combination of 2 models processing different levels of the images feature space.

## Model development
Our model will consist of 2 parts:
1. Images compressed to 320x320 will be fed into a custom convolution model or one of the pre-trained models (EfficientNetB6). This model is needed to determine the composition of the work: the location of color spots, including painted and unpainted parts.
2. The original images separated into 320x320 pieces will be fed into a not so deep convolution model to read the lowest-level information (line clarity, color contrast). For validation and test sampling, a 320x320 piece will be cut from the middle of the original image.

- Custom models was decided to make quite simple, not deep. The main goal is to check the correctness of the chosen approach.
- For convolutional layers of the first model a filter sized 10x10 was chosen since there is no need to collect the lowest-level information. 3 Convolution2D blocks with the relu neurons activating function and MaxPooling2D layers, alternating with BatchNormalization and Dropout. The head is made of Flatten and 2 Dense layers with Dropout. The last Dense layer defining 5 classes has a softmax activation function.
- For the second model an attempt of data augmentation was made: the original images were split into 320x320 pieces (TensorArray (), .stack(), .fill()). Unfortunately, the augmentation could not be implemented into the model: the loss and accuracy indicators on the training and validation samples from epoch to epoch showed unchanged results.
- For the convolutional layers of the second model a filter sized 5x5 and an even less deep architecture were chosen, since we do not need a general vision of a piece of the image - only lower-level information. 2 blocks of Convolution2D layers with relu activation function, alternating with BatchNormalization, and 1 MaxPooling2D layer with Dropout between them. The head is the same as the first model. The last Dense layer defining 5 classes has a softmax activation function.

## Model testing and results analysis
### 1st model: definition of the artwork composition. 
Gradual training of the model (the speed was changed from 0.005 to 0.001) is a good sign. The best result was achieved by the 7th epoch (73.28%). After that, the jumps in indicators began. Our dataset has a rather unbalanсed distribution by class. This circumstance makes learning difficult. 

The model could not identify at all photography and gouache with watercolors as a classes. The rest is determined pretty well. The model is confusing:
- Drawings with Engravings: they are mostly black and white, the decisive moment is the clarity of the lines, but this model is designed to read color spots. However, engravings are most often completely filled with lines, and there are a lot of voids in the drawings, which prevents correct classification. 
- Photos with drawings and engravings - the same problem. However, the photograph in most cases was identified as a painting. Compositionally, photographs really look like paintings. But it is strange that the model did not take into account the lack of color. Although there are examples of colorized photos.
- Drawings and engravings with paintings: book illustrations, drawings on colored paper, bright posters, as well as painted and very tightly shaded engravings.
- Gouache and watercolor with drawings and engravings: compositionally and in terms of color spots, it is similar to painted drawings and engravings.

### 2nd model: lower-level information reading (line clarity, color contrast). 
The training is more abrupt. The best result was achieved by the 9th epoch (68.70%). It makes sense to reduce the learning rate.

The shape of the curve is also affected by the approach to creating a dataset - a crop from the middle of the original image is extremely heterogeneous information. Augmentation was assumed for the model. Now only the crop from the middle was used for training. This definitely impairs the predictive capabilities of the model.

The model could not identify at all gouache with watercolors as a class. Unlike the previous one, it was able to identify a small number of photos. But engravings and paintings it defines worse.
- Engravings are often defined as drawings, although this model had to take into account the clarity of the lines. The quality of the paper and the density of the shading of the engravings prevent the model from correctly determining their class.
- Photographs even on the lower-level features are similar to the drawing - black and white with blurred contours.
- Gouache and watercolor are often painted drawings. Gouache is a fairly dense paint, this creates a great risk of defining it as a painting.
- Pieces of paintings in which black, gray and beige shades predominate are defined as drawings.

### 3rd model
**EfficientNetB6** is one of the most efficient models that achieves the highest accuracy in image classification tasks by transfer learning. The best result was achieved by the 9th epoch (87.84%). The training took place in 3 stages:
- Just the heads. The training started from the very first stage. Although the lines were located far from each other, they began to converge.
- Defrosting of half of the weights: the distance between the lines has been significantly reduced.
- Defrosting 100% of the weights improved the result, but there was a risk of retraining.

EfficientNetB6 did a good job even with photographs and gouaches with watercolor. But its error tree turned out to be more branched. The model confuses all classes with all, though less often than the previous two custom ones. Examples:
- Drawings in gouache and watercolors: I would define some copies myself as gouache - a question of the quality of the dataset.
- Paintings in gouache and watercolors or in photographs. It is difficult to understand the logic of the model.

## Conclusions
The task that the human eye solves with ease and in seconds turned out to be quite difficult for the machine. To improve the quality of classification in the future, it is necessary:
1. On the one hand, we can also try to train EfficientNetB6 on pieces of original images; enrich datasets with augmentation (it was made, but not implemented into the model for technical reasons); increase the size of images to 528x528 (224x224 was used); reduce the dimension; adjust the learning rate schedule; add a penalty (due to unbalanced sampling); add blanding.
2. On the other hand, we can generalize the data itself - enter new parameters. For example, using detection and segmentation to determine the location and number of different objects in the image. Drawings, for example, are characterized by a small number of objects and a lot of empty space around it.






