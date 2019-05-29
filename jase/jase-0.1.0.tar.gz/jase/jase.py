#jass: Just A Simple Sentiment analysis tool for English
#Version: 0.1
#Author: Hsin-Min Lu; luim@ntu.edu.tw
#Users Beware: This project was created for pedagogical purpose, and is not suitable for production use.

import os
#from datetime import datetime
import pandas as pd
import pkg_resources
import re
import csv

class jase:
    def __init__(self, debug = 0, basedir = "jase", dict_fn = "data/dict_v1.csv"):
        self.debug = debug
        #self.tb_word_tokenizer = nltk.tokenize.treebank.TreebankWordTokenizer()
        #tokenizer = RegexpTokenizer('(?u)\W+|\$[\d\.]+|\S+')
        self.special_chars = ['.', ',', '!', '?', '(', ')', '%', '*']
        #self.lang = "eng"
        self.re_mon1 = re.compile(
            '^\$?\-?([1-9]{1}[0-9]{0,2}(\,\d{3})*(\.\d{0,2})?|[1-9]{1}\d{0,}(\.\d{0,2})?|0(\.\d{0,2})?|(\.\d{1,2}))$|^\-?\$?([1-9]{1}\d{0,2}(\,\d{3})*(\.\d{0,2})?|[1-9]{1}\d{0,}(\.\d{0,2})?|0(\.\d{0,2})?|(\.\d{1,2}))$|^')
        #self.cmud = cmudict.dict()
        dict_fn = pkg_resources.resource_filename('jase', "data/dict_v1.csv")
        csvreader = csv.reader(open(dict_fn, newline=''))
        self.csv_header = next(csvreader)

        self.all_keywords = []

        key_count = 0
        for aline in csvreader:
            key_count = key_count + 1
            category = aline[0]
            case_sen = aline[1].strip()
            key1 = aline[2]
            dateadded = aline[3]

            # remove extra space
            key1 = key1.strip()
            sub_space = re.compile('\s+')
            key1 = sub_space.sub(' ', key1)

            akey = dict()
            akey['category'] = category
            akey['case_sen'] = case_sen
            akey['dateadded'] = dateadded
            akey['key'] = key1

            key_re = "\\b" + key1.replace(".", "\.") + "\\b"
            akey['key_re'] = key_re
            if case_sen == '1':
                akey['re'] = re.compile(key_re)
            else:
                akey['re'] = re.compile(key_re, re.I)

            self.all_keywords.append(akey)
            if self.debug: print ("%s: %s" % (aline[0], key1))

    def match_keywords(self, thisdoc):
        sum1 = dict()
        for akey in self.all_keywords:
            re1 = akey['re']
            cate = akey['category']
            m1 = re1.findall(thisdoc)
            if cate in sum1:
                sum1[cate] = sum1[cate] + len(m1)
            else:
                sum1[cate] = len(m1)
        return (sum1)

    def mark_match_keywords(self, thisdoc):
        #sum1 = dict()
        allresult = []
        for akey in self.all_keywords:
            re1 = akey['re']
            cate = akey['category']
            m1 = re1.findall(thisdoc)

            for m in re1.finditer(thisdoc):
                #print(cate, akey['key_re'], m.start(), m.end(), m.group())
                allresult.append([cate, akey['key'], m.start(), m.end(), m.group()])

        out2 = pd.DataFrame(allresult, columns=['cate', 'key', 'start', 'end', 'match'])
        out3 = out2.sort_values(by=['start'])

        idx = 0
        outstr = ""
        for agroup in out3.groupby(by=['start']):
            # print(agroup)
            #nmatch = len(agroup[1])
            start = agroup[1]['start'].values[0]
            end = agroup[1]['end'].values[0]
            cate_str = ",".join(set(agroup[1]['cate'].values))

            # pre_str = text0[idx:start]
            outstr += text0[idx:end]
            outstr += "[" + cate_str + "]"

            idx = end

        #print(outstr)

        return(outstr)



if __name__ == "__main__":
    #jase1 = jase(debug = 1)
    jase1 = jase()

    text0 = """Item 7. MANAGEMENT S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS
CAUTIONARY NOTE
The following discussion should be read in conjunction with Item 8, Consolidated Financial Statements and Supplementary Data, included in this Annual Report on Form 10-K. This discussion contains forward-looking statements that involve risks and uncertainties. Our actual results could differ materially from the results anticipated in these forward-looking statements as a result of factors including, but not limited to, those under Risk Factors contained in Item 1A, in this Annual Report on From 10-K.
OVERVIEW
We provide outsourced, web and phone- based financial technology services to financial institution, biller, card issuer and creditor clients and their millions of consumer end-users. We currently derive approximately 80% of our revenues from payments and 20% from other services including account presentation relationship management, professional services, and custom software solutions. End-users may access and view their accounts online and perform various web-based self-service functions. They may also make electronic bill payments and funds transfers, utilizing our unique, real-time debit architecture, ACH and other payment methods. Our value-added relationship management services reinforce a favorable user experience and drive a profitable and competitive Internet channel for our clients. Further, we have professional services, including software solutions, which enable various deployment options, a broad range of customization and other value-added services.
We currently operate in two business segments Banking and eCommerce. The operating results of these business segments exclude general corporate overhead expenses. Within each business segment, we face differing opportunities, challenges and risks. In our Banking segment we have the opportunity to deploy the new and enhanced products we have developed to expand and deepen the relationships we have with our existing clients. Our differentiated account presentation and payments products, as well as our ability to deliver a full suite of remote delivery financial services, provide the opportunity for us to increase market share particularly among mid-sized financial institutions. In the bank market, a very large percentage of financial institutions now offer internet banking and bill payment to their customers. We therefore face competition in our efforts to obtain new clients from other established providers of these services. The end-user base within these clients is not highly penetrated,
however, so we benefit from continuing adoption increases.
Additionally, financial service providers have recently been adversely affected by significant illiquidity and credit tightening trends in the financial markets in which they operate. Unfavorable economic conditions adversely impacting those types of business could have a material adverse effect on our business.
In our eCommerce segment, there are still a significant number of potential clients who do not offer services such as those we are in a position to provide to their customer base. Further, the competition to provide these services is more fragmented than it is in the banking market. These factors provide us with the opportunity to expand our client base. We also offer an innovative debt collection product that is attractive to a number of large and mid-sized potential clients. For a portion of our eCommerce business, our revenue is tied to the value of the payment being made which exposes us to the impact of economic factors on these payments. We also continuously monitor the potential risks that we face due to the interfaces we have with, and our reliance on, various payments networks.
Across our markets, we are exposed to interest rate risk as we earn interest income from the bill payment funds in transit we hold on behalf of our end-users. We also closely monitor covenant and other compliance requirements under our debt and preferred stock agreements, as well as other potential risks associated with our capital structure.
We have experienced, and expect to continue to experience, significant user and transaction growth. This growth has placed, and will continue to place, significant demands on our personnel, management and other resources. We will need to continue to expand and adapt our infrastructure, services and related products to

accommodate additional clients and their end-users, increased transaction volumes and changing end-user requirements.
Registered end-users using account presentation, bill payment or both, and the payment transactions executed by those end-users are the major drivers of our revenues. Since December 31, 2009, the number of users of our account presentation services increased 3%, and the number of users of our payment services increased 15%, for an overall 12% increase in users.
The following table summarizes users and payment services transactions:"""


    out1 = jase1.mark_match_keywords(text0)
    print(out1)

    sum1 = jase1.match_keywords(text0)
    print(sum1)

    #import re
    #p = re.compile("[a-z]")
