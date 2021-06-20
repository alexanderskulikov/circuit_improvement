from os import listdir, system
from circuit import Circuit

for ckt_file in sorted(listdir('circuits/mod3/')):
    if ckt_file.endswith('.ckt'):
        print(ckt_file)
        circuit = Circuit(fn='mod3/' + ckt_file[:-4])
        circuit.draw(ckt_file[:-4], experimental=True)

# circuit = Circuit(fn='mod3/mod3_6_0_size12')
# circuit.draw('mod3_6_0_size12', experimental=True)
#
# circuit = Circuit(fn='mod3/mod3_6_1_size13')
# circuit.draw('mod3_6_1_size13', experimental=True)