# Do-support with HAVE from COHA
## Output
A tab-separated file (coha_dohave.txt) with data from all of the downloadable [COHA](http://corpus.byu.edu/coha/) texts with a column that indicates whether a given token of HAVE with negation showed do-support or not. Builds on work by [Richard Zimmerman](http://www.old-engli.sh/my-research.php).

## Instructions
  1. Make sure the directory has (or has symbolic links to) all of the .zip files from the COHA Word_lemma_PoS folder (e.g. wlp_1810s_ksw.zip).
  2. Create a tab-separated value file from the first worksheet from the coha-sources.xlsx file in the sources.zip file in the Shared_files (save as from excel) 
  3. Run the DO_HAVE_collate.py

## Details of algorithm
The python script cuts each file into tokens (as marked by sentence ending punctuation or copyright exclusion section). For each file it looks to see if there is a case of negation with possessive HAVE (auxiliary HAVE is excluded by removing any cases of HAVE followed by a perfect participle within 7 words). If negative possessive HAVE is identified, the script check to see if DO is present or not.

## Variable explanation
  1. "id" - COHA text id
  2. "startnum" - word number in file for start of token
  3. "endnum" - word number in file for end of token
  4. "dosupport" - presence/absence of DO
  5. "author" - name of author when known
  6. "genre" - COHA genre code
  7. "year" - Year of publication
