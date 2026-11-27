# An archive catalog image was only a thumbnail

Appendix item: 31. Date: 24 November 2026 (JST).

Terms used here:

- A **hojok** (호적) is a Korean household register. Older forms include household declarations (호구단자) and certified extracts of them.
- **AKS** is the Academy of Korean Studies, which runs a national catalog of historical documents. Some items are held and displayed by regional institutions, such as the Honam Korean Studies archive.

## Summary

A regional search for household records returned AKS catalog descriptions with an image. The image was only 100 × 150 pixels. The full image and the archive's own transcription sat behind a separate viewer at the holding institution.

## Impact

A thumbnail looks like a successful download, but it is too small to read household details. Treating it as the record would have meant matching against an image nobody could read.

## How it was noticed

Checking the downloaded file's pixel dimensions, instead of only checking that a JPEG came back.

## Root cause

The catalog serves a preview image. The source document lives on the holder's own site, reached by a redirect link from the catalog record.

## Fix

From each catalog record, follow the "real view" redirect to the holder's page. That page contains item-specific links to the transcription and to the image viewer. For an 1831 household declaration from Imsil County, the viewer exposed a 3840 × 5760 image.

Save the catalog URL, the document identifier, the transcription and the image separately. Record the image's fingerprint (SHA-256). The holder route used plain HTTP, so the connection does not prove the bytes are authentic.

The retrieval used a temporary script. It is not a maintained downloader, and the archive's page structure can change.

## Lesson

Check the dimensions of every archival image you download.

Keep the catalog description, the archive's transcription and the image as three separate pieces of evidence. A transcription can differ from the handwriting.

A record from the right county with the right surname is a lead, not an identity match.

## Evidence

- The internal solution note "Find full hojok images and transcriptions from Korean archival catalogs", which has the step-by-step method.
