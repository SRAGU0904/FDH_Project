# 1808 Sommarioni: Data description


# Files:
* `sommarioni_geometries_<date>.geojson`: the vectorization of Venice's 1808 Napolean cadastral maps saved as GeoJSON polygons. Relate to the text data entries through the `geometry_id` field.
* `sommarioni_text_data_<date>.json`: the transcribed textual entries of the cadaster's manuscript (called "sommarioni") with the field `geometry_id` relating the group of geometry from the geometries' geojson file. Parcels function (type of ownership and qualities) have been normalized.
* `people_sommarioni_dataset_<date>.json`: results of a work of disambiguation and standardisation of people mentioned in the Sommarioni done by Carlo Mussi. Holds unique JSON entries per person mentioned in the registry's owner's text. The values from the field `parcel_ids` relate to the `uniqueID` field from the text data file.
* `aggregated/sommarioni_geometries_function_and_people_standardised_<date>.jsoon`: all previous 3 files rendered in a single geojson, contains many duplicates, as there are many poeple who can hold many parcels, and many geometries can be references in many entries. Useful mainly for plotting the data through QGIS.
* `2023_Carlo_musso_Standardising_ownership_information_from_the_Napoleonic_Cadastre_of_1808_Venice__methods_and_findings_in_the_first_database_creation-2.pdf`: Master thesis report of Carlo's work on the standardisation of named entities and unique functions and ownership types in the Sommarioni.

## sommarioni_text_data: metadata fields
- `geometry_id`: a non-null unique integer linking the entry to the group of geometries in the corresponding geojson. 
- `unique_id`: a non-null unique integer identifying the entry. This is an operational field generated to easily reference single data entries and does not stem from the original transcription of the text.
- `district_acronym`: a non-null standardized string representing the sestiere (district) of the entry as an acronym. Possible values are  NSM (`San Marco`), NCS (`Castello`), NCC/NCN (`Cannaregio`), NSP (`San Polo`),  NSC (`Santa Croce`) and NDD (`Dorsoduro`).
- `parcel_number`: a nullable string linking the entry to the coressponding cadaster on the map. The name in the original document is `Numero della Mappa`.
- `sub_parcel_number`: a nullable string used to indicate sub-division of the entry. The name in the original document is `subalterno`.
- `austrian_cadaster_correspondance`: nullable string showing the corresponding number(s) of the austrian cadaster. This attribute does not exist in the orignal document, but comes from a [document from the state archive of venice whose source is no longer accessible.](http://www.archiviodistatovenezia.it/siasve/cgi-bin/pagina.pl?Tipo=inventario&Chiave=520)
- `austro_italian_cadaster_correspondance`: nullable string showing the corresponding number(s) of the austro-italian cadaster. This attribute does not exist in the orignal document, but comes from a [document from the state archive of venice whose source is no longer accessible.](http://www.archiviodistatovenezia.it/siasve/cgi-bin/pagina.pl?Tipo=inventario&Chiave=521)
- `place`: a non-null string representing the toponym (place) locating the entry. This attribute is written in the original document above the entries in the `Denominazione dei Pezzi di Terra` column.
- `house_number`: nullable string of the physical house number of the entry, can be multiple numbers in a chain separated by commas. The name in the original document is `Denominazione dei Pezzi di Terra`.
- `owner`: nullable string denoting the owner of the entry. The family names of this field are transcribed in uppercase, except for the `Cannaregio` sestiere. The name in the original document is `Possessori`.
- `owner_standardised`: nullable string which is a standardised version of the above string.
- `area`: a non-null float value describing the parcel's area in square meters. Likely computed from the vectorization available in the GeoJSON file. Useful for plotting statistics. 
- `quality`: a nullable string of the quality of the entry. It describes the type of good from the entry in a more or less systematic way. The name in the original document is `Qualità`.
- `ownership_types`: a nullable **list** of standardized strings representing the types of ownership. The possible values are `AFFITO`, `PUBBLICO`, `COMMUNE` and `PROPRIO`. This standardized information stems from the `quality` field.
- `qualities`: a nullable **list** of standardized strings representing the possible qualities of a parcel. They are 72 possible values. This standardized information stems from the `quality` field.

## people_sommarioni_dataset: metadata fields
This dataset stems from the "ownership_standardised" text from the "sommarioni_text_data" file. The description below is mainly from Carlo's Musso report (2023_Carlo_musso_Standardising_ownership_information_from_the_Napoleonic_Cadastre_of_1808_Venice__methods_and_findings_in_the_first_database_creation-2.pdf). with some additional type information.
- `own_uid`: non null unique integer, unique ID of the person in the dataset
- `own_nucleus_uid`: non-null integer, identifier of the family nucleus
- `own_family`: non-null string, lastname(s)
- `own_name`: non-null string, firstname(s)
- `own_title`: nullable string, person’s title
- `own_father`: nullable string, father’s name
- `own_father_is_q`: nullable boolean, True if the father is dead, False otherwise
- `own_mother`: nullable string, mother’s name
- `own_siblings`: nullable string, names of all siblings
- `own_husband`: nullable string, husband’s name
- `own_husband_is_q`: nullable boolean, True if husband is dead, False otherwise
- `own_other_notes`: nullable string, any other note
- `parcel_ids`: list of integer, all the unique parcel IDs (unique in the "sommarioni_text_data" json file) where this person appears as the owner or one of the owners.

## sommarioni_geometries: metadata fields
Only the fields stored in the "properties" sub-dict per geoJSON object are described, as they are domain dependant metadata, whereas all other fields are standard geojson properties.
- `id`: non-null string, operational ID attributed to each single geometry, in the format `<type>/<id>`. Multiple geometries may hold the same `id`, it generally means a single parcel with many different kind of geometries (building with a courtyard for instance)
- `parcel_type`: non-null standardized string, represent the type of the geometry, mainly for display purpose. Possibles values are `building`, `courtyard`, `sottoportico`, `street`, `water`.
- `parcel_number`: nullable string, refers to the parcel number associated to the current geometry. Matches with the corresponding value from the "sommarioni_text_data" JSON file. 
- `geometry_id`: non-null integer, an unique identifier grouping all the different geometries to the sommarioni entries they correspond. Matches the values from the corresponding field in the "sommarioni_text_data" and serve as the key to link both files. The value "-1" is used for all the geometries without entries in the register.
- `parish_standardized`: nullable string, refers to the adminstrative delimitation of the parish in which the geometries likely falls within. This is a derived data from an interpretation of the parish boundaries as they were thought to be organized in 1740. The appartenance of parcel was computed by checking under which parish boundaries most of a parcel's geometry fell under. The parishes have likely changed a bit between 1740 and 1808, so this field should not be taken as factual.