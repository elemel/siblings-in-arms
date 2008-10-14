# Copyright (c) 2008 Mikael Lind
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import sys, os, pygame


def main():
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: loop <file>\n'
                         'Loop a music file with pygame.\n')
        sys.exit(1)
    path = sys.argv[1]
    if not os.path.isfile(path):
        sys.stderr.write('No such file: %s\n' % path)
        sys.exit(1)
    pygame.mixer.pre_init(44100, -16, 2, 1024 * 3)
    pygame.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(-1)
    sys.stderr.write('Looping music file. Press <enter> to stop.\n')
    sys.stdin.readline()


if __name__ == '__main__':
    main()
