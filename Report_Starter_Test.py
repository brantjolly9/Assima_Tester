import os
import csv
import datetime
import shutil
import json
import datetime

# Run psexec, install-packages, and npm install from the test suite first
# TODO: prompt user for the suites they want to run then pass that into __init__ to avoid complications


class Report_Runner:
    def __init__(self, server):
        self.server = server
        self.collabSectionHeaders = [
            'Content Administration - Administrator',
            'Community - Administrator',
            'Licence - Administrator',
            'Author',
            'Dashboard - Administrator',
            'End User',
            '7.24 - New Features',
            '7.25 - New Features']
        self.date = str(datetime.datetime.today()).split(" ")[0]
        self.FINAL_REPORT_PATH = f'C:\\AutomatedReports_{self.date}'

        self.TEST_SUITE_PATH = input('Enter Test Suite Path: ')
        os.chdir(self.TEST_SUITE_PATH)
        self.LOG_PATH = os.path.join(self.FINAL_REPORT_PATH, 'Reporter_Log.txt')
        print(f'Changed dir to: {self.TEST_SUITE_PATH}')

        if input('Overwrite today\'s reports? (y/n) ') == 'y':
            # Try to delete old report folder to make way for new folder creation
            try:
                shutil.rmtree(self.FINAL_REPORT_PATH)
                print(f'{self.FINAL_REPORT_PATH} Deleted')
                self.log.open(self.log, 'x')
            except:
                print('No file to delete')
            os.mkdir(self.FINAL_REPORT_PATH)
            self.Create_Folders()
        else:
            self.log = open(self.LOG_PATH, 'w')
    
        self.Scripts_To_Run = {'Collab': [], 'Train': []}

        Batch_Script_Path = f'{self.TEST_SUITE_PATH}\\Collab-BatchScript-{self.server}.ps1'

        # Get all the commands from the Collab BatchScript file and add to Scripts_To_Run
        with open(Batch_Script_Path, 'r') as batchScript:
            for line in batchScript.readlines():
                line = line.strip()
                suite = line.replace(
                    'dotnet test --filter CollabTestSuite', '')
                suite = suite.replace(self.server, '')

                for header in self.collabSectionHeaders:
                    if suite in header.replace(' ', ''):
                        suite = header
                self.Scripts_To_Run.get('Collab').append((suite, line))

        self.Scripts_To_Run.get('Train').append(
            (f'Train', f'dotnet test --filter TrainTestSuite{self.server}'))

        # Impliment a way to pause before running new features
        # self.Scripts_To_Run.get('Collab').append(
        #     ('7.25 - New Features', 'dotnet test --filter CollabTestSuiteNewFeatures725 '))

        # Write the collected ps1 commands to self.log

        self.log.write('============= GET SCRIPTS =============\n')
        json.dump(self.Scripts_To_Run, self.log, indent=1)

    # Install Packages and NPM
    def Install(self):
        if input('Install Packages: ') == 'y':
            package_output = os.popen('.\\Install-packages.ps1').read()
            print(package_output)
        if input('Install NPM: ') =='y':
            npm_output = os.popen('npm install').read()
            print(npm_output)

    def Create_Folders(self):
        # Final_Report_Folder stucture
        self.reportStructure = {
            "725_Reports": {"Assist": "",
                            "Collab": self.collabSectionHeaders,
                            "Train": "",
                            },
            "726_Reports": {"Assist": "",
                            "Collab": self.collabSectionHeaders,
                            "Train": "",
                            }}
            
        os.chdir(self.FINAL_REPORT_PATH)

        self.log = open(self.LOG_PATH, 'a')
        self.log.write('\n============ CREATE FOLDERS ===========\n')

        for server, product in self.reportStructure.items():
            for prodName, item in product.items():
                tempPath = os.path.join(
                    self.FINAL_REPORT_PATH, server, prodName)
                os.makedirs(tempPath)
                self.log.write("Product: {:>5}\t\tPath: {:<8}\n".format(
                    prodName, tempPath))
                if type(item) == list:
                    os.chdir(tempPath)
                    for i in item:
                        os.makedirs(os.path.join(tempPath, i))
                        self.log.write(os.path.join(tempPath, i) + '\n')
        else:
            print('Using old files')

        os.chdir(self.TEST_SUITE_PATH)
        existingDocs = list(os.scandir('GeneratedReports'))
        # print(len(existingDocs))
        # if len(existingDocs) > 0:
        #     for doc in existingDocs:
        #         shutil.move(doc, 'OldReports\\')

    def Change_Credentials(self):
        creditsCSV = open(os.path.join(self.TEST_SUITE_PATH, 'Data', 'credentials.csv'), 'r', newline='')
        credReader = csv.reader(creditsCSV, delimiter=';', quotechar="'")
        next(credReader)
        data = next(credReader)
        email = data[0]
        password = data[1]
        if input(f"Are credentials correct: {email}, {password} (y/n) ") != 'y':
            email = input('Enter email: __________@assima.net ') + '@assima.net'
            password = input('Enter password: ')

        creditsCSV = open(os.path.join(self.TEST_SUITE_PATH,
                                       'Data', 'credentials.csv'), 'w', newline='')
        credWriter = csv.writer(creditsCSV, delimiter=';')
        credWriter.writerow(['username', 'password', ''])
        credWriter.writerow([email, password, ''])
        creditsCSV.close()

        # Write the entered credentials to log

        self.log.write('\n============ CHANGE CREDENTIALS ============\n')
        self.log.write(
            "Email: {:>8}\t\tPassword: {:>8}".format(email, password))

    def Move_Reports(self, report_path, name):
        counter = 0
        for item in os.scandir('GeneratedReports'):
            if item.name.endswith('.html'):
                os.rename(item, os.path.join(
                    report_path, name + '.html'))
            else:
                counter += 1
                shutil.move(item, report_path)
                print(f'Failed: {item.name.split(".")[0]}')
            self.log.write('Copied {:<10} into {:<8}\n'.format(
                item.name, report_path))
        print(f'Failed Tests: {counter}\n')

    def Run_Scripts_Individually(self):
        self.log.write(
            '\n============= RUN SCRIPTS INDIVIDUALY ===============\n')
        self.log.write(f'Test Suite Path: {os.getcwd()}')

        for suite, tests in self.Scripts_To_Run.items():
            self.log.write(f'\n------ {suite} ------\n')
            for test in tests:

                os.chdir(self.TEST_SUITE_PATH)
                if suite == 'Collab':
                    self.log.write(f'\n--------- {test[0]} -------\n')
                    report_path = os.path.join(
                        self.FINAL_REPORT_PATH, self.server + '_Reports', suite, test[0])
                    # C:\\AutomatedReports\72X_Reports\Collab\ContentAdministration    \ContentAdministration_Log.txt
                    logPath = os.path.join(report_path, test[0] + '_Log.txt')

                    self.log.write(f'Report Path: {report_path}\n')
                    self.log.write(f'Log Path: {logPath}\n')
                    if input(f'Run {test[0]}? (y/n) ') == 'y':
                        output = os.popen(test[1]).read()
                        with open(logPath, 'x') as l:
                            l.write(output)

                elif suite == 'Train' and input('Run Train? (y/n) ') == 'y':
                    print(os.getcwd())
                    logPath = f'C:\\AutomatedReports_{self.date}\\{self.server}_Reports\\{suite}\\{test[0]}_Log.txt'
                    report_path = os.path.join(
                        self.FINAL_REPORT_PATH, self.server + '_Reports', suite)
                    self.log.write(f'Log Path: {logPath}\n')
                    output = os.popen(test[1]).read()
                    with open(logPath, 'x') as l:
                        l.write(output)

                # Get all items in Generated reports and move them to the correct report folder
                self.Move_Reports(report_path, test[0])

    def Run_Train(self):
        print(os.getcwd())
        trainSer = f'Train{self.server}'
        trainCmd = self.Scripts_To_Run.get('Train')[0]
        print(trainCmd[1])
        logPath = f'C:\\AutomatedReports_{self.date}\\{self.server}_Reports\\Train\\{trainSer}_Log.txt'
        report_path = os.path.join(
            self.FINAL_REPORT_PATH, self.server + '_Reports', 'Train')
        self.log.write(f'Log Path: {logPath}\n')
        output = os.popen(trainCmd[1]).read()
        with open(logPath, 'x') as l:
            l.write(output)
        self.Move_Reports(report_path, trainSer)

    def Run_All_Scripts(self):

        self.log.write('\n============= RUN ALL SCRIPTS ===============\n')
        self.log.write(f'Test Suite Path: {os.getcwd()}')

        for suite, tests in self.Scripts_To_Run.items():
            self.log.write(f'\n------ {suite} ------\n')
            for test in tests:

                os.chdir(self.TEST_SUITE_PATH)
                if suite == 'Collab':
                    self.log.write(f'\n--------- {test[0]} -------\n')
                    
                    report_path = os.path.join(
                        self.FINAL_REPORT_PATH, self.server + '_Reports', suite, test[0])
                    # C:\\AutomatedReports\72X_Reports\Collab\ContentAdministration    \ContentAdministration_Log.txt
                    logPath = os.path.join(report_path, test[0] + '_Log.txt')

                    self.log.write(f'Report Path: {report_path}\n')
                    self.log.write(f'Log Path: {logPath}\n')

                    output = os.popen(test[1]).read()
                    with open(logPath, 'x') as l:
                        l.write(output)

                elif suite == 'Train':
                    print(os.getcwd())
                    logPath = f'C:\\AutomatedReports_{self.date}\\{self.server}_Reports\\{suite}\\{test[0]}_Log.txt'
                    report_path = os.path.join(
                        self.FINAL_REPORT_PATH, self.server + '_Reports', suite)
                    self.log.write(f'Log Path: {logPath}\n')
                    output = os.popen(test[1]).read()
                    with open(logPath, 'x') as l:
                        l.write(output)

                # Get all items in Generated reports and move them to the correct report folder

                self.Move_Reports(report_path, test[0])

    def Run_Collab(self):
        self.log.write('\n============= RUN ALL SCRIPTS ===============\n')
        self.log.write(f'Test Suite Path: {os.getcwd()}')

        for suite, tests in self.Scripts_To_Run.items():
            self.log.write(f'\n------ {suite} ------\n')
            for test in tests:

                os.chdir(self.TEST_SUITE_PATH)
                if suite == 'Collab':
                    self.log.write(f'\n--------- {test[0]} -------\n')
                    print(f'Starting {test[0]}')
                    report_path = os.path.join(
                        self.FINAL_REPORT_PATH, self.server + '_Reports', suite, test[0])
                    # C:\\AutomatedReports\72X_Reports\Collab\ContentAdministration    \ContentAdministration_Log.txt
                    logPath = os.path.join(report_path, test[0] + '_Log.txt')

                    self.log.write(f'Report Path: {report_path}\n')
                    self.log.write(f'Log Path: {logPath}\n')

                    output = os.popen(test[1]).read()
                    with open(logPath, 'x') as l:
                        l.write(output)
                self.Move_Reports(report_path, test[0])



creds = ('brant.jolly@assima.net', 'Test!234')
print('Start PSExec before running')
server = input('Server (ex.725): ')
rr = Report_Runner(server)
# rr.Create_Folders()
rr.Install()
rr.Change_Credentials()

choice = input(
    f'Run All Scripts (1)\nRun Scripts Individually (2)\nRun Train{server} (3)\nRun Collab (4)\nChoice: ')

if choice == '1':
    rr.Run_All_Scripts()
elif choice == '2':
    rr.Run_Scripts_Individually()
elif choice == '3':
    rr.Run_Train()
elif choice == '4':
    rr.Run_Collab()

rr.log.close()
