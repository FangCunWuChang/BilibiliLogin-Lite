from geetest.upgrade import upgradeChromedriver
import sys


if __name__ == '__main__':
    #if sys.argv[-1] != "-disableUpgradeChromedriver":
    #    upgradeChromedriver()

    from application.apps.app import load_app
    load_app().mainloop()
