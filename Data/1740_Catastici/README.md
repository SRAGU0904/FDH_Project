# 1740 Catastici

# Files
* `catastici_1740_full_geojson_20240917.geojson`: version of the dataset where all single entries have been mapped to their corresponding gps coordinate on the map. It is merely present here for ease of browsing the data in Graphical Information System application such as QGIS, and should not be processed as such, use the `text_data_20240924.json` instead.
* `catastici_text_data_20240924.json`: actual transcription of the Catastici with data relating to the disambiguation of people and institution or other kind of named entities. Information on how such data was produced can be found in `index/README.md`. This file should be used as the main dataset file for analysis and processing.
* `index`: scripts and documentation on how people disambiguation and named entity recognition was performed to obtain the aforementionned file by Carlo Musso. Left here as documentation/inspiration.


# Data Fields

## From the transcription

- `id`: manual id of the entry drawn using a pencil. The sequence of number was restarted at each parish. Is merely useful to  
-  `ten_name`: Name of the tenant,
-  `function`: Function of the parcel
-  `an_rendi`: rent paid.
-  `place`: indication of the place where the parcel is located, can contain information about the place's function or a unique toponym related to this place.

## Operational

- `uidx` unique index for each entry, used for uniquerly identifying separate object
- `uid`: internal identifiant related to the original entry.
- `path_img`: name of the original scan image containing the information.
- `author`: first name of the person that transcribed the entry.

## Standardized / Additonial fields
- `id_napo`: whenever found, the corresponding parcel in the Sommarioni 1808. 
- `sestiere`: the sestiere (district) of the entry as an acronym. Possible values are  SM (`San Marco`), CS (`Castello`), CC/CN (`Cannaregio`), SP (`San Polo`),  SC (`Santa Croce`) and DD (`Dorsoduro`),
- `geometry`: single point coordinate where the parcel is located in CRS84 format.
- `parish_std`: standardized name of the parish.
- `owner_code`: code of owner type
- `owner_count`: number of owners (type `int`)
- `owner_count_remark`: remark for owner count if exact number is not applicable (e.g. *fratelli*)
- `owner_entity`: owner entity name (blank if owner is not an entity)
- `owner_entity_group`: owner entity group standardisation (blank if owner is not an entity)
- `owner_first_name`: owner first name (blank if owner is not an person)
- `owner_family_name`: owner last name (blank if owner is not an person)
- `owner_family_group`: owner family group standardisation (blank if owner is not an person)
- `owner_title`: owner title (blank if owner has not title)
- `owner_title_std`: standardisation or propagation of owner title
- `owner_mestiere`: owner *mestiere* (blank if owner has no *mestiere*)
- `owner_mestiere_std`: standardisation of owner title *mestiere*
