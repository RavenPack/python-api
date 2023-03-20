import glob
import os
from concurrent.futures.thread import ThreadPoolExecutor

from ravenpackapi import RPApi

api = RPApi()

files_to_batch_upload = glob.glob('folder/*.txt')  # we upload all the files in this folder
print(files_to_batch_upload)


def upload_and_get_results(file_path, output_path, method_name, extra_args=None):
    """ We upload the file_path and call its method_name to save to output_file """
    print(f"Uploading {file_path}")
    f = api.upload.file(file_path)

    # now let's get the output using the parameters
    print(f"Saving output to {output_path}")
    method = getattr(f, method_name)
    method(output_path, **(extra_args or {}))


print(f"Uploading {len(files_to_batch_upload)} files")
with ThreadPoolExecutor(max_workers=5) as thread_executor:  # we upload and get the results concurrently
    for file_path in files_to_batch_upload:
        output_path = f"{file_path}.csv"  # we save in the same folder, with an extra extension
        if not os.path.isfile(output_path):  # skip if the output exists already
            thread_executor.submit(  # submit to the threadpool
                upload_and_get_results,
                file_path=file_path,
                output_path=output_path,
                method_name='save_analytics',
                extra_args={"output_format": 'text/csv'},
            )
