import subprocess
import multiprocessing

def run_bot1():

    subprocess.call(['python', 'bot.py'])

def run_bot2():

    subprocess.call(['python', 'script.py'])

if __name__ == '__main__':
    process1 = multiprocessing.Process(target=run_bot1)
    process2 = multiprocessing.Process(target=run_bot2)

    process1.start()
    process2.start()

    process1.join()
    process2.join()
