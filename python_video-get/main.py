from common import *
import argparse,sys,config

if __name__ == '__main__':
    for i in sys.argv:
        print(i)
    if len(sys.argv) == 1:
	    sys.argv.append('--help')
    
    parser = argparse.ArgumentParser(description=config.NAME+':'+config.VERSION)
    parser.add_argument('-d', '--dir', help='download path')
    parser.add_argument('-k', '--kkk',help='search content')
    parser.add_argument('-p', '--page',help='the number of')
    args = parser.parse_args()
    print(args.dir)
    main()

