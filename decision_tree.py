import pandas as pd
SURVEYDATA = '571 Course Feedback Analysis.csv'
GAINDATA = 'InformationGains.csv'
INPUT = 'Input.csv'


df1 = pd.read_csv(SURVEYDATA)
df2 = pd.read_csv(GAINDATA)
df3 = pd.read_csv(INPUT)


responses = []          # final responses from the decision tree 
activeBranches = []     # these are the branches of decision tree that the algorithm is actively pruning
firstPass = 0

featuresCol = df2.loc[:, 'gain']

for feature in featuresCol:
    featureValues = df1.loc[:, feature]     # list of value of the feature from the survey data
    desiredValue = df3.loc[:, feature][0]   # the value of the feature that we want
    
    responseChanged = 0                     # flag to check if all the responses are either all yeses or all nos
    _responses = []                         # list of responses based on the current feature values
    row = 0                                 # number of the current row/branch being checked
    
    for value in featureValues:
        if value == desiredValue:

            # first pass selects all the possible branches,
            # some of these branches are later discarded as the algorithm progresses
            if firstPass == 0:
                activeBranches.append(row)

            if row in activeBranches:
                if responseChanged == 0:

                    # set the flage if the new response is different from the previous response
                    if _responses and df1.iloc[row,47] != _responses[-1]:
                        responseChanged = 1                       
                    
                    # add the new response to the list
                    _responses.append(df1.iloc[row,47])
                        
                        
        # As the algorithm prunes deeper the unneeded branches are removed 
        elif value != desiredValue and row in activeBranches:
            activeBranches.remove(row)

        row += 1
    
    if firstPass == 0:
        firstPass = 1

    responses = _responses

    # if we have all yes or all no responses then end the algorithm and output the decision
    if responseChanged == 0:
        print("\nWould you recommend taking this course to another student?: " + _responses[-1] + "\n")
        break
        
yesCount = responses.count('yes')
noCount = responses.count('no')
total = yesCount + noCount

# In the that the decision tree does not have a decisive answer
# Yes and No is presented as percantages
if yesCount != 0 and noCount != 0:
    print("\nNo decisive answer based on your input:")
    print("Total yeses: " + str(yesCount/total*100) + "%")
    print("Total nos: " + str(noCount/total*100) + "%\n")
