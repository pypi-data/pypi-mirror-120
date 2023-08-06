# Utilities for manipulating word data structures
#
# Copyright (c) 2018-2021 Tatu Ylonen.  See file LICENSE and https://ylonen.org

import re
import collections
from .config import WiktionaryConfig
from wikitextprocessor import ALL_LANGUAGES, Wtp

# Mapping from language name to language info
languages_by_name = {x["name"]: x for x in ALL_LANGUAGES}
# Add "other_names", taking care not to override primary names
for x in ALL_LANGUAGES:
    for xn in x.get("other_names", ()):
        if xn not in languages_by_name:
            languages_by_name[xn] = x
# Add "aliases", taking care not to override primary names
for x in ALL_LANGUAGES:
    for xn in x.get("aliases", ()):
        if xn not in languages_by_name:
            languages_by_name[xn] = x

# Mapping from language code to language info
languages_by_code = {x["code"]: x for x in ALL_LANGUAGES}

# Keys in ``data`` that can only have string values (a list of them)
str_keys = ("tags", "glosses")
# Keys in ``data`` that can only have dict values (a list of them)
dict_keys = set(["pronunciations", "senses", "synonyms", "related",
                 "antonyms", "hypernyms", "holonyms", "forms"])


def data_append(ctx, data, key, value):
    """Appends ``value`` under ``key`` in the dictionary ``data``.  The key
    is created if it does not exist."""
    assert isinstance(ctx, Wtp)
    assert isinstance(data, dict)
    assert isinstance(key, str)

    if key in str_keys:
        assert isinstance(value, str)
    elif key in dict_keys:
        assert isinstance(value, dict)
    if key == "tags":
        if value == "":
            return
    lst = data.get(key)
    if lst is None:
        lst = []
        data[key] = lst
    lst.append(value)


def data_extend(ctx, data, key, values):
    """Appends all values in a list under ``key`` in the dictionary ``data``."""
    assert isinstance(ctx, Wtp)
    assert isinstance(data, dict)
    assert isinstance(key, str)
    assert isinstance(values, (list, tuple))

    # Note: we copy values, just in case it would actually be the same as
    # data[key].  This has happened, and leads to iterating for ever, running
    # out of memory.  Other ways of avoiding the sharing may be more
    # complex.
    for x in tuple(values):
        data_append(ctx, data, key, x)


def split_at_comma_semi(text, extra=()):
    """Splits the text at commas and semicolons, unless they are inside
    parenthesis."""
    assert isinstance(text, str)
    assert isinstance(extra, (list, tuple))
    lst = []
    paren_cnt = 0
    bracket_cnt = 0
    ofs = 0
    parts = []
    split_re = r"[][(),;，]"  # Note: special unicode comma
    if extra:
        split_re = "({})|{}".format(split_re,
                                    "|".join(re.escape(x) for x in extra))
    for m in re.finditer(split_re, text):
        if ofs < m.start():
            parts.append(text[ofs:m.start()])
        if m.start() == 0 and m.end() == len(text):
            return [text]  # Don't split if it is the only content
        ofs = m.end()
        token = m.group(0)
        if token == "[":
            bracket_cnt += 1
            parts.append(token)
        elif token == "]":
            bracket_cnt -= 1
            parts.append(token)
        elif token == "(":
            paren_cnt += 1
            parts.append(token)
        elif token == ")":
            paren_cnt -= 1
            parts.append(token)
        elif paren_cnt > 0 or bracket_cnt > 0:
            parts.append(token)
        else:
            if parts:
                lst.append("".join(parts).strip())
                parts = []
    if ofs < len(text):
        parts.append(text[ofs:])
    if parts:
        lst.append("".join(parts).strip())
    return lst

def split_slashes(ctx, text):
    """Splits the text at slashes.  This tries to use heuristics on how the
    split is to be interpreted, trying to prefer longer forms that can be
    found in the dictionary."""
    text = text.strip()
    if ctx.page_exists(text):
        return [text]

    text = re.sub(r"[／]", "/", text)
    alts = text.split(" / ")  # Always full split at " / "
    ret = []
    for alt in alts:
        alt = alt.strip()
        if alt.find("/") < 0 or alt[0] == "/" or alt[-1] == "/":
            # No slashes, no splitting; or starts/ends with a slash
            ret.append(alt)
            continue

        # Split text into words.  If only one word, assume single-word splits
        words = alt.split()
        if len(words) == 1:
            # Only one word
            ret.extend(x.strip() for x in alt.split("/"))
            continue

        # More than one word
        cands = [((), ())]
        for word in alt.split():
            new_cands = []
            parts = word.split("/")
            if len(parts) == 1:
                for ws, divs in cands:
                    ws = ws + tuple(parts)
                    new_cands.append([ws, divs])
            else:
                # Otherwise we might either just add alternatives for this word
                # or add alternatives for the whole phrase
                for p in parts:
                    for ws, divs in cands:
                        ws = ws + (p,)
                        new_cands.append(((), divs + (ws,)))
                        new_cands.append((ws, divs))
            cands = new_cands

        # Finalize candidates
        final_cands = set()
        for ws, divs in cands:
            if not ws:
                final_cands.add(divs)
                continue
            final_cands.add(divs + (ws,))
        print("final_cands", final_cands)

        # XXX this does not work yet
        ht = collections.defaultdict(list)
        for divs in final_cands:
            assert isinstance(divs, tuple) and isinstance(divs[0], tuple)
            score = 0
            words = []
            for ws in divs:
                assert isinstance(ws, tuple)
                exists = ctx.page_exists(" ".join(ws))
                words.extend(ws)
                score += 100
                score += 1 / len(ws)
                #if not exists:
                #    score += 1000 * len(ws)
            key = tuple(words)
            ht[key].append((score, divs))
        for key, items in sorted(ht.items()):
            print("key={} items={}".format(key, items))
            score, divs = min(items)
            for ws in divs:
                ret.append(" ".join(ws))

    return ret
