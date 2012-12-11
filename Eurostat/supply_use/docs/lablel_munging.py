import cPickle

files = ["use_col_lables.txt", "use_row_labels.txt"]

name = files[1]
f = open(name, 'r')
lines = f.readlines()
f.close()

sp = []

for l in lines:
    sp.append(l.split(' ', 1))

d = {k: v.lstrip() for k, v in sp}

out = open('clean_' + name[:-4] + '.pkl', 'w')
cPickle.dump(d, out, protocol=2)
out.close()
