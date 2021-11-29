from ravenpackapi import RPApi

api = RPApi()

# get the list of the uploaded files
for f in api.upload.list():
    # here we can access the file - see below for the options
    print(f)

# upload a file to access the analytics
f = api.upload.file("_orig.doc")
#f = api.upload.file("_orig.doc",
                    # upload_mode="RPJSON"
                    # properties={
                    #   "primary_entity": "RavenPack",
                    #   "provider_document_id": "<YOUR_DOCUMENT_ID>"
                    #   "extractor": "PDF_TABLE_EXTRACTOR"
                    #   }
                    #)

# you can also upload from a publicly available URL
# f = api.upload.file("demo.html",
#                     source_url='https://www.w3.org/2001/06/utf-8-test/UTF-8-demo.html'
#                     )

f.wait_for_completion()  # optionally, wait for completition

# we can also get it if we know the id
# f = api.upload.get('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

# get back the analytics found in the document
# f.save_analytics("_analytics.csv", output_format='text/csv')
f.save_analytics("_analytics.json", output_format='application/json')

# the annotated version
f.save_annotated("_annotated_document.json", output_format='application/json')

# or the original
f.save_original("_orig.doc")

# show or save the extracted text
# extracted_text = f.text_extraction()
f.save_text_extraction("_text_extraction.json", output_format='application/json')

# given a file we can set tags
# f.set_metadata(tags=['file tag'])
# f.get_metadata()

# return the process status of the file
f.get_status()

# ... or delete it
# f.delete()

# we can also work with folders
folder = api.upload.folder_create('documents')
print(folder)
folder.folder_name = "papers"
folder.save()

# upload a file into a folder:
f = api.upload.file("_orig.doc", folder=folder)
