---
title: Find full hojok images and transcriptions from Korean archival catalogs
module: Historical household record research
date: '2026-11-24'
problem_type: workflow_issue
component: development_workflow
severity: medium
category: workflow-issues
applies_when:
- Locating full-size images and transcriptions of cataloged household documents
- Building a source-linked sample set for genealogical matching
tags:
- hojok
- korean-archives
- provenance
- primary-sources
- genealogy
---

## Context

A regional household-record search returned Academy of Korean Studies (AKS) catalog descriptions and a `getImageData.aspx` image, but that image was only a 100 × 150 thumbnail. The full historical source and the archive's own transcription were behind a separate Honam Korean Studies viewer. Catalog search hits are not proof that an Anseong Lee ancestor is present, and the portal's image, extracted text, and source-document text are distinct evidence.

## Guidance

1. Search in Korean by locality and document type as well as a person's name: `장수현` / `임실현` with `호구단자` (household declaration), `준호구` (certified extract), or `호적대장` (register). Inspect historical administrative place names and variant Hanja; do not assume that every regional catalog hit belongs to the target clan.
2. Open the individual AKS catalog record, record the `dataUCI` identifier, issuing locality, document date and holding institution. Catalog item links can reveal related documents from the same collection. Search-result images and the archive’s `getImageData.aspx` endpoint can be tiny thumbnails: verify image dimensions rather than treating a successful JPEG response as an archival image.
3. Follow the individual record's `rinksRedirect.aspx?dataUCI=...&isRealView=yes` link to the holder's Honam `dataUCI.jsp` page. For the four items acquired in this session it returned HTML containing `dataText_evo.jsp?data_group=...` and `evoDataImage_evo.jsp?...data_group=...`. The `data_group` is item-specific: obtain it from the page, not from an unrelated record. An archive page can distinguish the item description, original-text transcription and original image.
4. For transcription, open the holder's `dataText_evo.jsp?data_group=...` page and save the contents of the `description` element, converting HTML line breaks and entities without altering Chinese characters. Label it the archive's transcription; compare the handwriting against the image before accepting it as ground truth. If no text is offered, record that absence rather than inventing one.
5. For the image, inspect the `evoDataImage_evo.jsp` form's `img_url` field and its viewer request; for the inspected 1831 record the viewer's source pointed to `/structure/save_img/KCIS_U038 CBNHNKSMC KSM-XD.1831.4575-20140430.ISPTS00002.jpg` on the Honam host. Preserve the actual path indicated by the page and URL-encode spaces when requesting it. Do not assume the same filename or one-image layout for every record. The observed holder route used plain HTTP, so transport does not authenticate the downloaded bytes; save the source link and SHA-256 and corroborate provenance where needed.
6. Check response status and file signature, inspect dimensions and orientation, hash each original, and preserve the catalog URL, document identifier, acquisition date, institution, transcription, and image separately. The acquisition in this session used a temporary script and is not a maintained, tested downloader. If a holder page or viewer changes, rediscover its links; do not present this example endpoint as a stable API.

## Why This Matters

A screenshot or thumbnail can look like a successful download while being too small to read the household details. Taking the extra step from portal metadata to the holder's full image yields evidence that can be zoomed and compared against both transcription and jokbo. Keeping the archive's transcription separate prevents an OCR or transcription discrepancy from being mistaken for a fact in the original. A record from the right county or a shared surname is a lead, not an identity match.

## When to Apply

Use this approach when locating digitized historical household records for the jokbo-to-hojok matching pilot, testing a proposed document schema, or evaluating whether a family and village can be traced through multiple record years. It is particularly useful when the national catalog supplies a thumbnail and redirects to a regional institution.

## Example

The 1831 Imsil declaration for Park Si-un has catalog UCI `KCIS_U038+CBNHNKSMC+KSM-XD.1831.4575-20140430.ISPTS00002`. The AKS item redirects to a Honam page whose JavaScript identifies `data_group=22022`; its text viewer exposed a transcription and its image viewer exposed a 3840 × 5760 JPEG. The retained [sample set](../../../research/hojok-samples/README.md) contains this item, a 1837 declaration by the same named household head, an 1846 declaration, and an 1891 Jangsu extract, with catalog links and image hashes. None is a confirmed Anseong Lee match.

The archive transcriptions list the named 1831 and 1837 household head as 67 and 91, respectively, although the records are six years apart. Treat that as a **candidate discrepancy** until both source images have been inspected: the transcription, document readings, dates, or identification could require further investigation. The 1846 transcription identifies its household head as the son of a deceased Park Si-un; independently assess that apparent connection rather than merging identities automatically.
