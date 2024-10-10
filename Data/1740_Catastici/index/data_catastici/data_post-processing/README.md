# Pipeline output: final datasets

From a dataset point of view, the result of this pipeline can be seen in the columns: 
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

## Content

- `catastici_1741_STD.xlsx`: excel version of the final output of the pipeline
- `catastici_1741_STD_expanded.xlsx`: expanded excel version of the final output of the pipeline

In the `pipeline_steps/` folder:
- `catastici_1741_step1.json`: output of Dataset setup
- `catastici_1741_step2.json`: output of Assignation of empty parcels
- `catastici_1741_step3.json`: output of Assignation of Repubblica di Venezia - owned parcels
- `catastici_1741_step4.json`: output of Assignation of Entity-owned parcels
- `catastici_1741_step5.json`: output of Assignation of People-owned parcels
- `catastici_1741_step6_patterns.json`: output of patterns NER model
- `catastici_1741_step7.json`: output of Assignation of Owners from model output
- `catastici_1741_step8.json`: output of Assignation of standardised Mappings
- `catastici_1741_STD`: json version of the final output of the pipeline
- `catastici_1741_STD_expanded.json`: expanded json version of the final output of the pipeline

