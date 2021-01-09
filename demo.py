import eoparser
from termcolor import colored
parser = eoparser.eoparser()

txt = """
Esperanto, origine la Lingvo Internacia, estas la plej disvastiĝinta internacia planlingvo. En 1887 Esperanton parolis nur manpleno da homoj; Esperanto havis unu el la plej malgrandaj
lingvo-komunumoj de la mondo. Ĝi funkciis dekomence kiel lingvo de alternativa komunikado kaj de arta kreipovo. En 2012, la lingvo fariĝis la 64-a tradukebla per Google Translate; En
2016, la lingvo fariĝis tradukebla per Yandex Translate; laŭ 2016, Esperanto aperis en listoj de lingvoj plej lernataj kaj konataj en Hungarujo. La nomo de la lingvo venas de la
kaŝnomo “D-ro Esperanto„ sub kiu la juda kuracisto Ludoviko Lazaro Zamenhofo en la jaro 1887 publikigis la bazon de la lingvo. La unua versio, la rusa, ricevis la cenzuran permeson
disvastiĝi en la 26-a de julio; ĉi tiun daton oni konsideras la naskiĝtago de Esperanto. Li celis kaj sukcesis krei facile lerneblan neŭtralan lingvon, taŭgan por uzo en la internacia
komunikado; la celo tamen ne estas anstataŭigi aliajn, naciajn lingvojn.
"""
word = ''
for ch in txt+' ':
        if eoparser.to_lower(ch) in 'abcdefghijklmnopurstuvwxyzĉĝĥĵŝŭ':
                word += ch
                continue
        else:
               if len(word) == 0:
                      print(colored(ch, 'white'), end='')
                      continue

               try:
                       decompostion = parser.parse(word, keep_ending_marker=True)
                       assert(type(decompostion) is list)
                       root_count = 0
                       idx = 0
                       for particle, particle_type in decompostion:
                                color = ''
                                if particle_type == 'prefix':
                                        color = 'green'
                                elif particle_type == 'root':
                                        color = 'blue' if root_count%2==0 else 'cyan'
                                        root_count += 1
                                elif particle_type == 'suffix':
                                        color = 'yellow'
                                elif particle_type == 'word':
                                        color = 'magenta'
                                elif particle_type == 'pos_marker':
                                       color = 'white'

                                print(colored(word[idx:idx+len(particle)], color), end='')
                                idx += len(particle)
               except:
                       print(colored(word, 'red'), end='')

               word = ''
               print(colored(ch, 'white'), end='')
print()
