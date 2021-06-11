# Reading error and disfluency features 

Code to replicate the features from "Automatically Detecting Errors and Disfluencies in Read Speech to Predict Cognitive Impairment in People with Parkinson’s Disease" to appear at Interspeech 2021. 

This code aligns a script and transcript using the Damerau-Levenshtein distance algorithm. It counts the number of inserted, omitted, substituted, and transposed words, and provides an alignment between a script and transcript. 

## Usage example 
```
script = 'the animals crossed and we continued walking'
transcript = 'th the animals crossed and they continued'
results = ErrorsAndDisfluencies(script, transcript)
print('Number of insertions: ', results.num_insertions)
print('Number of deletions: ', results.num_deletions)
print('Number of substitutions: ', results.num_substitutions)
print('Number of transpositions: ', results.num_transpositions) 
print('\n')
print(results.aligned_str) 
```

```
Number of insertions:  1
Number of deletions:  1
Number of substitutions:  1
Number of transpositions:  0

*  the animals crossed and  we  continued walking
I   C     C       C     C   S       C        D   
th the animals crossed and they continued    *  
```

## References
```
A. Romana, J. Bandon, M. Perez, S. Gutierrez, R. Richter, A. Roberts, and E. Mower Provost. 
"Automatically Detecting Errors and Disfluencies in Read Speech to Predict 
Cognitive Impairment in People with Parkinson’s Disease." in INTERSPEECH, 2021. 
```
