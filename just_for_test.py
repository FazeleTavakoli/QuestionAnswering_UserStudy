import re


# sparql = "{ <?x <http://dbpedia.org/property/international> <http://dbpedia.org/resource/Muslim_Brotherhood> . ?x <http://dbpedia.org/ontology/religion> ?uri  . ?x <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/ontology/PoliticalParty>}"
# lines = sparql.split(" .")
#
#
# pattern = re.compile(r'(\?(uri))|(\?(x))|(resource/[^<>]+>)|(property/[^<>]+>)|(ontology/[^<>]+>)|(\#type)')  # lcquad_1
# nodes = []
# links = []
#
# pattern_1 = re.compile(r'(resource/)([^<>]+)')
# pattern_2 = re.compile(r'([^<>]+)(\?uri)')
# input_string = "resource/Marine_Corps_Air_Station_Kaneohe_Bay"
# input_string_1 = "SELECT DISTINCT ?uri WHERE { ?uri <http://dbpedia.org/property/mouthLocation> <http://dbpedia.org/resource/Arctic_Ocean> . ?uri <http://dbpedia.org/property/mouthLocation> <http://dbpedia.org/resource/Laptev_Sea> . ?uri <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/ontology/River>}"
# title = pattern_1.match(input_string)
# matched_titles = pattern_2.finditer(input_string_1)
#
# print(title)
# for t in matched_titles:
#     printed_t = t.group(0)
#     print(printed_t)
#
#
# pattern_3 = re.compile(r'[/][^/]+')
# input_string_3 = "Element <uri> with attributes {}, children [] and cdata http://dbpedia.org/resource/United_States_Navy"
# matched_titles_1 = pattern_3.finditer(input_string_3)
# for t in matched_titles_1:
#     printed_t_1 = t.group(0)
#     print(printed_t_1)
#
#
# title_1 = pattern_3.match(input_string_3)
# print(title_1)

sparql_1 = 'SELECT DISTINCT COUNT(?uri) WHERE { ?x <http://dbpedia.org/ontology/commander> <http://dbpedia.org/resource/Andrew_Jackson> . ?uri <http://dbpedia.org/ontology/knownFor> ?x  . }'
lines_55 = re.split('\s\.|\.\s', sparql_1)


# if "}" in lines_55[len(lines_55)-1]:
#             del lines_55[len(lines_55)-1]


input_string = "Element <literal> with attributes {'datatype': 'http://www.w3.org/2001/XMLSchema#integer'}, children [] and cdata Northern Carolina http://hello/world"
pattern = re.compile(r'(cdata) (((\w+)(\s+))+|(\d+))')
matched_titles = pattern.finditer(input_string)
for match in matched_titles:
    title = match.group()
    print(title)
title_1 = pattern.match(input_string)
a = 2

input_string_1 = 'ASK WHERE { <http://dbpedia.org/resource/Fluidinfo> <http://dbpedia.org/property/programmingLanguage> <http://dbpedia.org/resource/PostgreSQL> }'
pattern = re.compile(r'(\?(uri))|(\?(x))|(resource/[^<>]+>)|(property/[^<>]+>)|(ontology/[^<>]+>)|(\#type)')
matched_titles = pattern.finditer(input_string_1)
for match in matched_titles:
    title = match.group()
    a = 1
