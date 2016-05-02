import os
from os import path
import zipfile


def find_metadata(zf, name):
    print(name)
    idt = name.split('.')[0].split('_')[2]
    if idt not in texts.keys():
        return 0
    cur_text = texts[idt]
    cur_file = zf.open(name)
    try:
        cur_title = cur_text['title']
    except:
        cur_title = ''
    try:
        cur_author = cur_text['author']
    except:
        cur_author = ''
    return idt, cur_text, cur_file, cur_title, cur_author


def search_file(outfile, name, zf, response):
    idt, cur_text, cur_file, cur_title, cur_author = response
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
                    outfile.write(str(idt) +
                                  '\t' +
                                  str(startword) +
                                  '\t' +
                                  str(curword) +
                                  '\t' +
                                  is_do_support +
                                  '\t' +
                                  cur_title +
                                  '\t' +
                                  cur_author +
                                  '\t' +
                                  cur_text['genre'] +
                                  '\t' +
                                  cur_text['year'] +
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

    infile = open('sources_coha.txt')
    names = infile.readline().rstrip().split('\t')

    texts = {}

    for line in infile:
        s = line.rstrip().split('\t')
        texts[s[0]] = {}
        for n in range(1, len(s)-1, 1):
            texts[s[0]][names[n]] = s[n]

    outfile = open('coha_dohave.txt', 'w')

    outfile.write('id\tstartnum\tendnum\tdosupport\tauthor\tgenre\tyear\n')

    for f in files:
        if zipfile.is_zipfile(f):
            zf = zipfile.ZipFile(f)
            zf_names = zf.namelist()
            for name in zf_names:
                response = find_metadata(zf, name)
                if response == 0:
                    continue
                search_file(outfile, name, zf, response)
