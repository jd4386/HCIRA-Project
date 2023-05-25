'''
Project Team Members:
1. Jagan Mohan Reddy Dwarampudi (UFID: 9357-2863)
2. Mohammad Shameer Mulla (UFID: 7066-4007)
'''

# Imports
import csv
import os
import random
import ndollarrecognizer
from icecream import ic
import xml.etree.ElementTree as ET

# Global variables
Path = 'Project 2/mmg'
Results_Path = 'Project 2/HCIRA-Proj2-logfile-temp.csv'
Gestures = [
    'T',
    'line',
    'arrowhead',
    'P',
    'asterisk',
    'pitchfork',
    'six_point_star',
    'null',
    'I',
    'H',
    'five_point_star',
    # 'exclamation_point',
    'X',
    'D',
    'half_note',
    'N'
]

# Gestures = [
#     'circle',
#     'question_mark',
#     'left_curly_brace',
#     'check',
#     'x',
#     'triangle',
#     'right_sq_bracket',
#     'delete_mark',
#     'rectangle',
#     'arrow',
#     'right_curly_brace',
#     'star',
#     'caret',
#     'left_sq_bracket',
#     'pigtail',
#     'v'
# ]

Users = [i for i in os.listdir(Path) if i != '.DS_Store' and 'stylus' in i and 'MEDIUM' in i]

# Function to get the points from the XML file
getPointsFromRoot = lambda gesture : [[ndollarrecognizer.Point(int(point.attrib['X']), int(point.attrib['Y']) )for point in stroke] for stroke in gesture]
getPointsFromRootCustom = lambda gesture : [[[int(point.attrib['X']), int(point.attrib['Y'])] for point in stroke] for stroke in gesture]

# Global variables
Dataset = {}
DatasetCustom = {}
Results = {}


# Main function to run all the functions
def main():
    global Dataset, Path, Gestures, Results_Path, Users, DatasetCustom

    ic('Reading dataset')
    Dataset, DatasetCustom = readDataset(Path, Gestures, Users)
    ic('Dataset read')

    # ic('Preprocessing dataset')
    # Dataset = preprocessDataset(Dataset)
    # ic('Dataset preprocessed')

    ic('Testing')
    results_fields, results_rows = testing(Dataset, Users)
    ic('Testing done')

    ic('Writing results')
    outputResults(results_fields, results_rows, Results_Path)
    ic('Results written')
    

# Function to read all the XML files and store them in a dictionary
def readDataset(path, gestures, users):
    global getPointsFromRoot

    dataset = {}
    datasetCustom = {}

   # Looping through all the users, speeds, gestures and examples
    for U in users:
        for gesture in gestures:
            for E in range(1, 11):
                key = f'{U}-{gesture}-{E:02d}'
                # print(key)

                # Reading the XML file
                filepath = os.path.join(path, U, f'{U}-{gesture}-{E:02d}.xml')
                root = ET.parse(filepath).getroot()
                value = getPointsFromRoot(root)

                # Adding the points to the dictionary
                dataset[key] = ndollarrecognizer.Multistroke(key, False, value)

                value = getPointsFromRootCustom(root)
                datasetCustom[key] = value


    return dataset, datasetCustom


# Function to preprocess all the unistrokes in the dataset
# def preprocessDataset(dataset):
#     return {key: recognizer.preprocess(value) for key, value in dataset.items()}


# Function that implements the testing psuedocode from the assignment
def testing(dataset, users):
    # users = list(range(2, 12))
    # speeds = ['slow', 'medium', 'fast']
    # examples = list(range(1, 10))
    # iterations = 100

    # Testing parameters
    # users = list(range(1, 7))
    examples = list(range(1, 10))
    iterations = 1

    # Results XML file fields and rows
    result_fields = [f'Recognition Log: Jagan Mohan Reddy Dwarampudi // $N Recognizer-Golden Section Search // Multistroke gesture logs: XML // USER-DEPENDENT RANDOM-{iterations}']
    
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
    for U in users[:1]:
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
                    train_examples_keys = [f'{U}-{gesture}-{example:02d}' for example in train_examples]
                    test_example_key = f'{U}-{gesture}-{test_example:02d}'

                    # Adding the training and testing examples to the dataset
                    train_dataset.update({key: value for key, value in dataset.items() if key in train_examples_keys})
                    test_dataset[test_example_key] = dataset[test_example_key]

                # Looping through all the testing examples and getting the NBest results
                for test_gesture_key, test_gesture_value in test_dataset.items():
                    # Getting the NBest results and sorting them in descending order
                    # nBest = recognizer.recognize(test_gesture_value, train_dataset, returnNBest=True, preProcessUnistrokes=False)
                    # sortedNBest = sorted(nBest.items(), key=lambda x: x[1], reverse=True)
                    # top50NBest = sortedNBest[:50]

                    strokes = DatasetCustom[test_gesture_key]
                    # ic(test_gesture_key, strokes)
                    result = ndollarrecognizer.recognize(strokes, False, False, list(train_dataset.values()))

                    # Checking if the gesture was recognized correctly
                    recognition_flag = 1
                    nomatch_flag = 0

                    if result.name == 'No match.':
                        nomatch_flag = 1

                    if nomatch_flag or test_gesture_key.split('-')[-2] != result.name.split('-')[-2]:
                        recognition_flag = 0

                    # Results XML file row to be appended
                    result_row = [
                        f'{U}',
                        test_gesture_key.split('-')[-2],
                        iteration + 1,
                        E,
                        len(train_dataset),
                        list(train_dataset.keys()),
                        test_gesture_key,
                        result.name.split('-')[-2] if not nomatch_flag else result.name,
                        recognition_flag,
                        result.score,
                        result.name,
                        [result.name, result.score]
                    ]

                    result_rows.append(result_row)

                    # Adding the accuracy results using the recognition flag
                    accuracy_key = f'User({U}) - Gesture({test_gesture_key.split("-")[-2]}) - No. of training examples({E})'
                    accuracy_keys.append(accuracy_key)

                    try:
                        accuracy_results[accuracy_key] += recognition_flag
                    except KeyError:
                        accuracy_results[accuracy_key] = recognition_flag

                    # ic(f'User {U} - Examples {E} - Iteration {iteration + 1} - Gesture {test_gesture_key.split("-")[-2]} done')

                # ic(f'Iteration {iteration + 1} done')

            ic(f'Examples {E} done')

        ic(f'{U} done')
        print()

    # Adding the average accuracy results to the results XML file
    result_rows.append([''])
    result_rows.append([''])
    result_rows.append([f'Average accuracy - {iterations} iterations'])

    # Calculating the average accuracy and adding it to the results XML file
    for accuracy_key, accuracy_value in accuracy_results.items():
        result_rows.append([accuracy_key, accuracy_value / iterations])

    ic(sum([accuracy_value / iterations for accuracy_value in accuracy_results.values()]) / len(accuracy_results.values()))
    result_rows.append(['Total average accuracy', sum([accuracy_value / iterations for accuracy_value in accuracy_results.values()]) / len(accuracy_results.values())])

    return result_fields, result_rows


# Function to write the results to a CSV file
def outputResults(result_fields, result_rows, results_path):
    with open(results_path, 'w') as f:
        write = csv.writer(f)
        write.writerow(result_fields)
        write.writerows(result_rows)