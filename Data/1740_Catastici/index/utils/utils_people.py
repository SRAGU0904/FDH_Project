import utils.utils as u


def extract_names(
    owner_text_minimal,
    family_names,
    first_names,
    collisions,
    ignore_next,
    cities,
    places,
):

    # =========================== PRE-PROCESSING ===========================
    owner_text_minimal = remove_ignore_next(
        owner_text_minimal, ignore_next, family_names
    )

    owner_text_minimal = remove_places(owner_text_minimal, places)

    contains_last_name = u.string_contains_one_of_substrings(
        owner_text_minimal, family_names, use_minimal=False
    )
    if not contains_last_name:
        return None

    if u.string_contains_one_of_substrings(
        owner_text_minimal, collisions, use_minimal=False
    ):
        return {"label": "PPL_VRF", "name_labeled_map": {}}

    # definition of accepted words as family names and first names
    accepted_words = []
    accepted_words.extend(
        family_names
    )  # no split because of composed family names (e.g. de Gasparo)
    for fn in first_names:
        accepted_words.extend(fn.split())
    accepted_words = sorted(list(set(accepted_words)), key=len, reverse=True)

    # find owner first and family names taking into account composed names
    owner_text_split = owner_text_minimal.split(" ")
    owner_names = populate_owner_name_array(owner_text_split, accepted_words)

    # remove city collision if also family name
    owner_names = remove_city_collision(owner_names, cities, family_names)
    if len(owner_names) == 0 or len(owner_names) > 4:
        return None

    # ============================ ASSIGNATION ============================

    extraction_result = {
        "label": "PPL",
        "name_labeled_map": {"FIRST_NAME": "", "LAST_NAME": ""},
    }

    if len(owner_names) == 1:
        name = owner_names[0]

        if name in family_names:
            extraction_result["name_labeled_map"]["LAST_NAME"] = name
        elif name in first_names:
            extraction_result["name_labeled_map"]["FIRST_NAME"] = name
            extraction_result["label"] = "PPL_VRF"
        else:
            extraction_result["label"] = "PPL_VRF"

        return format_extraction_result(extraction_result)

    elif len(owner_names) == 2:
        name1, name2 = owner_names

        if name1 in first_names and name2 in family_names:
            extraction_result["name_labeled_map"]["FIRST_NAME"] = name1
            extraction_result["name_labeled_map"]["LAST_NAME"] = name2
        elif name1 in family_names and name2 in family_names:
            extraction_result["name_labeled_map"]["LAST_NAME"] = f"{name1} {name2}"
        elif name1 in family_names and name2 in first_names:
            extraction_result["name_labeled_map"]["FIRST_NAME"] = name2
            extraction_result["name_labeled_map"]["LAST_NAME"] = name1
        else:
            extraction_result["label"] = "PPL_VRF"

        return format_extraction_result(extraction_result)

    elif len(owner_names) == 3:
        name1, name2, name3 = owner_names

        if name1 in first_names and name2 in first_names and name3 in family_names:
            extraction_result["name_labeled_map"]["FIRST_NAME"] = f"{name1} {name2}"
            extraction_result["name_labeled_map"]["LAST_NAME"] = name3
        elif name1 in first_names and name2 in family_names and name3 in family_names:
            extraction_result["name_labeled_map"]["FIRST_NAME"] = name1
            extraction_result["name_labeled_map"]["LAST_NAME"] = f"{name2} {name3}"
        elif name1 in family_names and name2 in family_names and name3 in family_names:
            extraction_result["name_labeled_map"][
                "LAST_NAME"
            ] = f"{name1} {name2} {name3}"
        elif name1 in family_names and name2 in first_names and name3 in first_names:
            extraction_result["name_labeled_map"]["FIRST_NAME"] = f"{name2} {name3}"
            extraction_result["name_labeled_map"]["LAST_NAME"] = name1
        elif name1 in family_names and name2 in family_names and name3 in first_names:
            extraction_result["name_labeled_map"]["FIRST_NAME"] = name3
            extraction_result["name_labeled_map"]["LAST_NAME"] = f"{name1} {name2}"
        else:
            extraction_result["label"] = "PPL_VRF"

        # Check for ambiguous middle names that are both first and last names
        if name2 in first_names and name2 in family_names:
            extraction_result["label"] = "PPL_VRF"

        return format_extraction_result(extraction_result)

    elif len(owner_names) == 4:
        name1, name2, name3, name4 = owner_names

        if (
            name1 in first_names
            and name2 in first_names
            and name3 in family_names
            and name4 in family_names
        ):
            extraction_result["name_labeled_map"]["FIRST_NAME"] = f"{name1} {name2}"
            extraction_result["name_labeled_map"]["LAST_NAME"] = f"{name3} {name4}"
        elif (
            name1 in first_names
            and name2 in family_names
            and name3 in family_names
            and name4 in family_names
        ):
            extraction_result["name_labeled_map"]["FIRST_NAME"] = name1
            extraction_result["name_labeled_map"][
                "LAST_NAME"
            ] = f"{name2} {name3} {name4}"
        elif (
            name1 in family_names
            and name2 in family_names
            and name3 in first_names
            and name4 in first_names
        ):
            extraction_result["name_labeled_map"]["FIRST_NAME"] = f"{name3} {name4}"
            extraction_result["name_labeled_map"]["LAST_NAME"] = f"{name1} {name2}"
        elif (
            name1 in family_names
            and name2 in family_names
            and name3 in family_names
            and name4 in first_names
        ):
            extraction_result["name_labeled_map"]["FIRST_NAME"] = name4
            extraction_result["name_labeled_map"][
                "LAST_NAME"
            ] = f"{name1} {name2} {name3}"
        else:
            extraction_result["label"] = "PPL_VRF"

        # Check for ambiguous middle names that are both first and last names
        if (name2 in first_names and name2 in family_names) or (
            name3 in first_names and name3 in family_names
        ):
            extraction_result["label"] = "PPL_VRF"
            
        return format_extraction_result(extraction_result)
    
    extraction_result["label"] = "PPL_VRF"
    return format_extraction_result(extraction_result)

def populate_owner_name_array(owner_array, accepted_words):
    owner_names = []
    i = 0
    while i < len(owner_array):
        found = False
        end_idx = len(owner_array)
        while end_idx > i and not found:
            w_composed = " ".join(owner_array[i:end_idx])
            if w_composed in accepted_words:
                owner_names.append(w_composed)
                found = True
                i = end_idx - 1
            end_idx -= 1
        i += 1
    return owner_names

def format_extraction_result(extraction_result):
    if extraction_result["label"] == "PPL_VRF":
        return extraction_result

    # First names (Capitalised)
    found_first_names = extraction_result["name_labeled_map"]["FIRST_NAME"].split()
    formatted_first_names = [name.capitalize() for name in found_first_names]

    # Family names (CAPS LOCK)
    found_family_names = extraction_result["name_labeled_map"]["LAST_NAME"].split()
    formatted_last_names = [name.upper() for name in found_family_names]

    extraction_result["name_labeled_map"]["FIRST_NAME"] = u.remove_extra_spaces(
        " ".join(formatted_first_names)
    )
    extraction_result["name_labeled_map"]["LAST_NAME"] = u.remove_extra_spaces(
        " ".join(formatted_last_names)
    )
    return extraction_result


def remove_city_collision(owner_names, cities, family_names):
    owner_names_reversed = owner_names[::-1]

    name_city_collision = next(
        (
            n
            for n in owner_names_reversed
            if u.string_contains_one_of_substrings(n, cities, use_minimal=False)
            and n in family_names
        ),
        None,
    )
    if name_city_collision:
        owner_names_reversed = [
            n for n in owner_names_reversed if n != name_city_collision
        ]

    if u.string_contains_one_of_substrings(
        " ".join(owner_names_reversed), family_names, use_minimal=False
    ):
        return owner_names_reversed[::-1]
    else:
        return owner_names


def remove_places(owner_text, places_to_remove):
    for place in places_to_remove:
        owner_text = owner_text.replace(place, "")

    return owner_text


def remove_ignore_next(owner_text_minimal, ignore_next, family_names):

    if not u.string_contains_one_of_substrings(owner_text_minimal, ignore_next):
        return owner_text_minimal

    owner_text_res = owner_text_minimal
    contains_last_name = u.string_contains_one_of_substrings(
        owner_text_minimal, family_names, use_minimal=False
    )

    ignored_string = ""
    ignore_start_idx = -1

    for ign in ignore_next:
        idx = u.find_substring(owner_text_res, ign, 0, use_minimal=False)
        if idx != -1 and (ignore_start_idx == -1 or idx < ignore_start_idx):
            ignore_start_idx = idx
            ignored_string = owner_text_res[idx:]
            break

    if ignored_string:
        owner_text_res = u.remove_extra_spaces(
            owner_text_res.replace(ignored_string, "*" * len(ignored_string))
        )

    post_contains_last_name = u.string_contains_one_of_substrings(
        owner_text_res, family_names, use_minimal=False
    )
    if contains_last_name and post_contains_last_name:
        return owner_text_res

    # manage case when ignoring a last name
    elif contains_last_name and not post_contains_last_name:
        sorted_fns = sorted(family_names, key=len, reverse=True)
        found_names = []

        for fn in sorted_fns:
            pos = u.find_substring(ignored_string, fn, 0, use_minimal=False)
            while pos != -1:
                found_names.append(
                    {"position": pos, "position_end": pos + len(fn), "name": fn}
                )
                pos = u.find_substring(ignored_string, fn, pos + 1, use_minimal=False)

        found_names_sorted = sorted(found_names, key=lambda x: x["position"])
        if found_names_sorted:
            processed_ignored_string = replace_unrelevant_text(
                ignored_string, found_names_sorted
            )
            owner_text_res = (
                owner_text_res[: -len(ignored_string)] + processed_ignored_string
            )

        return u.remove_extra_spaces(owner_text_res)

    return owner_text_minimal


def replace_unrelevant_text(ignored_string, found_names_sorted):
    processed_ignored_string = []
    intervals = [
        (name["position"], name["position_end"]) for name in found_names_sorted
    ]

    for i, char in enumerate(ignored_string):
        in_name_interval = False
        for start, end in intervals:
            if start <= i < end:
                in_name_interval = True
                break

        if in_name_interval or char == " ":
            processed_ignored_string.append(char)
        else:
            processed_ignored_string.append("*")

    return "".join(processed_ignored_string)


def extract_unknown_relative_owners(
    owner_text, unknown_relatives_sing, unknown_relatives_plur
):
    owner_text_minimal = u.text_to_minimal(owner_text)

    for unk_rp in unknown_relatives_plur:
        if u.string_contains_substring(owner_text_minimal, unk_rp, use_minimal=False):
            return {
                "owner_count": 2,
                "owner_count_remark": "2+",
                "unknown_relative": unk_rp,
            }

    for unk_rs in unknown_relatives_sing:
        if u.string_contains_substring(owner_text_minimal, unk_rs, use_minimal=False):
            return {
                "owner_count": 1,
                "owner_count_remark": "",
                "unknown_relative": unk_rs,
            }

    return None
