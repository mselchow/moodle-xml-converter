# Converts a text document of MC questions to Moodle XML
#
# Notes: for clarification on any regex, plug into regex101.com
#
# December 12, 2019
# Michael Selchow

# For regex and Moodle XML constants, respectively
import re
import moodlexmlconstants
import sys

# Dictionary for complexity text
complexity_dict = {
    "Low": "Easy",
    "Moderate": "Medium",
    "Hard": "Hard",
    "Medium": "Medium",
    "Easy": "Easy",
    "High": "Hard"
}

# From questionText, returns the question name as a string
# Note: this is for single question texts only, not for an array of questions
#       correct functioning should loop through question array and call this
#       function on each loop
def getQuestionName(questionText):
    # Get the standard by regex, get the match group of the standard #, use for q naming
    keyword = re.search("Standard:.*(\d\.\d{1,2})", questionText).group(1).strip()

    complexity = re.search("Complexity Level:(.*)", questionText).group(1).strip()
    complexity = complexity_dict[complexity]

    number = re.search("Question #:(.*)", questionText).group(1).strip()

    return "EN_US-History_" + keyword + "_PT_" + complexity + "_" + number


def getQuestionText(questionText):
    # Matches all text between "Complexity Level: X" and the first answer text, "A."
    # Accounts for removing whitespace/line breaks at the beginning through /\s+/
    # and also removes trailing whitespace/line breaks through second /\s/
    return re.search("Complexity Level:.*\s+([\S\s]+)\sA\.", questionText).group(1).strip()


def getQuestionAnswers(questionText):
    # Pull answer text from input
    answerText = re.search("(A\..*\sB\.[\S\s]+)", questionText).group(1).strip()

    # Create array from input by splitting by new lines
    answerText = answerText.split('\n')

    # Holder lists for output
    answers = []
    pcts = []

    # Loop through list, append lists and percentages
    for x in answerText:
        # Get answer text by finding answer letter, answer text, and, critically
        # by not allowing the asterisk to be in the question text through [^*]
        # but still capturing it -- if it exists -- through \*?
        answers.append(re.search("[A-D]\.\s?(.*[^*])\*?$", x).group(1).strip())
        if x.endswith("*"):
            pcts.append("100")
        else:
            pcts.append("0")

    # Return a 2D list from our two 1D lists
    return list(zip(answers, pcts))


if __name__ == '__main__':
    # Open output file, write initial text
    output = open("output.xml", "w")
    output.write(moodlexmlconstants.XML_QUIZ_BEGINNING)

    # set input file name by CLI, otherwise default to output.txt
    if (sys.argv[1] == ""):
        inputName = "input.txt"
    else:
        inputName = sys.argv[1]

    # Open input file, get text, close file
    inputFile = open(inputName, "r")
    input = inputFile.read()
    inputFile.close()

    # Split text by question delimeter (---)
    questions = input.split("---")

    # Loop through each question
    for x in questions:
        # Remove any whitespace or extra lines
        x = x.strip()

        # Get vars for each part of the question
        questionName = getQuestionName(x)
        questionText = getQuestionText(x)
        questionAnswers = getQuestionAnswers(x)

        # Get question XML and write to output
        xmlCode = moodlexmlconstants.getQuestionXML(questionName, questionText, questionAnswers)
        output.write(xmlCode)

    # Write ending XML to close off file
    output.write(moodlexmlconstants.XML_QUIZ_END)

    # Close our file before finishing :)
    output.close()
