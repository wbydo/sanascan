import re

class RakutenTravelStrategy():
    p = re.compile(r'(?P<period>(?:。|．|\.|！|!|？|\?)+)')

    def extract_post(self, line):
        csv = line.split('\t')
        contents = csv[2].strip()
        id = int(csv[3])
        return {'id':id, 'contents':contents}
