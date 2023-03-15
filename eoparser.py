import os

lib_dir = os.path.dirname(os.path.abspath(__file__))

x_to_hats = {
        'cx':'ĉ',
        'gx':'ĝ',
        'hx':'ĥ',
        'jx':'ĵ',
        'sx':'ŝ',
        'ux':'ŭ',
        'Cx':'Ĉ',
        'Gx':'Ĝ',
        'Hx':'Ĥ',
        'Jx':'Ĵ',
        'Sx':'Ŝ',
        'Ux':'Ŭ'
}

hats_to_lower = {
        'Ĉ':'ĉ',
        'Ĝ':'ĝ',
        'Ĥ':'ĥ',
        'Ĵ':'ĵ',
        'Ŝ':'ŝ',
        'Ŭ':'ŭ',
}

def xsystem_to_hats(word: str) -> str:
        res = ''
        i = 0
        while i < len(word):
                ch1 = word[i]
                if i == len(word)-1:
                        res += ch1
                        break
                ch2 = word[i+1]
                if ch1+ch2 in x_to_hats:
                        res += x_to_hats[ch1+ch2]
                        i += 2
                else:
                        res += ch1
                        i += 1
        return res

def to_lower(word: str) -> str:
        res = ''
        for ch in word:
                if ch in hats_to_lower:
                        res += hats_to_lower[ch]
                else:
                        res += ch.lower()
        return res

def read_as_set(path: str) -> set:
        f = open(path, encoding = "utf-8")
        s = set()
        for word in f:
                word = word.replace(' ', '').replace('\t', '').replace('\n', '')
                if len(word) == 0 or word[0] == '#':
                        continue
                s.add(str(word))
        f.close()
        return s

class eoparser:
        def __init__(self, **kwargs):
                value_or = lambda d, v, default: d[v] if v in d else default
                roots = value_or(kwargs, "roots", lib_dir+"/roots.txt")
                prefixes = value_or(kwargs, "prefixes", lib_dir+"/prefixes.txt")
                suffixes = value_or(kwargs, "suffixes", lib_dir+"/suffixes.txt")
                full_words = value_or(kwargs, "full_words", lib_dir+"/full_words.txt")
                numbers = value_or(kwargs, "numbers", lib_dir+"/numbers.txt")
                correlatives = value_or(kwargs, "correlatives", lib_dir+"/correlatives.txt")
                self.roots = read_as_set(roots) if type(roots) is str else set(roots)
                self.prefixes = read_as_set(prefixes) if type(prefixes) is str else set(prefixes)
                self.suffixes = read_as_set(suffixes) if type(suffixes) is str else set(suffixes)
                self.full_words = read_as_set(full_words) if type(full_words) is str else set(full_words)
                self.numbers = read_as_set(numbers) if type(numbers) is str else set(numbers)
                self.correlatives = read_as_set(correlatives) if type(correlatives) is str else set(correlatives)

                self.roots.update(self.full_words)

        def parse(self, word: str, keep_ending_marker = False) -> list:
                if word == '':
                        return []
                word = xsystem_to_hats(to_lower(word))

                if word in self.full_words:
                        return [[str(word), 'word']]

                # Try to compose the thing as a number. If not, try other options
                substr = ""
                decomposition = []
                for ch in word:
                        substr += ch
                        if substr in self.numbers:
                                decomposition += [[substr, "root"]]
                                substr = ""
                if substr == "":
                        return decomposition
                # Try to parse it as a correlative
                decomposition = []
                corr_word = word
                # Find if the corralative is prefixed. (eg: samtiel)
                for prefix in self.prefixes:
                        if word[:len(prefix)] == prefix:
                                corr_word = word[len(prefix):]
                                decomposition += [[prefix, 'prefix']]
                                break

                for corr in self.correlatives:
                        idx = corr_word.find(corr)
                        if idx == -1:
                               continue
                        length_diff = len(corr_word) - len(corr)
                        if length_diff == 0:
                                return decomposition + [[str(corr_word), "word"]]
                        elif length_diff == 1 and corr_word[-1] in ('o', 'i', 'a', 'u', 'j', 'n'):
                                return decomposition + [[str(corr_word), "word"]]
                        elif length_diff == 2 and ((corr_word[-2] in ('o', 'i', 'a', 'u') and corr_word[-1] in ('j', 'n')) or corr_word[-2:] == "jn"):
                                return decomposition + [[str(corr_word), "word"]]
                        elif length_diff == 1 and corr_word[-3] in ('o', 'i', 'a', 'u') and corr_word[-2:] == "jn":
                                return decomposition + [[str(corr_word), "word"]]

                # Basically simplifed a GLL parser with some code to 'attemp' to disambiguate
                # esperanto spelling ambiguiaty by finding a compostion that have the minimal amount
                # of particals
                stack = []
                stack.append([0, '', [], 'prefix/root/backformation'])
                possible_compositions = []
                while len(stack) != 0:
                        ctx = stack.pop()
                        idx, substr, tokens, stage = ctx

                        if idx == len(word):
                                continue

                        # Look ahead parser
                        substr = substr + word[idx]
                        stack.append((idx+1, substr, tokens, stage))
                        # Handle word endings
                        if 'end' in stage and len(word)-idx <= 3 and len(substr) <= 3:
                                recudual = word[idx:]
                                if len(recudual) == 1 and recudual[0] in ('o', 'i', 'a', 'e', 'u', '\'', 'n', 'j') and len(substr) == 1:
                                        possible_compositions.append(tokens + ([[recudual, 'pos_marker']] if keep_ending_marker else []))
                                elif len(recudual) == 2 and ((recudual[0] in ('o', 'i', 'a', 'e', 'u') \
                                        and recudual[1] in ('j', 'n')) or recudual in ('as', 'is', 'os', 'us')) and len(substr) == 1:
                                        possible_compositions.append(tokens + ([[recudual, 'pos_marker']] if keep_ending_marker else []))
                                elif len(recudual) == 3 and recudual[0] in ('o', 'i', 'a', 'e', 'u') \
                                         and recudual[1] in ('j', 'n') and recudual[2] in ('j', 'n') and len(substr) == 1:
                                        possible_compositions.append(tokens + ([[recudual, 'pos_marker']] if keep_ending_marker else []))
                        if 'intermid' in stage and word[idx] in ('o', 'i', 'a', 'e', 'u') and len(substr) == 1:
                                stack.append((idx+1, '', tokens + ([[word[idx], 'pos_marker']] if keep_ending_marker else []), 'prefix/root'))
                        if 'root' in stage and substr in self.roots:
                                stack.append((idx+1, '', tokens + [[substr, 'root']], 'root/suffix/end/intermid'))
                        if 'prefix' in stage and substr in self.prefixes:
                                stack.append((idx+1, '', tokens + [[substr, 'prefix']], 'prefix/root'))
                        if 'suffix' in stage and substr in self.suffixes:
                                stack.append((idx+1, '', tokens + [[substr, 'suffix']], 'prefix/root/suffix/end/intermid'))
                        if 'backformation' in stage and substr in self.suffixes:
                                stack.append((idx+1, '', tokens + [[substr, 'suffix']], 'end'))
                        if 'backformation' in stage and substr in self.prefixes:
                                stack.append((idx+1, '', tokens + [[substr, 'prefix']], 'end'))


                if len(possible_compositions) == 0:
                        raise ValueError(f'Cannot parse word: {word}')
                return sorted(possible_compositions, key=lambda it: len(it))[0]

