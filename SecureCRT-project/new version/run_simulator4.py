import pyautogui as pag
import time

num = int(input("input number of tabs: "))
numberOfTabs=num
print("Please change the window to SecureCRT tab in 10 seconds")
print("cancel this program by using CTRL+C")
time.sleep(2)
print("Simulator will run in 8 seconds...")
time.sleep(8)
print("Simulator is running....")

run_script = ['alt','right','right','right','right','right','enter',
                        'down','down','down','down','down','enter']
run_clone = ['alt','enter','down','down','down','down','down','down','down','enter']

pag.PAUSE = 4
pag.press('alt')
pag.PAUSE = 0.2
pag.press('alt')
for i in range(numberOfTabs-1):
    pag.press(run_script)
    time.sleep(1.5)
    pag.typewrite(str(i+1)+"/"+str(numberOfTabs))
    time.sleep(1)
    pag.press("enter")
    time.sleep(1.5)
    pag.press(run_clone)

time.sleep(2)
pag.press(run_script)
pag.typewrite(str(numberOfTabs)+"/"+str(numberOfTabs))
time.sleep(2)
pag.press("enter")
print("SIMULATION FINISH")
