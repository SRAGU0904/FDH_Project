# Pipeline: 1741 Catastici

@author [Carlo Musso](https://github.com/CaiMusso)

The Pipeline presented here is the code performing the actual **parcel assignation** and **information extraction** from the `owner_name` attribute of each parcel in the 1741 Catastici.

The 10-stage python pipeline is intended to be executed one file at the time from stage 1 to stage 10. Each stage reads the output of the previous stage, then uses the dictionaries to extract information from all entries for which this stage is responsible. The extracted information is then assigned to new standardised attributes of the dataset and the final output of that stage is written to file.

With this approach, the input and output of each stage is accessible as json file in the [pipeline_steps](/data_catastici/data_post-processing/pipeline_steps/) directory. 

The average execution time of the full pipeline is ~5 minutes.

From a dataset point of view, the result of this pipeline can be seen in the final output files in the columns: 
- **uidx** -  unique index of type `string` in expanded dataset, type `int` in original
- **owner_code** - code of owner type
- **owner_count** - number of owners (type `int`)
- **owner_count_remark** - remark for owner count if exact number is not applicable (e.g. *fratelli*)
- **owner_entity** - owner entity name (blank if owner is not an entity)
- **owner_entity_group** - owner entity group standardisation (blank if owner is not an entity)
- **owner_first_name** - owner first name (blank if owner is not an person)
- **owner_family_name** - owner last name (blank if owner is not an person)
- **owner_family_group** - owner family group standardisation (blank if owner is not an person)
- **owner_title** - owner title (blank if owner has no title)
- **owner_title_std** - standardisation or propagation of owner title
- **owner_mestiere** - owner *mestiere* (blank if owner has no *mestiere*)
- **owner_mestiere_std** - standardisation of owner title *mestiere*
- **parcel_portion** - (only for expanded dataset) is the portion of the parcel owned by this owner (e.g. 0.33 if 3 owners own that parcel)

These columns store the result of information extraction from the `owner_name` column.

## Starting Point
The starting point is the [file](/data_catastici/data_pre-processing/catastici_20240123.json) `catastici_20240123.json` provided by Paul Guhennec. This is the digitalised version of the 1741 Catastici produced by the DHLab.

## Stage 1: Dataset setup
- average execution time: ~ 1s

In this stage, the template of the final augmented dataset is created by adding the attribute-columns mentioned above. By default every `owner_code` is set to TODO, every pipeline step will read all TODOs, process and assign its specific category of owners, then re-write the updated dataset.

## Stage 2: Assignation of empty parcels
- average execution time: ~ 2s

In this stage, all the entries with empty owner_name are marked as blank (BLK as `owner_code`), then the `unknown_owners.json` file is used to assign unknown parcels (UNK as `owner_code`).

## Stage 3: Assignation of Repubblica di Venezia - owned parcels
- average execution time: ~ 5s

In this stage, the `venezia_entities.json` - `venezia_titles_entities.json` - `unlinked_entities.json > venezia_entities` files are used to assign parcels that are owned by institutions belonging to Venice itself. These are assigned with the `owner_code` ent_VNZ, ent_VNZ_TTL, ent_VNZ_UNL respectively.

This stage fills in the attributes: 
`owner_entity` - `owner_title` - `owner_code` - `owner_count` - `owner_count_remark`

## Stage 4: Assignation of Entity-owned parcels
- average execution time: ~ 10s

In this stage, all the files: `guild_entities.json` - `jew_entities.json` - `religious_entities.json` - `religious_titles_entities.json` - `scuole_grandi_entities.json` - `scuole_mestieri_entities.json` - `scuole_religious_entities.json` - `social_care_entities.json` and the `unlinked_entities.json` for all the above are used to assign parcels that are owned by these institutions. See the `owner_code` summary map at the end of this document for more info.

This stage fills in the attributes: 
`owner_entity` - `owner_title` - `owner_code` - `owner_count` - `owner_count_remark`

## Stage 5: Assignation of People-owned parcels
- average execution time: ~ 1min 10s

In this stage, all the files in the `PPL_dictionary` directory are used to assign parcels owned by people, mainly using the function `extract_names` in `utils > utils_people.py`. The pipeline stage spots people using the family name dictionary, removes unnecessary text not related to the owner, then extracts information such as: first and last name, title, *mestiere*, family relations (e.g. *fratello*, *nipoti*) and number of owners.

Note: this stage only considers people-owned parcels owned by a single person, parcels with `separators.json` are ignored and left for stage 6 and 7. When `owner_count > 1` is assigned in this stage it is because a plural family relation was found (e.g. *fratelli*); in this case the `owner_count = 2` and the `owner_count_remark = "2+"`.

This stage fills in the attributes: 
`owner_first_name` - `owner_family_name` - `owner_title` - `owner_mestiere`- `owner_code` - `owner_count` - `owner_count_remark`

## Stage 6: Named Entity Recognition model for assignation
- average execution time: ~ 2min 50s

In this stage, a rule-based [spaCy](https://spacy.io) model for Named Entity Recognition is created to assign the remaining entity-owned or people-owned parcels (in particular those having two or more owners). All dictionaries are fed to the model and labeled with a tag (e.g. FIRST_NAME, LAST_NAME, ENTITY, SEPARATOR), the model then pattern-matches all the TODO parcels in the dataset and **finds the patterns corresponding to each tag**.

The output patterns are then saved to disk and processed in stage 7.

## Stage 7: Assignation of Owners from model output
- average execution time: ~ 15s

In this stage, the output patterns of stage 6 are processed and owners are extracted. The algorithm starts by creating owners based on the output patterns using the `update_owner` function and looping through each parcel, each owner and each pattern extracted from this owner. Then, the created owners are processed in a loop and assigned to the parcels. This stage fills in both the attributes of people-owned and entity-owned parcels according to the owner.

Note that all parcels assigned by the model are appended the string "_m" to their `owner_code`.

This stage fills in the attributes: 
`owner_entity` - `owner_first_name` - `owner_family_name` - `owner_title` - `owner_mestiere`- `owner_code` - `owner_count` - `owner_count_remark`

## Stage 8: Assignation of standardised Mappings
- average execution time: ~ 12s

In this stage, we perform the standardisation of terms by assigning standardised mappings for family names, entities, titles and *mestieri*.
This step is crucial for future data analysis and for the visualisation of the output. Most importantly, it is **necessary** in order to deliver results that match historical facts as opposed to ones that are influenced spelling variations.

Until this stage, we have used all dictionaries except the `std_mappings` folder. Here these mappings are crucial to standardise the terms. Standardisation depends on the category of owner.

### People Standardisation
People standardisation uses the `std_mappings > people_to_mentions` dictionaries to:
- Assign the `owner_family_group` of the corresponding `owner_family_name`. Family names are spelled differently across the Catastici, this step assigns the common name to the group (e.g. *Zustinian* is group *Giustiniani*)
- Assign the standardisation of the owner title and *mestiere*
- Propagate the plural owner titles according to the number of owners (e.g. *Nobil Homini Francesco e Pietro* becomes *NOBIL HOMO | NOBIL HOMO*)

### Entity Standardisation
People standardisation uses the `std_mappings > entities_to_mentions` dictionaries to:

- Assign the `owner_entity_group` of the corresponding `owner_entity`. Entity mentions are mapped to their institutional name (e.g. *scola di san rocco* is group *SCUOLA GRANDE DI SAN ROCCO*)
- Assign the title-owned parcels to the corresponding entity group (e.g. *primo prete di san martin* falls under group *CHIESA DI SAN MARTINO*)


This stage fills in the attributes: 
`owner_entity_group` - `owner_family_group` - `owner_title_std` - `owner_mestiere_std` 

## Stage 9: Format Verification
- average execution time: ~ 12s

This stage checks some formatting and assigns parcels as to-verify if formatting is ambiguous. The following checks are made (and more could be added):
- Family name missing for people-owned entities
- Every entry has same number of first and last names (if at least one first name is present)
- Check very long family names (more than 4 words)

This stage could modify in the attribute `owner_code` to C_VRF (as for check - to verify)

## Final Output and Stage 10: Statistics & Insights

### Final Output

The final output after stage 9 is saved in the `data_catastici > data_post-processing` folder as `catastici_1741_STD.xlsx` in Excel file and in the `pipeline_steps` folder as `catastici_1741_STD.json`.

This file has the following attributes filled in were applicable:
- owner_code
- owner_count
- owner_count_remark
- owner_entity
- owner_entity_group
- owner_first_name
- owner_family_name
- owner_family_group
- owner_title
- owner_title_std
- owner_mestiere
- owner_mestiere_std

Each parcel is assigned an `owner_code` that represents the owner type:

- **PPL** - owner is one or more people
- **PPL_VRF** - people-owned with names to verify
- **ent_VNZ** - owner is an institution of the Republic of Venice
- **ent_VNZ_TTL** - title-owned parcel of the Republic of Venice
- **ent_VNZ_UNL** - parcel of the Republic of Venice (not linkable)
- **ent_REL** - owner is a religious institution
- **ent_REL_TTL** - title-owned parcel of a religious institution
- **ent_REL_TTL_UNL** - title-owned parcel of a religious institution (not linkable)
- **ent_REL_UNL** - owner is a religious institution (not linkable)
- **ent_SCL_GRD** - owner is one of the *Scuole Grandi di Venezia*
- **ent_SCL_REL** - owner is a *Scuola* of a religious institution
- **ent_SCL_MST** - owner is a *Scuola mestieri*
- **ent_SCL_UNL** - owner is a *Scuola* (not linkable)
- **ent_SCR** - owner is a social care institution
- **ent_SCR_UNL** - owner is a social care institution (not linkable)
- **ent_GLD** -  owner is a guild entity
- **ent_JEW** - owner is a jew entity
- **ent_OTH** - owner is a non-categorised entity
- **BLK** - owner_name was blank
- **UNK** - owner_name is an explicit unknown
- **TODO** - the parcel was not assigned by the pipeline

Each of the above has a possible equivalent with "_m" appended if the parcel was assigned in stage 6 and 7 using the spaCy model.

Parcels with multiple owners have filled-in attributes which are separated by a "|" symbol. Since this is not convenient from a data analysis and visualisation point of view, stage 10 of the pipeline creates and expanded version of the dataset with one owner per entry. The rest of stage 10 is statistics and insights.

### Stage 10: Statistics & Insights
In this stage, the expanded version of the dataset is created and all statistics and insights on ownership in 1741 Venice are visualised.

#### Expanded 1741 Catastici
The expanded version in the `data_catastici > data_post-processing` folder as `catastici_1741_STD_expanded.xlsx` in Excel file and in the `pipeline_steps` folder as `catastici_1741_STD_expanded.json`. In this file, instead of having entries with multiple owners, entries with more owners are transformed in multiple entries of one single owner. Thus, in these entries `owner_count` will be fixed to 1 and `parcel_portion` will determine the portion of each owner. Note that the `uidx` changes from type `int` to type `string` in the expanded version. For example a two-owned entry that had `uidx = 123`, now becomes two separated single-owned entries with `uidx = "123_0"` and `uidx = "123_1"`.

#### Statistics & Insights
Stage 10 shows all statistics regarding distribution of ownership in 1741 Venice. A specific part on the impact of the standardisation process on misclassifications is also addressed for both Families and Entities. The notebook is self-explanatory.

##### Example: Distribution of Entity types

![entity_types](https://github.com/CaiMusso/venice-catastici-1741-index/assets/47753346/a34b2c6d-002a-4b7d-98ac-29994201684c)


##### Example: Distribution of Family ownership

![family_ownership](https://github.com/CaiMusso/venice-catastici-1741-index/assets/47753346/8e92f104-1040-494d-83f4-294c081cc885)

