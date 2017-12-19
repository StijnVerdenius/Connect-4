# Connect-4

## Fundamentals of Fuzzy Logic Connect-4 AI

### Stijn Verdenius University of Amsterdam

#### Instructions

- In reading material -> own you find the paper and presentation

- In code, run python 4opeenrij.py to run the program

- If you want to regenerate data/relearn rules etc, go to -> code -> players -> fuzzyAgent
	- Change the boolean values in the constructor of fuzzytoolbox
	- For manual adjustments change the fis files for the agents

#### Technical details:

##### python2.7 (!!)

Recuired packages:

numpy

sklearn

skfuzzy

scipy

#### Structure

The setup is made around 4opeenrij.py, which holds the interface and game mechanics and the boarddef.py which holds the board information and basic board operation methods.

The setup is made as general as possible, so that more players (or sub components of players such as the bruteforce judge in the fuzzyagent) could be added later.

- fuzzy

In the fuzzyplayer.py are the game mechanics who do the descsion making, yet they use a fuzzy system (which is the fuzzy controller). The fuzzy toolbox is used as the sub class of the fuzzy system and holds a few other classes: the dataset creator, the fuzzy rule maker and the fuzzybasics. Furthermore, it uses the two fis files to save the designed sytems to, so that multiple systems can live next to each other (again, as general as possible for possible later expansion).