# Venezia: Catastici 1741

@author [Carlo Musso](https://github.com/CaiMusso)

This repository is the result of the work done on the 1741 Catastici between Autumn 2023 and Summer 2024, as part of the Venice Time Machine project of DHLab, EPFL.

## Introduction & Context
The 1741 Catastici is a document registering the **ownership** of parcels in Venice along with additional information such as the location, *sestiere*, parish, tenant, rent and parcel function. This hand-written document from 1741 was digitalised in excel format by DHLab. 

The `owner_name` column of this dataset contains *noisy* text strings showing the owner(s) of the parcel and additional information about them. From these entries we were able to extract information such as: first names, family names, entity names, titles, *mestieri* and in some cases family relations as *fratelli, nipoti*, etc.

The goal of this project is to create a python pipeline that processes the initial dataset and extracts step-by-step the most information possible from the `owner_name` column. The final result is an augmented dataset with additional attributes for each row containing the extracted and standardised information. 
This final dataset represents an accurate Index of parcels in Venice paired with their owners: Institutions or Families.

## Design & Technical Approach
Extracting information using a python pipeline from a historical document as the 1741 Catastici is a very delicate and intricate task that **has to be done with the highest accuracy to ensure not to tamper with historical facts**. 
For this reason, the strategy chosen to extract this information is a **rule-based dictionary-driven approach** that executes in sequential pipeline steps that categorise a specific type of owner during each stage.

### Dictionaries
During the first two months of the project all dictionaries containing family names, first names, institutions, titles, *mestieri*, cities and more were created **by hand** and *ad-hoc* for the 1741 Catastici. These dictionaries were then continuously updated and fixed during all the duration of the project. 

The creation of these dictionaries enabled a very accurate information extraction otherwise impossible to achieve with general-purpose algorithms on such noisy and delicate data as the 1741 Catastici.

More information on these dictionaries in the `dictionaries`[directory](/dictionaries/).

### Pipeline 
The 10-stage python pipeline is intended to be executed one file at the time from stage 1 to stage 10. Each stage reads the output of the previous stage, then uses the dictionaries to extract information from all entries for which this stage is responsible. The extracted information is then assigned to new standardised attributes of the dataset and the final output of each stage is written to file.

With this approach, the input and output of each stage is accessible as json file in the [pipeline_steps](data_catastici/data_post-processing/pipeline_steps/) directory. 
More information on the pipeline, parcel assignation and information extraction in the [pipeline](/pipeline/) directory.

## Conclusion & Output
The final output of the pipeline is an augmentation of the original digitalised version of the 1741 Catastici. This augmentation consists in the addition of the following attributes for each entry: *owner_code* - *owner_count* - *owner_count_remark* - *owner_entity* - *owner_entity_group* - *owner_first_name* - *owner_family_name* - *owner_family_group* - *owner_title* - *owner_title_std* -
*owner_mestiere* - *owner_mestiere_std*.


The final output is of two types and of two file formats. These files were all generated based on the input file `catastici_20240123.json` provided by Paul Guhennec, available in the [data_pre-processing](/data_catastici/data_pre-processing/) repository.

- `catastici_1741_STD.json`: json version of the final output of the pipeline
- `catastici_1741_STD.xlsx`: excel version of the final output of the pipeline

The **expanded version** is intended for data visualisation or statistics as it is easier to use. Instead of having entries with multiple owners, entries with more owners are transformed in multiple entries of one single owner. Thus, in these entries `owner_count` will be fixed to 1 and `parcel_portion` will determine the portion of each owner. Note that the `uidx` changes from type `int` to type `string` in the expanded version. For example a two-owned entry that had `uidx = 123`, now becomes two separated single-owned entries with `uidx = "123_0"` and `uidx = "123_1"`.

- `catastici_1741_STD_expanded.json`: expanded json version of the final output of the pipeline
- `catastici_1741_STD_expanded.xlsx`: expanded excel version of the final output of the pipeline

