'''
Project Team Members:
1. Jagan Mohan Reddy Dwarampudi (UFID: 9357-2863)
2. Mohammad Shameer Mulla (UFID: 7066-4007)
'''

# Imports
import csv
import os
import random
import recognizer
from icecream import ic
import xml.etree.ElementTree as ET

# Global variables
Path = 'Part 4 (Update)/xml_logs'
Results_Path = 'Part 4 (Update)/HCIRA-Proj1-logfile.csv'
Gestures = ['delete_mark', 'right_sq_bracket', 'triangle', 'right_curly_brace', 'star', 'x', 'pigtail', 'left_sq_bracket', 'circle', 'caret', 'question_mark', 'v', 'check', 'rectangle', 'left_curly_brace', 'arrow']

# Function to get the points from the XML file
getPointsFromRoot = lambda gesture : [[int(point.attrib['X']), int(point.attrib['Y'])] for point in gesture]

# Global variables
Dataset = {}
Results = {}


# Main function to run all the functions
def main():
    global Dataset, Path, Gestures, Results_Path

    ic('Reading dataset')
    Dataset = readDataset(Path, Gestures)
    ic('Dataset read')

    ic('Preprocessing dataset')
    Dataset = preprocessDataset(Dataset)
    ic('Dataset preprocessed')

    ic('Testing')
    results_fields, results_rows = testing(Dataset)
    ic('Testing done')

    ic('Writing results')
    outputResults(results_fields, results_rows, Results_Path)
    ic('Results written')
    

# Function to read all the XML files and store them in a dictionary
def readDataset(path, gestures):
    global getPointsFromRoot

    dataset = {}

    # Looping through all the users, speeds, gestures and examples
    for U in range(2, 12):
        for speed in ['slow', 'medium', 'fast']:
            for gesture in gestures:
                for E in range(1, 11):
                    key = f'{U:02d}-{speed}-{gesture}-{E:02d}'

                    # Reading the XML file
                    filepath = os.path.join(path, f's{U:02d}', speed, f'{gesture}{E:02d}.xml')
                    root = ET.parse(filepath).getroot()
                    value = getPointsFromRoot(root)

                    # Adding the points to the dictionary
                    dataset[key] = value

    return dataset


# Function to preprocess all the unistrokes in the dataset
def preprocessDataset(dataset):
    return {key: recognizer.preprocess(value) for key, value in dataset.items()}


# Function that implements the testing psuedocode from the assignment
def testing(dataset):
    # users = list(range(2, 12))
    # speeds = ['slow', 'medium', 'fast']
    # examples = list(range(1, 10))
    # iterations = 100

    # Testing parameters
    users = list(range(2, 12))
    speeds = ['medium']
    examples = list(range(1, 10))
    iterations = 10

    # Results XML file fields and rows
    result_fields = [f'Recognition Log: Jagan Mohan Reddy Dwarampudi // $1 Recognizer-Golden Section Search // Unistroke gesture logs: XML // USER-DEPENDENT RANDOM-{iterations}']
    
    result_rows = [[
        'User[all-users]',
        'GestureType[all-gestures-types]',
        f'RandomIteration[1to{iterations}]',
        '#ofTrainingExamples[E]',
        'TotalSizeOfTrainingSet[count]',
        'TrainingSetContents[specific-gesture-instances]',
        'Candidate[specific-instance]',
        'RecoResultGestureType[what-was-recognized]',
        'CorrectIncorrect[1or0]',
        'RecoResultScore',
        'RecoResultBestMatch[specific-instance]',
        'RecoResultNBestSorted[instance-and-score]'
    ]]

    # Variable to store the accuracy results
    accuracy_results = {}

    # Looping through all the users, speeds, examples, iterations and gestures
    for U in users:
        for speed in speeds:
            for E in examples:
                accuracy_keys = []

                for iteration in range(iterations):
                    train_dataset = {}
                    test_dataset = {}

                    for gesture in Gestures:
                        # Getting the training and testing examples randomly
                        gesture_examples = list(range(1, 11))
                        train_examples = random.sample(gesture_examples, E)
                        test_example = random.choice(list(set(gesture_examples) - set(train_examples)))

                        # Initializing the training and testing dataset keys
                        train_examples_keys = [f'{U:02d}-{speed}-{gesture}-{example:02d}' for example in train_examples]
                        test_example_key = f'{U:02d}-{speed}-{gesture}-{test_example:02d}'

                        # Adding the training and testing examples to the dataset
                        train_dataset.update({key: value for key, value in dataset.items() if key in train_examples_keys})
                        test_dataset[test_example_key] = dataset[test_example_key]

                    # Looping through all the testing examples and getting the NBest results
                    for test_gesture_key, test_gesture_value in test_dataset.items():
                        # Getting the NBest results and sorting them in descending order
                        nBest = recognizer.recognize(test_gesture_value, train_dataset, returnNBest=True, preProcessUnistrokes=False)
                        sortedNBest = sorted(nBest.items(), key=lambda x: x[1], reverse=True)
                        top50NBest = sortedNBest[:50]

                        # Checking if the gesture was recognized correctly
                        recognition_flag = 1

                        if test_gesture_key.split('-')[2] != sortedNBest[0][0].split('-')[2]:
                            recognition_flag = 0

                        # Results XML file row to be appended
                        result_row = [
                            f's{U:02d}',
                            test_gesture_key.split('-')[2],
                            iteration + 1,
                            E,
                            len(train_dataset),
                            list(train_dataset.keys()),
                            test_gesture_key,
                            sortedNBest[0][0].split('-')[2],
                            recognition_flag,
                            sortedNBest[0][1],
                            sortedNBest[0][0],
                            top50NBest
                        ]

                        result_rows.append(result_row)

                        # Adding the accuracy results using the recognition flag
                        accuracy_key = f'User(s{U:02d}) - Speed({speed}) - Gesture({test_gesture_key.split("-")[2]}) - No. of training examples({E})'
                        accuracy_keys.append(accuracy_key)

                        try:
                            accuracy_results[accuracy_key] += recognition_flag
                        except KeyError:
                            accuracy_results[accuracy_key] = recognition_flag

                ic(f'Examples {E} done')

        ic(f'User s{U:02d} done')
        print()

    # Adding the average accuracy results to the results XML file
    result_rows.append([''])
    result_rows.append([''])
    result_rows.append([f'Average accuracy - {iterations} iterations'])

    # Calculating the average accuracy and adding it to the results XML file
    for accuracy_key, accuracy_value in accuracy_results.items():
        result_rows.append([accuracy_key, accuracy_value / iterations])

    ic(sum([accuracy_value / iterations for accuracy_value in accuracy_results.values()]) / len(accuracy_results.values()))

    return result_fields, result_rows


# Function to write the results to a CSV file
def outputResults(result_fields, result_rows, results_path):
    with open(results_path, 'w') as f:
        write = csv.writer(f)
        write.writerow(result_fields)
        write.writerows(result_rows)