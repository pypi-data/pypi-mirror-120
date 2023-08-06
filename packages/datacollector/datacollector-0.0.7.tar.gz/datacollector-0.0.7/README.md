# Data Collector
## By Query
To get the papers data by search query, you can use the following python script, 
```
from datacollector import datacollector_query

# Search for a query, biofilm co2, with 10 results and download the pdf format of the result 
datacollector_query('biofilm co2', 10, True)

# Search for a query, biofilm co2, with 10 results and without download the pdf format of the result 
datacollector_query('biofilm co2', 10)
```
In this script, it takes 3 arguments.
* Search Query (Non-empty String)
* Number of results (Integer)
* Download PDF file? (yes/no)

NOTE: For the search query, it must be a non-empty String, and if you want more than one query, using + symbol between two words (Ex. word1+word2).
This script will 
* Search for the query at the PubMed repository
* Format the result as JSON format
* Name the JSON with paper’s id (Ex. 1234.json)
* Automatucally create a directory (./datasets_query/json) to save the JSON results 
* For the pdf file, they will be saved into ./pdf

The JSON file will contain the metadata of the paper
* pmid
* authors
* year
* title
* abstract
* doi
* references
* citedby

If you type yes for the third argument, it also will download the paper with pdf format into the pdf directory from a repository HERE.

NOTE: You might not be able to download some of the paper with pdf format. The reason I have found is first the repository doesn’t have it. Second, the paper hasn't been published yet because it’s too new.

## By PMIDs
To get the papers data by list of ids, you can use the following python script, 
```
from datacollector import datacollector_query

# import list of ids with text format, download metadata, and download the pdf format of the result 
datacollector_query('./ids_list.txt', True)

# import list of ids with text format, download metadata without downloading the pdf format of the result 
datacollector_query('./ids_list.txt')

```
In this script, it takes 2 arguments.
* File path (TXT format)
* Download PDF file? (yes/no)

This script will do the same things as ABOVE, but with list of pmids, not query. It also will automatically create a directory (./datasets_id/json) to save the JSON results.
NOTE: For the TXT file, you must separate those pmids with a new line character (“\n”).