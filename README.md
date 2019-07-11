[28-Mar-2019]

This project is for the maintenance of the DASH part 1 schemas (ISO/IEC 23009-1).

There are necessarily a few branches at this time as we have a few things going on in parallel:

master – verbatim from w18312 (draft FDIS 3rd Ed). Note that I did not include xlink.xsd since that’s not ISO’s and should not be in the electronic attachments. The master has various errors covered in the open issues. A release was created for the baseline master since it was published in the FDIS 3rd Ed. Do not make PRs against this master branch.

3rd-Ed (from master) – schema typos are fixed and is the target for the final 3rd Ed schema and examples. No more edits should be made to this branch unless you find an error WRT to the spec text, in which case an issue should be filed. I will ensure that it matches the as-published 3rd Ed in a few months. Do not make PRs against this branch.  

Amd5 (from 3rd-Ed) – this is the beginning of the schema for FDAM5 (as of this morning, aka FDIS 4th Ed).  FYI, I have fixes committed for the errors in G4, G5 and G8, but I am along ways from adding the schema updates from COR3+DAM5+SoDAM5 found in my m47966-v6; which would then need to be modified per the DoC output from this meeting (which would include for example the mixed=true on Event).

This is the not forum for proposing changes to DASH. This is a forum for working through the details of the intent of approved contributions and TexOf text outputs, as well as fixing errors.

