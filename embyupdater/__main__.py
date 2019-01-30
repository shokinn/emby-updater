#!/usr/bin/env python3
import os
import sys

try:
    import embyupdater
except ImportError:
    sys.path.append(os.path.abspath('..'))
    import embyupdater

if __name__ == '__main__':
    embyupdater.main()
