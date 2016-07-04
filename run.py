import os
import behaviroal_targeting
import ctr
import time

def main():
    while True:
        behaviroal_targeting.main()
        ctr.main()
        print "UPDATE."
        time.sleep(2)

if __name__ == "__main__":
    main()