# NLP-Class-Project
Improved System for the Complex Word Identification Task for George Chrysostomou

The following repository containes the improved system code, along with the rest of 
the files it required to execute. To obtain the results please run the following 
command in the directory of the run.py file:

python run.py 

Results are displayed in under 10 seconds. 

To reproduce results from the development set, as they appear on Table 1 of the report
please change imports in run.py and adjust accordingly for each model. For example to run
the development set for Extremely Randomised Trees:

## Example

### changes in the run.py file :

In Line 3\\
from utils.baseline import Baseline \\ -> to -> \\ 
from utils.Development.baseline_extra import Baseline

to load the development set for the ExtraTreesClassifier

In Line 12\\
Baseline(language) \\-> to -> \\ 
Baseline(language, data.trainset)

to load properly the data

### changes in the dataset.py file :

In Line 10\\
devset_path = "datasets/{}/{}_Test.tsv".format(language, language.capitalize()) \\ -> to ->\\
devset_path = "datasets/{}/{}_Dev.tsv".format(language, language.capitalize()) 

to change to the development set.


