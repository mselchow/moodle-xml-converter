# Moodle XML constants organized in one place
# Easier adjustment of code and declutters main file

# Quiz constants

XML_QUIZ_BEGINNING = """<?xml version="1.0" encoding="UTF-8"?>
  <quiz>
  <question type="category">
    <category>
        <text>none</text>
    </category>
  </question>

"""

XML_QUIZ_END = "  </quiz>"



# Question constants

XML_QUESTION_BEGINNING = """    <question type="multichoice">
"""

XML_QUESTION_END = """    </question>

"""


# Given a question name, stem, and 2D list of answers/percentages,
# this function will return fully formatted XML for a single question
def getQuestionXML(name, stem, answers):
    # Add initial question XML
    tmp = XML_QUESTION_BEGINNING

    # Add question name XML
    tmp += """    <name>
      <text>""" + name + """</text>
    </name>

"""

    # Add question stem XML
    tmp += """    <questiontext format="moodle_auto_format">
      <text><![CDATA[""" + stem + """]]></text>
    </questiontext>
    <answernumbering>ABCD</answernumbering>
    <shuffleanswers>true</shuffleanswers>

"""

    # Add answer XML from 2D list of answers/pcts
    for x in range(len(answers)):
        tmp += '''    <answer fraction="''' + answers[x][1] +  '''" format="moodle_auto_format">
      <text><![CDATA[''' + answers[x][0] + ''']]></text>
      <feedback format="moodle_auto_format">
        <text></text>
      </feedback>
    </answer>

'''

    # Add question end XML
    tmp += XML_QUESTION_END

    # Return final XML
    return tmp
