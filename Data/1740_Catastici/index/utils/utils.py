import re
import unidecode


def remove_extra_spaces(s):
    return re.sub(r"\s+", " ", s).strip()


def remove_apos(s):
    apos_chars = {"'", "’", "‘", "`"}
    res_words = []
    for w in s.split(" "):
        if w.startswith(tuple(apos_chars)):
            w = w[1:]
        if w.endswith(tuple(apos_chars)):
            w = w[:-1]
        res_words.append(w)

    return " ".join(res_words)


def text_to_minimal(s):
    s_minimal = []
    for word in s.split(" "):
        word = word.lower().strip()

        # exception made for the "°" character
        segments = word.split("°")

        processed_segments = []
        for segment in segments:
            segment = remove_apos(segment)
            segment = remove_extra_spaces(segment)
            segment = unidecode.unidecode(segment)
            processed_segments.append(segment)

        word_minimal = "°".join(processed_segments)
        s_minimal.append(word_minimal)

    return " ".join(s_minimal).strip()


def string_contains_substring(s, sub_s, use_minimal=True):
    if use_minimal:
        s = text_to_minimal(s)
        sub_s = text_to_minimal(sub_s)

    start_idx = s.find(sub_s)
    end_idx = start_idx + len(sub_s)

    if start_idx == -1:
        return False

    if start_idx == 0 and end_idx == len(s):
        return True

    if start_idx == 0 and end_idx < len(s):
        return s[end_idx].isspace() or s[end_idx] == ","

    if start_idx > 0 and end_idx == len(s):
        return s[start_idx - 1].isspace() or s[start_idx - 1] == ","

    if start_idx > 0 and end_idx < len(s):
        return (s[start_idx - 1].isspace() or s[start_idx - 1] == ",") and (
            s[end_idx].isspace() or s[end_idx] == ","
        )

    return False


def has_multiple_owners(owners, separators, use_minimal=True):
    if use_minimal:
        owners = text_to_minimal(owners)

    for sep in separators:
        if sep in owners:
            return True

    return False


def string_contains_one_of_substrings(s, words, use_minimal=True):
    if use_minimal:
        s = text_to_minimal(s)

    for w in words:
        search_term = text_to_minimal(w) if use_minimal else w
        if string_contains_substring(s, search_term, use_minimal=False):
            return True

    return False


def find_substring(s, sub_s, offset=0, use_minimal=True):
    if use_minimal:
        s = text_to_minimal(s)
        sub_s = text_to_minimal(sub_s)

    if offset < 0 or offset > len(s):
        return -1

    pattern = r"\b{}\b".format(re.escape(sub_s))
    match = re.search(pattern, s[offset:])
    return match.start() + offset if match else -1
