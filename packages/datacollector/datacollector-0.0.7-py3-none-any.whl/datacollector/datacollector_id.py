from .article import Article
from .util import checkDir
import time

def getIDs(path):
    with open(path, 'r') as in_f:
        return in_f.read().split('\n')

def datacollector_id(path, download=False):
    fail = []
    fail_counter = 0
    pmids = getIDs(path)
    counter = 0
    if pmids:
        for index, pmid in enumerate(pmids):
            try:
                a = Article(pmid, '')
                a.fetcher()
                a.format_json()
                counter += 1
                time.sleep(1)
                if (download):
                    try:
                        a.download()
                        time.sleep(1)
                    except:
                        fail.append(pmid)
                        fail_counter += 1
            except:
                pass
            if (index+1)%100 == 0:
                print('{} / {}'.format(index+1, len(pmids)))
        print('Done {} / {}'.format(index+1, len(pmids)))
        if fail:
            save_path = checkDir('./result/download')
            with open('{}/fail_download_byID.txt'.format(save_path), 'w') as out: out.write('\n'.join(fail))
    print('{} Results saved'.format(counter))
    print('{} PDF downloaded successfully.'.format(counter - fail_counter))
    # print('{} Fail to download'.format(fail_counter))