from spacy.en import English, LOCAL_DATA_DIR
from spacy.parts_of_speech import ADV
import os



data_dir = os.environ.get('SPACY_DATA', LOCAL_DATA_DIR)
nlp = English(data_dir=data_dir)
doc = nlp('Ask not for whom the bell tolls, it tolls for thee.')
# print([(d, d.tag_, d.pos_) for d in doc])

for t in doc:
    print(t.orth_,t.ent_type_ if t.ent_type_ != "" else "(Not and entity)", t.dep_, t.head.orth_, [c.orth_ for c in t.lefts], [c.orth_ for c in t.rights])
    # print(dependency_labels_to_root(t))


doc2 = nlp('Beheading video follows U.S. raid')

for t in doc2:
    print(t.orth_,t.ent_type_ if t.ent_type_ != "" else "(Not and entity)", t.dep_, t.head.orth_, [c.orth_ for c in t.lefts], [c.orth_ for c in t.rights])
    # print(dependency_labels_to_root(t))

