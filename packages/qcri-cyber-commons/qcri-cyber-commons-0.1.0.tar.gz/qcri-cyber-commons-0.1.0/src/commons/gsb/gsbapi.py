from pysafebrowsing import SafeBrowsing
import pandas as pd
import sys

keys = ['AIzaSyCXUW2uCTHoSyLjAIEKzNRPUIXCfG3MScU', #0 digestize
        'AIzaSyCtXkzebCAfuISFqAog9pep_sSvY1-9SWY', #1 minhaj
        'AIzaSyAoA6JzjEYv3vqBqiJT4BS621sBJmodiao'] #2



infile = sys.argv[1]
outfile = sys.argv[2]
index = int(sys.argv[3])

gsb = SafeBrowsing(keys[index])

urls = []
with open(infile) as inf:
    for line in inf:
        urls.append(line.strip())

res = gsb.lookup_urls(urls)

if res != None:
    drop_list = []
    for key, values in res.items():
        try:
            if res[key]['malicious'] == False:
                drop_list.append(key)
        except KeyError as e:
            print("Key error: URL: {}".format(key))
            pass

    for url in drop_list:
        del res[url]

    res2 = []
    for key, values in res.items():
        values['url'] = key
        res2.append(values)

    res_df = pd.DataFrame().from_records(res2)
    res_df.to_csv(outfile, index = False)

