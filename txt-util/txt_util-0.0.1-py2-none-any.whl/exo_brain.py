# -*- coding: utf-8 -*-


def dep_parse_result(text, dump=True, wjson_name=None):
    import urllib3
    import json

    from txt_util.file_op import read_file_utf8

    openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
    accessKey = "f51eeee8-ad69-4826-be27-5d79dd5d4d86"
    analysisCode="dparse"

    requestJson = {
        "access_key": accessKey,
        "argument": {
            "text": text,
            "analysis_code": analysisCode
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson)
    )


    if response.status is 200:
        results_dic = json.loads(response.data)
        if (results_dic['result'] == -1) is True:
            print(results_dic['reason'])
            assert False

        else:
            results_dic = results_dic['return_object']
            sentences = results_dic['sentence']
            if dump is False:
                return sentences
            else:
                if wjson_name is None:
                    print 'wjson_name cannot be None'
                else:
                    json.dump(sentences, open(wjson_name, 'w'))

    elif response.status is 413:
        return 413

    else:
        print ("[responseCode] " + str(response.status))
        print text




def dep_context(dep_parsed_sents):

    import networkx as nx
    import matplotlib.pyplot as plt

    dep_sent_contexts = []
    for sent in dep_parsed_sents:
        graph = nx.Graph()
        targets = []
        id2word = {}

        for dep in sent:

            id = int(dep['id'])
            id2word[id] = [dep['text'], dep['label']]
            graph.add_node(id)
            if len(dep['mod']) > 0:
                for mod in dep['mod']:
                    mod = int(mod)
                    graph.add_edge(mod, id)

            else:
                targets.append(id)

        for target in targets:
            for path in nx.all_simple_paths(graph, source=id, target=target):
                word = ''
                for step in path[::-1]:
                    word += '/'.join([id2word[step][0], id2word[step][1]])+' '
                dep_sent_contexts.append(word)
    return dep_sent_contexts


def dep_context_words(dep_parsed_sents):

    import networkx as nx
    import matplotlib.pyplot as plt

    dep_sent_contexts = []
    for sent in dep_parsed_sents:
        graph = nx.Graph()
        targets = []
        id2word = {}

        for dep in sent:

            id = int(dep['id'])
            id2word[id] = [dep['text'], dep['label']]
            graph.add_node(id)
            if len(dep['mod']) > 0:
                for mod in dep['mod']:
                    mod = int(mod)
                    graph.add_edge(mod, id)

            else:
                targets.append(id)

        for target in targets:
            for path in nx.all_simple_paths(graph, source=id, target=target):
                word = ''
                for step in path[::-1]:
                    word += '/'.join([id2word[step][0], id2word[step][1]])+' '
                dep_sent_contexts.append(word)
    return dep_sent_contexts

"""
for key, val in sentence[0].items():
    print key,
    try:
        assert len(val)
        for ele in val:
            print ele
    except:
        print val

json.dump(sentence[0]['dependency'], open('sample_dep.json','w'))

sample_dep = json.load(open('sample_dep.json'))


plt.subplot(121)
# nx.draw(g, with_labels=True)
nx.draw_shell(graph, with_labels=True, font_weight='bold')
plt.show()

"""
