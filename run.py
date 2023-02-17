import openpyxl
import os

all_data = {
    # Left Leg
    'left_position_hip': open('static/left_position_hip.txt', 'r'),
    'left_position_knee': open('static/left_position_knee.txt', 'r'),
    'left_position_ankle': open('static/left_position_ankle.txt', 'r'),
    'left_angle': open('static/left_angle.txt', 'r'),
    'left_velocity': open('static/left_velocity.txt', 'r'),

    # Right Leg
    'right_position_hip': open('static/right_position_hip.txt', 'r'),
    'right_position_knee': open('static/right_position_knee.txt', 'r'),
    'right_position_ankle': open('static/right_position_ankle.txt', 'r'),
    'right_angle': open('static/right_angle.txt', 'r'),
    'right_velocity': open('static/right_velocity.txt', 'r'),
}

files = ['static/Left Leg.xlsx', 'static/Right Leg.xlsx']


def start(fl):
    workbook = openpyxl.load_workbook(fl)  # create file
    worksheets = workbook.sheetnames
    for sheet in worksheets:
        if sheet == 'Final Data':
            continue
        init(sheet, workbook, fl)


def init(data, workbook, file_name):
    worksheet = workbook[data]  # create worksheet
    open_file = all_data[data]
    linelist = open_file.readlines()  # read each line
    count = len(linelist)  # count lines

    for num in range(0, count):  # create each line and print in excel
        line = linelist[num]  # load each line in variable
        rows = line.split(",")  # split lines
        rows = [float(rows[0]), float(rows[1])]  # split lines
        worksheet.append(rows)  # write each line in excel

    workbook.save(file_name)
    workbook.close()


if __name__ == '__main__':
    os.system('python clear.py')
    print("Files cleared")
    print("Starting Pose Detection Module")
    os.system('python PoseDetectionModule.py')

    print("Loading Data...")
    for file in files:
        start(file)

    print("Data Loaded")

    print("Opening Excel Files...")
    os.system('start excel.exe "static/Left Leg.xlsx"')
    os.system('start excel.exe "static/Right Leg.xlsx"')
    print("Excel Files Opened")
