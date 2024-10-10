import utils.utils as u

entity_codes = [
    "ENT",
    "ent_GLD",
    "ent_JEW",
    "ent_OTH",
    "ent_REL_UNL",
    "ent_REL",
    "ent_REL_TTL_UNL",
    "ent_REL_TTL",
    "ent_SCL_UNL",
    "ent_SCL_GRD",
    "ent_SCL_MST",
    "ent_SCL_REL",
    "ent_SCR_UNL",
    "ent_SCR",
    "ent_VNZ",
    "ent_VNZ_TTL",
    "ent_VNZ_UNL",
]


def get_entity_code_from_mention(
    mention,
    guild_entities=[],
    jew_entities=[],
    other=[],
    religious_entities_unlinked=[],
    religious_entities=[],
    religious_titles_entities_unlinked=[],
    religious_titles_entities=[],
    scuole_entities_unlinked=[],
    scuole_grandi_entities=[],
    scuole_mestieri_entities=[],
    scuole_religious_entities=[],
    social_care_entities_unlinked=[],
    social_care_entities=[],
    venezia_entities=[],
    venezia_titles_entities=[],
    venezia_entities_unlinked=[],
):

    # Check mentions against the provided lists
    if mention in guild_entities:
        return "ent_GLD"
    elif mention in jew_entities:
        return "ent_JEW"
    elif mention in other:
        return "ent_OTH"
    elif mention in religious_entities_unlinked:
        return "ent_REL_UNL"
    elif mention in religious_entities:
        return "ent_REL"
    elif mention in religious_titles_entities_unlinked:
        return "ent_REL_TTL_UNL"
    elif mention in religious_titles_entities:
        return "ent_REL_TTL"
    elif mention in scuole_entities_unlinked:
        return "ent_SCL_UNL"
    elif mention in scuole_grandi_entities:
        return "ent_SCL_GRD"
    elif mention in scuole_mestieri_entities:
        return "ent_SCL_MST"
    elif mention in scuole_religious_entities:
        return "ent_SCL_REL"
    elif mention in social_care_entities_unlinked:
        return "ent_SCR_UNL"
    elif mention in social_care_entities:
        return "ent_SCR"
    elif mention in venezia_entities:
        return "ent_VNZ"
    elif mention in venezia_titles_entities:
        return "ent_VNZ_TTL"
    elif mention in venezia_entities_unlinked:
        return "ent_VNZ_UNL"
    else:
        return "ENT"



def is_entity_code(code):
    return code in entity_codes


def is_title_code(code):
    return "TTL" in code


def entity_in_owner_codes(owner_codes):
    owner_codes = [code.strip() for code in owner_codes.split("|")]

    for oc in owner_codes:
        if oc in entity_codes:
            return True

    return False
