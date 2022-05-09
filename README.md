# large_repo_uploader

This is a utility script for working with large repos (over 500MB) and the Uleska Platform.  It will only remove files if it needs to in order to bring the repo under 500MB. This script:

* Checks the size of the repo, and if it's over 500MB it will attempt to remove some extranious files.
* Removes large zip or image files not used in scans (suffixs ending in .zip, .ZIP, .jpg, .JPEG, .wmv).  If this brings the repo under 500MB it'll jump to the ZIP step.
* If repo is still over 500MB it removes binary files that are typically large (suffixs ending in .bin, .so, .so.2, .dylib, .dll).  This loses some quality (SCA tools won't pick them up) but will help move to scanning.  If this brings the repo under 500MB it'll jump to the ZIP step.
* If repo is still over 500MB it removes the .git directory as a last option.  Again this prevents the .git history from being searched for secrets, but allows testing to progress (hopefully).
* If repo is still over 500MB after the above steps, the script will exit with a failure and no upload will occur.
* Assuming repo is below 500MB, it ZIPs the repo up.
* Configures your app version to take a repo via ZIP instead of from GIT.
* Uploads the repo to the Uleska Platform for the application and version specified

You can the run a security toolkit from the Uleska UI (or API).  You can run this script as many times as you need - it will refresh the ZIP file as needed.

You will need an account to the Uleska Platform, an auth token, and an application/version to upload to.

Usage is as follows:

    usage: large_repo_uploader.py [-h] --uleska_host ULESKA_HOST --token TOKEN
                              [--application_name APPLICATION_NAME]
                              [--version_name VERSION_NAME] [--path PATH]

    Uleska 'Large Repo Uploader'. Removes typically large files and uploads to the
    project/pipeline to test (you can specify either --application_name and
    --version_name, or --application and --version (passing GUIDs))

    optional arguments:
      -h, --help            show this help message and exit
      --uleska_host ULESKA_HOST
                            URL to the Uleska host (e.g. https://s1.uleska.com/)
                            (note final / is required)
      --token TOKEN         String for the authentication token
      --application_name APPLICATION_NAME
                            Name for the application to reference
      --version_name VERSION_NAME
                            Name for the version/pipeline to reference
      --path PATH           path to the local code repo to trim, zip, and upload

You can run it as follows:
    
    python3 large_repo_uploader.py --uleska_host https://my.uleska.io/ --token *** --application_name "My app" --version_name "My version" --path /path/to/my/repo/



# Example Run

This is an example run of the helper tool working on a large repo (tensorflow) and removing elements to allow it to upload.

python3 large_file_uploader.py --uleska_host https://test.uleska.com --token U.aaaaaaaaa-a01c-aaaa-aaa-2484ce9294ef.aaaaaaaaaaa  --application_name tensorflow --version_name mainline --path ../redirect/tensorflow
ApplicationsURL is: https://test.uleska.com/SecureDesigner/api/v1/applications/
Application ID found for [tensorflow]: 37d1a988-71f6-434d-8b52-3574bbf39fe5
Version ID found for [mainline]: f81ea447-5c36-4c3e-8eb8-13a88e59b756
Mapped names to ids: application name [tensorflow], id [37d1a988-71f6-434d-8b52-3574bbf39fe5], version name [mainline] id [f81ea447-5c36-4c3e-8eb8-13a88e59b756]
Pre-check size of repo is 1.2G

As repo is above 500 MB we will remove ZIPs and images that are not scanned by security tools...

Removing file ../redirect/tensorflow/tensorflow/core/lib/jpeg/testdata/bad_huffman.jpg
Removing file ../redirect/tensorflow/tensorflow/core/lib/jpeg/testdata/corrupt.jpg
Removing file ../redirect/tensorflow/tensorflow/core/lib/jpeg/testdata/corrupt34_2.jpg
Removing file ../redirect/tensorflow/tensorflow/core/lib/jpeg/testdata/corrupt34_3.jpg
Removing file ../redirect/tensorflow/tensorflow/core/lib/jpeg/testdata/corrupt34_4.jpg
Removing file ../redirect/tensorflow/tensorflow/core/lib/jpeg/testdata/jpeg_merge_test1.jpg
Removing file ../redirect/tensorflow/tensorflow/core/lib/jpeg/testdata/jpeg_merge_test1_cmyk.jpg
Removing file ../redirect/tensorflow/tensorflow/core/lib/jpeg/testdata/medium.jpg
Removing file ../redirect/tensorflow/tensorflow/core/lib/jpeg/testdata/small.jpg
Removing file ../redirect/tensorflow/tensorflow/core/lib/psnr/testdata/cat_q20.jpg
Removing file ../redirect/tensorflow/tensorflow/core/lib/psnr/testdata/cat_q72.jpg
Removing file ../redirect/tensorflow/tensorflow/core/lib/psnr/testdata/cat_q95.jpg
Removing file ../redirect/tensorflow/tensorflow/core/profiler/g3doc/pprof.jpg
Removing file ../redirect/tensorflow/tensorflow/core/profiler/g3doc/profiler_ui.jpg
Removing file ../redirect/tensorflow/tensorflow/examples/label_image/data/grace_hopper.jpg
Removing file ../redirect/tensorflow/tensorflow/examples/multibox_detector/data/surfers.jpg
Removing file ../redirect/tensorflow/tensorflow/lite/examples/ios/simple/data/grace_hopper.jpg
Removing file ../redirect/tensorflow/tensorflow/lite/experimental/acceleration/mini_benchmark/chessboard.jpg
Removing file ../redirect/tensorflow/tensorflow/lite/experimental/acceleration/mini_benchmark/snow_4032_3024_3.jpg
Removing file ../redirect/tensorflow/tensorflow/lite/experimental/acceleration/mini_benchmark/test_card.jpg
Removing file ../redirect/tensorflow/tensorflow/lite/g3doc/images/convert/op_fusion_banner.jpg
Removing file ../redirect/tensorflow/tensorflow/lite/g3doc/inference_with_metadata/task_library/images/dogs.jpg
Removing file ../redirect/tensorflow/tensorflow/lite/g3doc/inference_with_metadata/task_library/images/plane.jpg
Removing file ../redirect/tensorflow/tensorflow/lite/g3doc/inference_with_metadata/task_library/images/sparrow.jpg
Removing file ../redirect/tensorflow/tensorflow/lite/g3doc/performance/images/optimization.jpg
Removing file ../redirect/tensorflow/tensorflow/lite/java/src/testdata/grace_hopper_224.jpg
Removing file ../redirect/tensorflow/tensorflow/lite/tools/evaluation/stages/testdata/grace_hopper.jpg
Removing file ../redirect/tensorflow/tensorflow/tools/android/test/sample_images/classify1.jpg
Removing file ../redirect/tensorflow/tensorflow/tools/android/test/sample_images/detect1.jpg
Removing file ../redirect/tensorflow/tensorflow/tools/android/test/sample_images/stylize1.jpg
Finished ZIP and image removal.

Repo is still above 500 MB (it's 1.2G) so we will have to remove binaries.  Note this means 3rd party library scanners won't be able to scan existing libraries, however they will still be able to scan your 3rd party config files (e.g. NPM, maven, etc).

Removing file ../redirect/tensorflow/tensorflow/core/kernels/spectrogram_test_data/short_test_segment_spectrogram.csv.bin
Removing file ../redirect/tensorflow/tensorflow/core/kernels/spectrogram_test_data/short_test_segment_spectrogram_400_200.csv.bin
Removing file ../redirect/tensorflow/tensorflow/lite/experimental/acceleration/compatibility/gpu_compatibility.bin
Removing file ../redirect/tensorflow/tensorflow/lite/java/src/testdata/add.bin
Removing file ../redirect/tensorflow/tensorflow/lite/java/src/testdata/add_unknown_dimensions.bin
Removing file ../redirect/tensorflow/tensorflow/lite/java/src/testdata/float32.bin
Removing file ../redirect/tensorflow/tensorflow/lite/java/src/testdata/int32.bin
Removing file ../redirect/tensorflow/tensorflow/lite/java/src/testdata/int64.bin
Removing file ../redirect/tensorflow/tensorflow/lite/java/src/testdata/invalid_model.bin
Removing file ../redirect/tensorflow/tensorflow/lite/java/src/testdata/mul_add_signature_def.bin
Removing file ../redirect/tensorflow/tensorflow/lite/java/src/testdata/multi_signature_def.bin
Removing file ../redirect/tensorflow/tensorflow/lite/java/src/testdata/quantized.bin
Removing file ../redirect/tensorflow/tensorflow/lite/java/src/testdata/string.bin
Removing file ../redirect/tensorflow/tensorflow/lite/java/src/testdata/string_scalar.bin
Removing file ../redirect/tensorflow/tensorflow/lite/java/src/testdata/tile_with_bool_input.bin
Removing file ../redirect/tensorflow/tensorflow/lite/java/src/testdata/uint8.bin
Removing file ../redirect/tensorflow/tensorflow/lite/python/optimize/test_data/mobilenet_like_model.bin
Removing file ../redirect/tensorflow/tensorflow/lite/python/optimize/test_data/string_input_flex_model.bin
Removing file ../redirect/tensorflow/tensorflow/lite/python/testdata/pc_conv.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/0_subgraphs.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/2_subgraphs.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/2_subgraphs_dont_delegate_name.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/add.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/add_quantized.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/add_quantized_int8.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/add_shared_tensors.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/call_once_mul.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/conv3d_huge_im2col.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/conv_huge_im2col.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/custom_lstm.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/custom_sinh.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/double_flex.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/dynamic_shapes.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/empty_model.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/lstm.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/multi_add.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/multi_add_flex.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/multi_signatures.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/multi_subgraphs_while.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/no_subgraphs.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/segment_sum_invalid_buffer.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/softplus_flex.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/sparse_tensor.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/string_input_model.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/test_min_runtime.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/test_model.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/test_model_broken.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/test_model_redux_precision.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/test_model_versioned_ops.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/two_subgraphs.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/unidirectional_sequence_lstm.bin
Removing file ../redirect/tensorflow/tensorflow/lite/testdata/while_op_with_forwarding_input.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/add_with_const_input.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/argmax.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/broadcast_to.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/concat.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/custom_op.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/fc.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/fc_qat.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/gather_nd.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/lstm_calibrated.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/lstm_calibrated2.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/lstm_quantized.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/lstm_quantized2.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/maximum.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/minimum.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/mixed.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/mixed16x8.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/multi_input_add_reshape.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/pack.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/quantized_with_gather.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/resource_vars_calibrated.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/single_avg_pool_min_minus_5_max_plus_5.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/single_conv_no_bias.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/single_conv_weights_min_0_max_plus_10.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/single_conv_weights_min_minus_127_max_plus_127.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/single_softmax_min_minus_5_max_plus_5.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/split.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/svdf_calibrated.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/svdf_quantized.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/transpose.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/unidirectional_sequence_lstm_calibrated.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/unidirectional_sequence_lstm_quantized.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/unpack.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/weight_shared_between_convs.bin
Removing file ../redirect/tensorflow/tensorflow/lite/tools/optimize/testdata/where.bin

Repo is still above 500 MB (it's 1.2G) so we will have to remove the .git directory.  Note this means secrets scanners that check the git won't be able to check historical git pushes.

Removing directory ../redirect/tensorflow/.git

Removed all unnecessary files...

Reduced repo size is now 299M

Creating zip file...
Created zip file ../redirect/tensorflow_zipped.zip

Setting version config to accept ZIP files, URL: https://test.uleska.com/SecureDesigner/api/v1/applications/37d1a988-71f6-434d-8b52-3574bbf39fe5/versions/f81ea447-5c36-4c3e-8eb8-13a88e59b756

Version config now set to use ZIP upload.

Uploading ZIP file.

Upload URL: https://test.uleska.com/SecureDesigner/api/v1/applications/37d1a988-71f6-434d-8b52-3574bbf39fe5/versions/f81ea447-5c36-4c3e-8eb8-13a88e59b756/upload


Upload successful in 2.4144349098205566 seconds.
