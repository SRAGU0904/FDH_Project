# Dictionaries: 1741 Catastici

@author [Carlo Musso](https://github.com/CaiMusso)

During the first two months of the project all dictionaries containing family names, first names, institutions, titles, *mestieri*, cities and more were created **by hand** and *ad-hoc* for the 1741 Catastici. 

The creation of these dictionaries enabled a very accurate information extraction otherwise impossible to achieve with general-purpose algorithms on such noisy and delicate data as the 1741 Catastici.

Every dictionary and the separation and categorisation of words and mentions in these dictionaries was made by hand as a continuous work in progress during the project. It is a result of a combination of custom tools to format and clean the dictionaries and a meticulous analysis of these terms during meetings with Prof. Isabella di Lenardo and Dr. Paul Guhennec. With historical documents at hand we reconstructed the links between the Catastici mentions to Institutions and Families of 1741 Venice.

## Dictionary Structure
The dictionaries are structured in the following macro-categories:
- **ENT_dictionary**: the Entities dictionary of all mentions or sub-mentions referring to Venetian public institutions.
- **PPL_dictionary**: the People dictionary of all mentions of family names, first names, titles, *mestieri* and other people-related terminology.
- **MSC_dictionary**: the Miscellaneous dictionary contains other useful terms that don't have a common purpose but are necessary for correct information extraction such as cities, separators, unknown owners and others.
- **std_mappings**: the standardised mappings are mappings between all entity mentions and their institutions. For families, the mappings between family name variations and the actual last names. The result of these mappings creates a network that maps entity mentions to institutions and family names to family groups.

## Entity Dictionary
The Entity dictionary contains various files that separate entities and institutions into different categories according to the identity or scope of the institution.

- `entities.json`: this dictionary contains every entity mention (or sub-mention) categorised from the 1741 Catastici. It is the comprehensive set containing all the mentions from other files.
- `venezia_entities.json`: contains mentions or sub-mentions of institutions of the Repubblica di Venezia.
- `venezia_titles_entities.json`: contains mentions or sub-mentions of titles that belong to institutions of the Repubblica di Venezia.
- `guild_entities.json`: contains mentions or sub-mentions of Guild institutions.
- `religious_entities.json`: contains mentions or sub-mentions of Religious institutions.
- `religious_titles_entities.json`: contains mentions or sub-mentions of titles that belong to Religious institutions.
- `scuole_grandi_entities.json`: contains mentions or sub-mentions of the Scuole Grandi di Venezia.
- `scuole_mestieri_entities.json`: contains mentions or sub-mentions of the Scuole mestieri.
- `scuole_religious_entities.json`: contains mentions or sub-mentions of the religious institutional-owned Scuole.
- `social_care_entities.json`: contains mentions or sub-mentions of entities involved in social care and public welfare activities.
- `jew_entities.json`: contains mentions or sub-mentions related to Jewish entities.
- `unlinked_entities.json`: Includes entity mentions that could not be linked to specific categories or that belong to a category but cannot be linked to a specific known institution. This last dictionary is slightly different from the others as it is not a simple list of mentions but a more structured json object containing the list of mentions separated in their categorisation. The key `entities_type` gives us information on the categorisation of these unlinked mentions (*religious_entities*, *scuole_entities*, etc.) while the `entities_unlinked` key is the corresponding list of mentions.

## People Dictionary
The People and Families dictionary contains mentions of family names, first names and their variations. Furthermore, also categorises titles, *mestieri*, relatives and more.

- `family_names.json`: contains family names extracted from the 1741 Catastici.
- `first_names.json`: contains first names extracted from the 1741 Catastici.
- `mestieri.json`: contains job titles or professions.
- `titles.json`: contains institutional titles extracted from the 1741 Catastici and their spelling variations.
- `titles_plur.json`: contains the plural forms of the titles extracted.
- `titles_sing.json`: contains the singular forms of the titles extracted.
- `unknown_relatives.json`: contains mentions of unidentified family relations and their spelling variations (e.g. *fratelli*, *nipoti*, etc).
- `unknown_relatives_plur.json`: contains the plural forms of the unknown relatives extracted.
- `unknown_relatives_sing.json`: contains the singular forms of the unknown relatives extracted.
- `family_names_comp.json`: contains the short words that form a composed family name.

## Miscellaneous Dictionary
Miscellaneous dictionary contains other useful terms that don't have a common purpose but are necessary for correct information extraction.

- `cities.json`: contains city names extracted from the 1741 Catastici.
- `ignore_next.json`: contains terms that signal that the mentioned text and what comes after should be ignored (in practice replaced by '*' symbols) during the People-owned parcels data extraction. These mentions look quite random but are very useful to improve the accuracy of the extraction by ignoring text that is not relevant to the owner.
- `places.json`: contains names of specific places mentioned in the 1741 Catastici.
- `separators.json`: contains characters and strings used as separators of owners when a parcel has more than one owner.
- `unknown_owners.json`: contains exact mentions of explicit "unknown" property owners (e.g. *"non si pote saper"*, *"ne si sa il patron"*)

## Standardisation Mappings & Network
These files are mappings between all entity mentions and their institutions. For families, the mappings between family name variations and the actual last names. This is the result of several meetings where each single mention was looked at and manually categorised as belonging to a certain Institution or Family with the help of official websites, historical documents and the expertise of Prof. Isabella di Lenardo and Dr. Paul Guhennec.

All these standardisations and groupings are done for accuracy, statistics and visualisation purposes trying to get out of the Catastici the most accurate information without tampering with historical facts. This cannot be done without a long, dedicated and accurate human intervention.

The result of these mappings creates a network that maps entity mentions to institutions and family names to family groups. The `std_mappings` directory contains two sub-directories: one for Entities and one for People.

### People to Mentions
The directory [people_to_mentions](/dictionaries/std_mappings/people_to_mentions/) contains the file that maps each family name variation to its standardised spelling (usually the most common). Furthermore, also contains files that map titles and mestieri to their standardised version.

Note: for family name grouping, the assignation process was done through the [NameGrouper WebApp](https://namegrouper-dhlab-epfl.vercel.app) designed and implemented specifically for this task but generalisable to other datasets. All groupings were checked manually contextualising them from their parcel in the Catastici.

Here below the files in **people_to_mentions**.
- `family_name_groups.json` (mapping between family name variations and family groups)
- `mestieri_to_std.json`
- `title_plur_to_sing.json`
- `title_to_std.json`

### Entities to Mentions
The directory [entities_to_mentions](/dictionaries/std_mappings/entities_to_mentions/) contains files that map each entity to its mentions. The files are divided in categories and each file contains multiple entities/institutions with their corresponding mentions. The standardised entity is the value of the key `entity`, the entity mentions is the value list of the key `entity_mentions`; R. di Venezia and Religious entities also have the value list for the key `title_mentions` representing the title-owned mentions of a certain institution (e.g. when the *Primo prete di San Martino* owns a parcel on behalf of *CHIESA DI SAN MARTINO*)

Here below the files in **entities_to_mentions**, titles are self-explanatory.
- `mestieri_to_mentions.json`
- `religious_to_mentions.json`
- `scuole_grandi_to_mentions.json`
- `scuole_mestieri_to_mentions.json`
- `scuole_religious_to_mentions.json`
- `social_care_to_mentions.json`
- `venezia_to_mentions.json`

### The Entity Network
Here below the diagram of the mappings made on entity mentions.

![Entity Mapping - Catastici 1741](https://github.com/CaiMusso/venice-catastici-1741-index/assets/47753346/4edf83d9-b501-4b9c-9685-053ff50b998d)


