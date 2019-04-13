import pyautogui as pag
import time

numberOfTabs=5

def login():
    time.sleep(1)
    pag.typewrite("ossuser")
    pag.press("enter")
    time.sleep(1)
    pag.typewrite("Dtac@6677")
    pag.press("enter")
    time.sleep(1)

run_script = ['alt','right','right','right','right','right','enter',
                        'down','down','down','down','down','enter']
run_clone = ['alt','enter','down','down','down','down','down',
             'down','down','enter']

pag.PAUSE = 5
pag.press('alt')
pag.PAUSE = 0.2
for i in range(numberOfTabs-1):
    login()
    time.sleep(1)
    pag.press(run_script)
    time.sleep(1)
##    pag.typewrite(str(i+1))
##    pag.typewrite("/")
##    pag.typewrite(str(numberOfTabs))
    pag.typewrite(str(i+1)+"/"+str(numberOfTabs),interval=0.2)
    time.sleep(1)
    pag.press("enter")
    time.sleep(2)
    pag.press(run_clone)

login()
pag.press(run_script)
pag.typewrite(str(numberOfTabs)+"/"+str(numberOfTabs))
time.sleep(2)
pag.press("enter")

##pag.press(['alt','enter','down','down','down','down','down','enter','enter'])
