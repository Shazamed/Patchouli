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
    scoreDF = pandas.read_csv(score_path, index_col=0)
    guess = answerStr[1].replace(" ","").lower()
    puzzleGuessNO = answerStr[0]
    if int(puzzleGuessNO) != scoreDF.loc[ID, 'Score'] + 1:
        return "❌ You have not unlocked this puzzle"
    if guess == answerDF.iloc[0, 3]:
        if ID not in scoreDF.index:
            templateID = [0]
            for x in range(len(answersDF)):
                templateID.append(False)
            scoreDF.loc[ID] = templateID
        if not scoreDF.loc[ID, puzzleGuessNO]:
            scoreDF.loc[ID, 'Score'] = int(scoreDF.loc[ID, 'Score']) + 1
            scoreDF.loc[ID, puzzleGuessNO] = True
            scoreDF.to_csv(score_path)
            if scoreDF.loc[ID, 'Score'] == 5:
                return f"✅ Correct! The answer is **{guess.upper()}**!\nUnlocked FINAL: <https://docs.google.com/document/d/1plB6Ubw4umQDtGVwz-xwdmlHw_sylT8W5BFAv42PtqE/edit#>"
            puzzleNo = answersDF.iloc[scoreDF.loc[ID, 'Score'], 0]  # unlocks only 1 puzzle need change in future
            puzzleName = answersDF.iloc[scoreDF.loc[ID, 'Score'], 1]
            puzzleLink = answersDF.iloc[scoreDF.loc[ID, 'Score'], 2]
            return f"✅ Correct! The answer is **{guess.upper()}**!\nUnlocked {puzzleNo}. **{puzzleName}**: <{puzzleLink}>"
        else:
            return "You have already solved this puzzle"
    return f"❌ Incorrect! Your guess of **{guess.upper()}** is wrong!"


def solve_check(ID):
    scoreDF = pandas.read_csv(score_path, index_col=0)
    answersDF = pandas.read_csv(answers_path)
    if ID not in scoreDF.index:
        templateID = [0]
        for x in range(len(answersDF)):
            templateID.append(False)
        scoreDF.loc[ID] = templateID
        scoreDF.to_csv(score_path)

    score = int(scoreDF.loc[ID, 'Score'])
    solvedArray = []

    for x in range(score):
        puzzleNo = answersDF.iloc[x,0]
        puzzleName = answersDF.iloc[x,1]
        puzzleLink = answersDF.iloc[x,2]
        solvedArray.append(f'{puzzleNo},{puzzleName},{puzzleLink}')
    return solvedArray
