import csv
import sys
import re

FLAG = ""

p_semester = re.compile("(Fall|Winter|Spring|Summer)\s+\d+")
p_syllabus = re.compile("syllabus", re.IGNORECASE)
p_days_of_the_week = re.compile("(Monday|Mon\.|Tuesday|Tues\.|Wednesday|Wed\.|Thursday|Thurs\.|Friday|Fri\.|Saturday|Sat\.|Sunday|Sun\.)", re.IGNORECASE)
p_lecturer = re.compile("Lecture|Lecturer|Instructor", re.IGNORECASE)
p_requisite = re.compile("requisite", re.IGNORECASE)
p_office_hours = re.compile("Office Hours", re.IGNORECASE)
p_objectives = re.compile("outcome|goal|objective|description|student will", re.IGNORECASE)
p_text = re.compile("required textbook|required text|textbook|text|reading|material|bibliography", re.IGNORECASE)
p_homework = re.compile("assignment |assignments |mid-term|midterm|final exam|exam |exams |grade |grades|grading", re.IGNORECASE)
p_policy = re.compile("cheating|honesty|plagiar|integrity", re.IGNORECASE)
p_tallis = re.compile("Talis")
p_mit = re.compile("MIT OpenCourseWare")
patterns = [ (p_semester, "semester"), (p_syllabus,"syllabus"), (p_days_of_the_week,"weekdays"), (p_lecturer, "lecturer"),
             (p_requisite, "prequisite"), ( p_office_hours, "officeHours"), (p_objectives,"objectives"),
             (p_text,"textbook"), (p_homework,"classWork"), (p_policy,"policy"), (p_tallis, "talis"), (p_mit,"MIT")]

labels = ["fileName", "isSyllabus", "lineCount"] + [label for _, label in patterns]

def get_text(file_name):
    with open(file_name) as fp:
        text = [line for line in fp]
    return text

def get_line_length(text):
    return len(text)

def get_average_length(text):
    count = 0.0
    average = 0.0
    for line in text:
        average = average + len(line)
        count += 1
    if count:
        average = average / count
    return average

def mentions(text, pattern):
    result = None
    line_count = 0
    for line in text:
        m = pattern.search(line)
        if m:
            result = (line_count, m.group(0))
            break
        line_count += 1
    return result

def show_lines(text, line_number):
    for i in range(line_number - 1, line_number + 1):
        print(text[i])

def get_syllabus_status(file_name):
    new_file_name = file_name.replace("../documents/","")
    is_syllabus = syllabus_table[new_file_name]
    return is_syllabus

def get_representation(answer):
    result = None
    if FLAG == "naive":
        if answer:
            result = "y"
        else:
            result = "n"
    else:
        result = answer
    return result

def analyze(file_name, text):
    results = [file_name]
    isSyllabus = get_syllabus_status(file_name)
    line_count = get_line_length(text)
    average_line_length = get_average_length(text)
    results.append(get_representation(int(isSyllabus)))
    results.append(line_count)
    for pattern, name in patterns:
        if mentions(text, pattern):
            answer = 1
        else:
            answer = 0
        results.append(get_representation(answer))
    return results

def write_file(file_name, rows):
    with open(file_name,'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(labels)
        for row in rows:
            writer.writerow(row)


def main():
    #if len(sys.args) < 3:
    #    print("usage: python generate_csv file_name flag")
    results = []
    for s in samples:
        file_name = "../documents/" + str(s) + ".txt"
        text = get_text(file_name)
        rows = analyze(file_name, text)
        results.append(rows)
    write_file("syllabus.csv", results)

if __name__ == "__main__":
    main()

