import pandas

score_path = "./data/puzzlehunt/score.csv"
answers_path = "./data/puzzlehunt/answers.csv"

def puzzle_check(ID):
    scoreDF = pandas.read_csv(score_path, index_col=0)
    answersDF = pandas.read_csv(answers_path)
    if ID not in scoreDF.index:
        templateID = [0]
        for x in range(len(answersDF)):
            templateID.append(False)
        scoreDF.loc[ID] = templateID
        scoreDF.to_csv(score_path)
    puzzleNo = answersDF.iloc[scoreDF.loc[ID, 'Score'], 0]  # unlocks only 1 puzzle need change in future
    puzzleName = answersDF.iloc[scoreDF.loc[ID, 'Score'], 1]
    puzzleLink = answersDF.iloc[scoreDF.loc[ID, 'Score'], 2]
    return [puzzleNo, puzzleName, puzzleLink]


def puzzle_guess(ID, answerStr):
    answersDF = pandas.read_csv(answers_path)
    answerStr = answerStr.split(",")
    answerDF = answersDF[answersDF['PuzzleID'] == int(answerStr[0])]
    guess = answerStr[1].replace(" ","").lower()
    if guess == answerDF.iloc[0, 3]:
        scoreDF = pandas.read_csv(score_path, index_col=0)
        if ID not in scoreDF.index:
            templateID = [0]
            for x in range(len(answersDF)):
                templateID.append(False)
            scoreDF.loc[ID] = templateID
        if not scoreDF.loc[ID, answerStr[0]]:
            scoreDF.loc[ID, 'Score'] = int(scoreDF.loc[ID, 'Score']) + 1
            scoreDF.loc[ID, answerStr[0]] = True
            scoreDF.to_csv(score_path)
            puzzleNo = answersDF.iloc[scoreDF.loc[ID, 'Score'], 0]  # unlocks only 1 puzzle need change in future
            puzzleName = answersDF.iloc[scoreDF.loc[ID, 'Score'], 1]
            puzzleLink = answersDF.iloc[scoreDF.loc[ID, 'Score'], 2]
            return f"✅ Correct! The answer is **{guess.upper()}**!\nUnlocked {puzzleNo}. **{puzzleName}**: {puzzleLink}"
        else:
            return "You have already solved this puzzle"
    return f"❌ Incorrect! Your guess of **{guess.upper()}** is wrong!"


def solve_check(ID):
    scoreDF = pandas.read_csv(score_path, index_col=0)
    answersDF = pandas.read_csv(answers_path)
    score = int(scoreDF.loc[ID, 'Score'])
    solvedArray = []
    for x in range(score):
        puzzleNo = answersDF.iloc[x,0]
        puzzleName = answersDF.iloc[x,1]
        puzzleLink = answersDF.iloc[x,2]
        solvedArray.append(f'{puzzleNo},{puzzleName},{puzzleLink}')
    return solvedArray
