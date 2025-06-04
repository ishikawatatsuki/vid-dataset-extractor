# VID-dataset extractor

A simple python script that extracts csv files out of VID-dataset formatted in bag file, available in https://github.com/ZJU-FAST-Lab/VID-Dataset?tab=readme-ov-file.

## Usage

### Build a docker container
`docker build --tag vid_data_extractor .`

### Run the container
```
docker run --rm \
	--mount type=bind,source=./extractor.py,target=/app/extractor.py \
	--mount type=bind,source=./misc.py,target=/app/misc.py \
	--mount type=bind,source=./data/VID_dataset,target=/app/VID_dataset \
	-it vid_data_extractor
```

### Run the python script:
***When specifying a .bag file***

`python extractor.py --bag_file ./data/VID_dataset/{filename}.bag`

***When extracting all bag files***

`python extractor.py`
