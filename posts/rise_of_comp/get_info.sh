#!/bin/bash

;while read -r line;
do curl https://api.semanticscholar.org/graph/v1/paper/$line\?fields\=abstract,venue,referenceCount,citationCount,influentialCitationCount,fieldsOfStudy,tldr,authors,citationCount >> metadata_papers; 
done < list_papersIds.txt
