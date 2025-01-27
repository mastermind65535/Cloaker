import psutil
import os
import sys
import time
import datetime
import argparse

class Scanner:
    class Process:
        def __init__(self, time:float, SHOW_EX=False):
            self.TIME = float(time)
            self.SHOW_EX = bool(SHOW_EX)
            self.EXCLUDE_EXTENSIONS = [
                "DLL",
                "EXE",
                "SYS",
                "MUI",
            ]

            self.HIGHLIGHT_EXTENSIONS = [
                "LOG",
                "TXT",
                "JSON",
                "YAML",
                "YML",
                "XML",
                "DB",
                "SQLITE",
                "BIN",
                "DAT"
            ]

        def scan(self):
            detected_file = []
            for proc in psutil.process_iter():
                try:
                    if proc.create_time() < self.TIME:
                        create_time = datetime.datetime.fromtimestamp(proc.create_time()).strftime("%Y-%m/%d-%H:%M:%S")
                        files = proc.open_files()
                        if len(files) == 0 and self.SHOW_EX == False: continue
                        print(f"{create_time} | PID: {proc.pid} | Name: {proc.name()}")
                        for file in files:
                            path = file.path
                            extension = path.split(".")[-1].upper()
                            if not extension in self.EXCLUDE_EXTENSIONS and self.SHOW_EX == False:
                                if extension in self.HIGHLIGHT_EXTENSIONS:
                                    print(f"|-\033[31m{path}\033[0m")
                                    detected_file.append(path)
                                else:
                                    print(f"|-{path}")
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass

            print("*" * 50)

            for item in detected_file:
                print(f"\033[31m{item}\033[0m")
                

def main():
    parser = argparse.ArgumentParser(prog="Cloaker", usage="Cloaker [OPTIONS]")
    parser.add_argument("-t", "--time", help="Specify possible logged time.", required=True, type=str)
    parser.add_argument("-sP", "--scan-process", help="Scan possible logging processes to identify log files.", action="store_true")
    parser.add_argument("-sF", "--scan-file", help="Scan possible log files that may contains logs.", action="store_true")
    parser.add_argument("-e", "--exclude-show", help="Show excluded results.", action="store_true")

    arguments = parser.parse_args()
    TIME = None
    if arguments.time == "ctime": TIME = time.time()
    else: TIME = datetime.datetime.strptime(arguments.time, "%Y-%m/%d-%H:%M:%S").timestamp()
    if arguments.scan_process == True:
        Engine = Scanner.Process(TIME)
        Engine.scan()

if __name__ == '__main__':
    main()