import os
from os import path
import zipfile


def find_metadata(zf, name):
    cur_file = zf.open(name)
    cur_genre = name.split('.')[0].split('_')[0]
    cur_year = name.split('.')[0].split('_')[1]
    cur_idt = name.split('.')[0].split('_')[2]
    return (cur_file, cur_genre, cur_year, cur_idt)


def search_file(outfile, name, zf, response):
    cur_file, cur_genre, cur_year, cur_idt = response
    startword = 0
    curword = 0
    do_word = -1
    have_word = -1
    neg_word = -1
    is_do_support = 'NA'
    cur_token = ''
    for line in cur_file:
        line = str(line)
        s = line.rstrip().split('\\t')
        try:
            cur_token += ' ' + s[0].split("'")[1] + ':' + s[2].split('\\')[0]
        except:
            pass
        try:
            if ((s[1] in ['.', '?', '!']) or (s[0] == '@' and s[2] == 'ii')):
                if is_do_support != 'NA':
                    outfile.write(str(cur_idt) +
                                  '\t' +
                                  str(startword) +
                                  '\t' +
                                  str(curword) +
                                  '\t' +
                                  is_do_support +
                                  '\t' +
                                  cur_genre +
                                  '\t' +
                                  cur_year +
                                  '\n')
                startword = curword + 1
                do_word = -1
                have_word = -1
                cur_token = ''
                is_do_support = 'NA'
                neg_word = -1
            elif is_do_support == '1':
                continue
            elif (s[1] == 'do' and have_word == -1):
                do_word = curword
            elif 'vh0' in s[2] or 'vhd' in s[2] or 'vhz' in s[2]:
                have_word = curword
            elif curword - do_word == 1 and 'xx' not in s[2]:
                do_word = -1
            elif curword - have_word == 1 and 'xx' not in s[2]:
                have_word = -1
            elif do_word != -1 and 'xx' in s[2]:
                neg_word = curword
            elif (neg_word != -1 and do_word != -1):
                if 'vhi' in s[2]:
                    is_do_support = '1'
                    have_word = curword
                else:
                    neg_word = -1
                    do_word = -1
            elif do_word == -1 and 'xx' in s[2] and have_word != -1:
                is_do_support = '0'
            elif is_do_support != 'NA':
                if ((curword - have_word <= 7 and
                    ('vbn' in s[2] or
                     'vvn' in s[2])) or
                   (curword - neg_word == 1 and 'to' in s[2])):
                    is_do_support = 'NA'
                    have_word = -1
                    neg_word = -1
        except:
            return
        curword += 1


if __name__ == "__main__":
    files = [x for x in os.listdir('.') if path.isfile('.'+os.sep+x)]

    outfile = open('coha_dohave.txt', 'w')

    outfile.write('id\tstartnum\tendnum\tdosupport\tauthor\tgenre\tyear\n')

    for f in files:
        print(f)
        if zipfile.is_zipfile(f):
            zf = zipfile.ZipFile(f)
            zf_names = zf.namelist()
            for name in zf_names:
                response = find_metadata(zf, name)
                search_file(outfile, name, zf, response)
