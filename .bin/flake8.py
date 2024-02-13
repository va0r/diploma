import os

if __name__ == "__main__":

    executive_string = 'flake8 ../. --ignore=E501,E731 > ../.flake8_text_report/flake8_report.txt 2>&1'
    os.system(executive_string)
